#!/usr/bin/env python3
"""
Main Invoice Processor

Orchestrates the complete flow:
1. OCR extraction from invoice
2. HSN code matching
3. User confirmation
4. Save categorized invoice
5. Generate GSTR-3B (monthly)

This is the main entry point for the MVP.
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from .ocr import InvoiceOCR
from .hsn_matcher import HSNMatcher
from .gstr3b import GSTR3BGenerator
from .db import db  # Database handler


class InvoiceProcessor:
    """Main invoice processing orchestrator"""

    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize processor

        Args:
            base_dir: Base directory for data storage
        """
        if base_dir is None:
            base_dir = Path(__file__).parent.parent / 'data'
        else:
            base_dir = Path(base_dir)

        self.base_dir = base_dir
        self.invoices_dir = base_dir / 'invoices'
        self.uploads_dir = base_dir.parent / 'uploads'

        # Create directories
        self.invoices_dir.mkdir(parents=True, exist_ok=True)
        self.uploads_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.ocr = InvoiceOCR()
        self.hsn_matcher = HSNMatcher()

        # Load user corrections if available
        corrections_file = self.base_dir / 'user_corrections.json'
        if corrections_file.exists():
            self.hsn_matcher.load_corrections(str(corrections_file))

    def process_invoice(self, invoice_file: str, invoice_type: str = 'purchase',
                       auto_confirm: bool = False) -> Dict:
        """
        Process a single invoice (end-to-end)

        Args:
            invoice_file: Path to invoice file (PDF/image)
            invoice_type: 'sales' or 'purchase'
            auto_confirm: If True, auto-accept HSN suggestions >85% confidence

        Returns:
            Processed invoice data with categorization
        """
        print(f"\n{'='*60}")
        print(f"Processing Invoice: {Path(invoice_file).name}")
        print(f"Type: {invoice_type.upper()}")
        print(f"{'='*60}\n")

        # Step 1: OCR Extraction
        print("Step 1: Extracting data using OCR...")
        ocr_result = self.ocr.extract_invoice_data(invoice_file)

        if not ocr_result['success']:
            return {
                'success': False,
                'error': 'OCR extraction failed',
                'details': ocr_result
            }

        print(f"✓ OCR completed (confidence: {ocr_result['confidence']}%)")
        print(f"  Vendor GSTIN: {ocr_result['vendor_gstin'] or 'Not found'}")
        print(f"  Invoice #: {ocr_result['invoice_number'] or 'Not found'}")
        print(f"  Date: {ocr_result['invoice_date'] or 'Not found'}")
        print(f"  Total: ₹{ocr_result['total_amount']:,.2f}")

        # Step 2: HSN Matching for Line Items
        print("\nStep 2: Matching HSN codes...")

        categorized_items = []

        # For MVP, if no line items extracted, create one from total
        if not ocr_result.get('line_items'):
            print("  No line items extracted. Using total amount as single item.")

            # Try to infer item description from filename or ask user
            item_description = self._infer_item_description(invoice_file)

            hsn_result = self.hsn_matcher.suggest_hsn(item_description)

            # User confirmation
            if auto_confirm:
                confirmed = True
                status = "High Confidence" if hsn_result['confidence'] >= 85 else "Low Confidence"
                print(f"  Auto-confirmed HSN ({status}) for '{item_description}': {hsn_result['hsn_code']} ({hsn_result['confidence']}%)")
            else:
                confirmed = self._confirm_hsn(item_description, hsn_result, auto_confirm)

            if confirmed:
                categorized_items.append({
                    'description': item_description,
                    'quantity': 1,
                    'rate': ocr_result['total_amount'],
                    'amount': ocr_result['total_amount'],
                    'hsn_code': hsn_result['hsn_code'],
                    'gst_rate': hsn_result['gst_rate'],
                    'confidence': hsn_result['confidence']
                })
            else:
                print("⚠️  Skipping invoice due to unconfirmed HSN code")
                return {'success': False, 'error': 'HSN confirmation failed'}

        else:
            # Process each line item
            for item in ocr_result['line_items']:
                hsn_result = self.hsn_matcher.suggest_hsn(item['description'])

                # User confirmation
                if auto_confirm:
                    confirmed = True
                    status = "High Confidence" if hsn_result['confidence'] >= 85 else "Low Confidence"
                    print(f"  Auto-confirmed HSN ({status}) for '{item['description']}': {hsn_result['hsn_code']} ({hsn_result['confidence']}%)")
                else:
                    confirmed = self._confirm_hsn(item['description'], hsn_result, auto_confirm)

                if confirmed:
                    item['hsn_code'] = hsn_result['hsn_code']
                    item['gst_rate'] = hsn_result['gst_rate']
                    item['confidence'] = hsn_result['confidence']
                    categorized_items.append(item)
                else:
                    print(f"⚠️  Skipping item '{item['description']}' due to unconfirmed HSN code")
                    # Decide whether to skip the whole invoice or just the item
                    # For now, if any item is unconfirmed, we'll fail the whole invoice
                    return {'success': False, 'error': f"HSN confirmation failed for item: {item['description']}"}


        # Step 3: Build Final Invoice Data
        invoice_id = str(uuid.uuid4())

        # Calculate tax amounts if not already present or if we need to recalculate
        # If OCR didn't extract tax amounts, calculate from total and GST rate
        cgst_amount = ocr_result['cgst']
        sgst_amount = ocr_result['sgst']
        igst_amount = ocr_result['igst']
        
        # User's State Code (Hardcoded for MVP, should come from User Profile)
        USER_STATE_CODE = "32" # Kerala
        
        # Extract Vendor State Code
        vendor_gstin = ocr_result['vendor_gstin']
        vendor_state_code = vendor_gstin[:2] if vendor_gstin and len(vendor_gstin) >= 2 else None
        
        # If no tax amounts found but we have total and GST rate, calculate them
        if (cgst_amount == 0 and sgst_amount == 0 and igst_amount == 0 and 
            ocr_result['total_amount'] > 0 and categorized_items):
            
            gst_rate = categorized_items[0]['gst_rate']
            total_amount = ocr_result['total_amount']
            
            # Calculate tax from total (assuming total includes tax)
            # Formula: Tax = Total × (GST% / (100 + GST%))
            total_tax = total_amount * (gst_rate / (100 + gst_rate))
            
            # Determine Tax Type based on State Code
            if vendor_state_code and vendor_state_code != USER_STATE_CODE:
                # Inter-State -> IGST
                igst_amount = total_tax
                cgst_amount = 0
                sgst_amount = 0
            else:
                # Intra-State -> CGST + SGST (Default if state code unknown)
                cgst_amount = total_tax / 2
                sgst_amount = total_tax / 2
                igst_amount = 0

        categorized_invoice = {
            'invoice_id': invoice_id,
            'type': invoice_type,
            'invoice_type': invoice_type,  # Add for frontend compatibility
            'vendor_gstin': ocr_result['vendor_gstin'],
            'vendor_state_code': vendor_state_code, # Store for reference
            'invoice_number': ocr_result['invoice_number'],
            'invoice_date': ocr_result['invoice_date'],
            'line_items': categorized_items,
            'total_amount': ocr_result['total_amount'],
            'cgst': cgst_amount,
            'sgst': sgst_amount,
            'igst': igst_amount,
            'cgst_amount': cgst_amount,  # Add for frontend compatibility
            'sgst_amount': sgst_amount,  # Add for frontend compatibility
            'igst_amount': igst_amount,  # Add for frontend compatibility
            'gst_rate': categorized_items[0]['gst_rate'] if categorized_items else None,
            'itc_eligible': invoice_type == 'purchase',  # Simplified logic
            'ocr_confidence': ocr_result['confidence'],
            'categorization_status': 'confirmed',
            'reconciliation_status': 'pending',  # New field for GSTR-2A matching
            'processed_at': datetime.now().isoformat(),
            'original_file': str(invoice_file)
        }

        # Step 4: Save Invoice (Local JSON)
        output_file = self.invoices_dir / f"{invoice_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(categorized_invoice, f, indent=2, ensure_ascii=False)

        print(f"\n✓ Invoice saved locally: {output_file.name}")

        # Step 5: Save to Database (Supabase)
        if db.is_connected():
            print("  Saving to Supabase database...")
            db_result = db.save_invoice(categorized_invoice)
            if db_result.get("success"):
                print("✓ Saved to Supabase")
            else:
                print(f"⚠️  Failed to save to Supabase: {db_result.get('error')}")

        return {
            'success': True,
            'invoice_id': invoice_id,
            'invoice_data': categorized_invoice
        }

    def _infer_item_description(self, invoice_file: str) -> str:
        """Infer item description from filename or ask user"""
        filename = Path(invoice_file).stem

        # Try to extract meaningful description from filename
        # e.g., "laptop_invoice.pdf" → "laptop"
        cleaned = filename.replace('_', ' ').replace('-', ' ').replace('invoice', '').strip()

        if cleaned:
            return cleaned
        else:
            # Fallback: ask user
            return input("  Enter item description: ").strip()

    def _confirm_hsn(self, item_description: str, hsn_result: Dict, auto_confirm: bool = False) -> bool:
        """
        Ask user to confirm HSN code suggestion

        Args:
            item_description: Item description
            hsn_result: HSN matching result
            auto_confirm: Not used in interactive mode, but kept for signature compatibility

        Returns:
            True if confirmed, False otherwise
        """
        if not hsn_result['hsn_code']:
            print(f"\n  ⚠️  No HSN match found for: {item_description}")
            print(f"  Please manually assign HSN code (or skip)")
            return False

        print(f"\n  Item: {item_description}")
        print(f"  Suggested HSN: {hsn_result['hsn_code']} ({hsn_result['gst_rate']}% GST)")
        print(f"  Confidence: {hsn_result['confidence']}%")

        # Show alternatives if available
        if len(hsn_result['matches']) > 1:
            print(f"\n  Alternatives:")
            for i, alt in enumerate(hsn_result['matches'][1:3], 1):
                print(f"    {i}. HSN {alt['hsn_code']}: {alt['description']} ({alt['gst_rate']}%)")

        response = input(f"\n  Accept? (y/n/number): ").strip().lower()

        if response == 'y' or response == 'yes':
            return True
        elif response.isdigit() and 1 <= int(response) <= len(hsn_result['matches']):
            # User selected alternative
            alt_index = int(response)
            selected = hsn_result['matches'][alt_index]
            hsn_result['hsn_code'] = selected['hsn_code']
            hsn_result['gst_rate'] = selected['gst_rate']

            # Learn from correction
            self.hsn_matcher.learn_from_correction(
                item_description,
                selected['hsn_code'],
                selected['gst_rate']
            )

            return True
        else:
            return False

    def generate_gstr3b(self, month: int, year: int, gstin: str,
                       output_file: Optional[str] = None) -> Dict:
        """
        Generate GSTR-3B for a specific month

        Args:
            month: Month (1-12)
            year: Year (YYYY)
            gstin: User's GSTIN
            output_file: Path to save GSTR-3B JSON

        Returns:
            Generated GSTR-3B data
        """
        print(f"\n{'='*60}")
        print(f"Generating GSTR-3B for {month:02d}/{year}")
        print(f"{'='*60}\n")

        # Initialize generator
        generator = GSTR3BGenerator(gstin)

        # Load all invoices
        generator.load_invoices_from_directory(str(self.invoices_dir))

        # Generate GSTR-3B
        gstr3b = generator.generate(month, year)

        # Print summary
        generator.print_summary(gstr3b)

        # Save to file
        if output_file is None:
            output_file = self.base_dir / f"gstr3b_{month:02d}_{year}.json"

        generator.save_to_file(gstr3b, str(output_file))

        return {
            'success': True,
            'gstr3b': gstr3b,
            'file_path': str(output_file)
        }

    def save_corrections(self):
        """Save user corrections for future use"""
        corrections_file = self.base_dir / 'user_corrections.json'
        self.hsn_matcher.save_corrections(str(corrections_file))


