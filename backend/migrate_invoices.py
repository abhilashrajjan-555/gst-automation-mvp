#!/usr/bin/env python3
"""
Migration Script: Recalculate Tax Amounts for Existing Invoices

This script updates all existing invoices to:
1. Calculate tax amounts from total_amount and gst_rate
2. Add invoice_type field for frontend compatibility
3. Add cgst_amount, sgst_amount, igst_amount fields
"""

import json
from pathlib import Path

def recalculate_invoice_tax(invoice_data):
    """Recalculate tax amounts for an invoice"""
    
    # Get values
    total_amount = invoice_data.get('total_amount', 0)
    gst_rate = invoice_data.get('gst_rate', 0)
    cgst = invoice_data.get('cgst', 0)
    sgst = invoice_data.get('sgst', 0)
    igst = invoice_data.get('igst', 0)
    
    # If no tax amounts but we have total and GST rate, calculate
    if (cgst == 0 and sgst == 0 and igst == 0 and total_amount > 0 and gst_rate > 0):
        # Calculate tax from total (assuming total includes tax)
        # Formula: Tax = Total × (GST% / (100 + GST%))
        total_tax = total_amount * (gst_rate / (100 + gst_rate))
        
        # For intra-state (CGST + SGST), split equally
        cgst = total_tax / 2
        sgst = total_tax / 2
        igst = 0
    
    # Update invoice data
    invoice_data['cgst'] = cgst
    invoice_data['sgst'] = sgst
    invoice_data['igst'] = igst
    invoice_data['cgst_amount'] = cgst
    invoice_data['sgst_amount'] = sgst
    invoice_data['igst_amount'] = igst
    
    # Add invoice_type if missing
    if 'invoice_type' not in invoice_data and 'type' in invoice_data:
        invoice_data['invoice_type'] = invoice_data['type']
        
    # Add reconciliation_status if missing
    if 'reconciliation_status' not in invoice_data:
        invoice_data['reconciliation_status'] = 'pending'
    
    return invoice_data

def main():
    """Migrate all invoices in the data directory"""
    
    # Get invoices directory
    data_dir = Path(__file__).parent / 'data' / 'invoices'
    
    if not data_dir.exists():
        print(f"❌ Invoices directory not found: {data_dir}")
        return
    
    # Process all invoice JSON files
    invoice_files = list(data_dir.glob('*.json'))
    
    if not invoice_files:
        print("ℹ️  No invoices found to migrate")
        return
    
    print(f"Found {len(invoice_files)} invoices to migrate\n")
    
    updated_count = 0
    
    for invoice_file in invoice_files:
        try:
            # Read invoice
            with open(invoice_file, 'r', encoding='utf-8') as f:
                invoice_data = json.load(f)
            
            # Store original state
            original_cgst = invoice_data.get('cgst', 0)
            original_sgst = invoice_data.get('sgst', 0)
            original_igst = invoice_data.get('igst', 0)
            has_cgst_amount = 'cgst_amount' in invoice_data
            has_recon_status = 'reconciliation_status' in invoice_data
            
            # Recalculate
            updated_data = recalculate_invoice_tax(invoice_data)
            
            # Check if anything changed
            if (updated_data['cgst'] != original_cgst or 
                updated_data['sgst'] != original_sgst or
                updated_data['igst'] != original_igst or
                not has_cgst_amount or
                not has_recon_status):
                
                # Save updated invoice
                with open(invoice_file, 'w', encoding='utf-8') as f:
                    json.dump(updated_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Updated: {invoice_file.name}")
                print(f"   Invoice #: {updated_data.get('invoice_number', 'N/A')}")
                print(f"   Total: ₹{updated_data.get('total_amount', 0):,.2f}")
                print(f"   Tax: ₹{(updated_data['cgst'] + updated_data['sgst'] + updated_data['igst']):,.2f}")
                print(f"   (CGST: ₹{updated_data['cgst']:,.2f}, SGST: ₹{updated_data['sgst']:,.2f})\n")
                
                updated_count += 1
            else:
                print(f"⏭️  Skipped: {invoice_file.name} (already up to date)")
        
        except Exception as e:
            print(f"❌ Error processing {invoice_file.name}: {str(e)}\n")
    
    print(f"\n{'='*60}")
    print(f"Migration complete!")
    print(f"Updated: {updated_count}/{len(invoice_files)} invoices")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