# CLI Interface
def main():
    """Command-line interface for the processor"""
    import argparse

    parser = argparse.ArgumentParser(description='GST Invoice Processor')

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Process invoice command
    process_parser = subparsers.add_parser('process', help='Process an invoice')
    process_parser.add_argument('invoice_file', help='Path to invoice file')
    process_parser.add_argument('--type', choices=['sales', 'purchase'],
                              default='purchase', help='Invoice type')
    process_parser.add_argument('--auto-confirm', action='store_true',
                              help='Auto-confirm HSN matches >85%% confidence')

    # Generate GSTR-3B command
    gstr_parser = subparsers.add_parser('gstr3b', help='Generate GSTR-3B')
    gstr_parser.add_argument('gstin', help='Your GSTIN')
    gstr_parser.add_argument('month', type=int, help='Month (1-12)')
    gstr_parser.add_argument('year', type=int, help='Year (YYYY)')
    gstr_parser.add_argument('--output', help='Output file path')

    args = parser.parse_args()

    # Initialize processor
    processor = InvoiceProcessor()

    if args.command == 'process':
        # Process invoice
        result = processor.process_invoice(
            args.invoice_file,
            invoice_type=args.type,
            auto_confirm=args.auto_confirm
        )

        if result['success']:
            print(f"\n✅ Success! Invoice ID: {result['invoice_id']}")
        else:
            print(f"\n❌ Failed: {result.get('error', 'Unknown error')}")

        # Save corrections
        processor.save_corrections()

    elif args.command == 'gstr3b':
        # Generate GSTR-3B
        gstr3b = processor.generate_gstr3b(
            month=args.month,
            year=args.year,
            gstin=args.gstin,
            output_file=args.output
        )

        print(f"\n✅ GSTR-3B generated successfully!")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
