"""
GSTR-3B Generator

Generates GSTR-3B (monthly summary return) from categorized invoices.
Calculates tax liability, input tax credit, and net tax payable.
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from collections import defaultdict


class GSTR3BGenerator:
    """Generate GSTR-3B monthly summary return"""

    def __init__(self, gstin: str):
        """
        Initialize GSTR-3B generator

        Args:
            gstin: User's GSTIN
        """
        self.gstin = gstin
        self.invoices = []

    def add_invoice(self, invoice_data: Dict):
        """
        Add a categorized invoice to be included in GSTR-3B

        Args:
            invoice_data: Categorized invoice dictionary
        """
        self.invoices.append(invoice_data)

    def load_invoices_from_directory(self, invoices_dir: str):
        """
        Load all invoice JSON files from a directory

        Args:
            invoices_dir: Path to directory containing invoice JSON files
        """
        invoices_path = Path(invoices_dir)

        if not invoices_path.exists():
            raise FileNotFoundError(f"Invoices directory not found: {invoices_dir}")

        json_files = list(invoices_path.glob('*.json'))

        for json_file in json_files:
            with open(json_file, 'r', encoding='utf-8') as f:
                invoice_data = json.load(f)
                self.add_invoice(invoice_data)

        print(f"✓ Loaded {len(self.invoices)} invoices")

    def generate(self, month: int, year: int) -> Dict:
        """
        Generate GSTR-3B for a specific month

        Args:
            month: Month number (1-12)
            year: Year (YYYY)

        Returns:
            GSTR-3B data structure as per GST portal format
        """
        # Filter invoices for the specified month
        month_invoices = self._filter_invoices_by_month(month, year)

        print(f"\nGenerating GSTR-3B for {month:02d}/{year}")
        print(f"Processing {len(month_invoices)} invoices...")

        # Separate sales and purchases
        sales_invoices = [inv for inv in month_invoices if inv.get('type') == 'sales']
        purchase_invoices = [inv for inv in month_invoices if inv.get('type') == 'purchase']

        print(f"  Sales: {len(sales_invoices)} invoices")
        print(f"  Purchases: {len(purchase_invoices)} invoices")

        # Calculate components
        table_3_1 = self._calculate_table_3_1(sales_invoices)
        table_3_2 = self._calculate_table_3_2(sales_invoices)
        table_4 = self._calculate_table_4(purchase_invoices)
        table_5 = self._calculate_table_5(sales_invoices, purchase_invoices)

        # Build GSTR-3B structure (table_6 calculated after)
        gstr3b = {
            'gstin': self.gstin,
            'ret_period': f"{month:02d}{year}",
            'filing_date': None,  # To be filled when actually filing
            'generated_at': datetime.now().isoformat(),

            # Table 3.1: Outward taxable supplies
            'table_3_1': table_3_1,

            # Table 3.2: Out of the supplies shown in 3.1(a)
            'table_3_2': table_3_2,

            # Table 4: Eligible ITC
            'table_4': table_4,

            # Table 5: Values of exempt, nil-rated and non-GST
            'table_5': table_5,

            # Table 6: Payment of tax (placeholder, calculated below)
            'table_6': {},

            # Summary
            'summary': {
                'total_sales': table_3_1['total_taxable_value'],
                'total_tax_on_sales': table_3_1['total_tax'],
                'total_purchases': table_4['total_itc'],
                'net_tax_liability': 0
            }
        }

        # Calculate actual net tax for table 6
        net_tax = self.calculate_net_tax(gstr3b)
        gstr3b['table_6'] = net_tax
        gstr3b['summary']['net_tax_liability'] = net_tax['total_tax_payable']

        return gstr3b

    def _filter_invoices_by_month(self, month: int, year: int) -> List[Dict]:
        """Filter invoices for specific month/year"""
        filtered = []

        for invoice in self.invoices:
            invoice_date = invoice.get('invoice_date')

            if not invoice_date:
                continue

            # Parse date (assumes YYYY-MM-DD format)
            try:
                date_parts = invoice_date.split('-')
                inv_year = int(date_parts[0])
                inv_month = int(date_parts[1])

                if inv_year == year and inv_month == month:
                    filtered.append(invoice)

            except (ValueError, IndexError):
                print(f"⚠️  Invalid date format: {invoice_date}")
                continue

        return filtered

    def _calculate_table_3_1(self, sales_invoices: List[Dict]) -> Dict:
        """
        Calculate Table 3.1: Outward taxable supplies (sales)

        Returns taxable value and tax amount by supply type
        """
        # Aggregate sales by type
        intra_state = {'taxable_value': 0, 'igst': 0, 'cgst': 0, 'sgst': 0, 'cess': 0}
        inter_state = {'taxable_value': 0, 'igst': 0, 'cgst': 0, 'sgst': 0, 'cess': 0}

        for invoice in sales_invoices:
            # Determine if intra-state or inter-state
            # Intra-state: CGST+SGST, Inter-state: IGST
            is_inter_state = invoice.get('igst', 0) > 0

            # Calculate taxable value (total - GST)
            total = invoice.get('total_amount', 0)
            gst_amount = invoice.get('cgst', 0) + invoice.get('sgst', 0) + invoice.get('igst', 0)
            taxable_value = total - gst_amount

            if is_inter_state:
                inter_state['taxable_value'] += taxable_value
                inter_state['igst'] += invoice.get('igst', 0)
            else:
                intra_state['taxable_value'] += taxable_value
                intra_state['cgst'] += invoice.get('cgst', 0)
                intra_state['sgst'] += invoice.get('sgst', 0)

        total_taxable_value = intra_state['taxable_value'] + inter_state['taxable_value']
        total_tax = (intra_state['cgst'] + intra_state['sgst'] + intra_state['igst'] +
                    inter_state['igst'])

        return {
            'intra_state_supplies': intra_state,
            'inter_state_supplies': inter_state,
            'total_taxable_value': round(total_taxable_value, 2),
            'total_tax': round(total_tax, 2)
        }

    def _calculate_table_3_2(self, sales_invoices: List[Dict]) -> Dict:
        """
        Calculate Table 3.2: Out of the supplies shown in 3.1(a)

        Details like zero-rated supplies, exports, etc.
        """
        # For MVP, returning simplified structure
        # In production, this would track exports, SEZ, deemed exports
        return {
            'zero_rated_supplies': 0,
            'exports': 0,
            'supplies_to_sez': 0,
            'deemed_exports': 0
        }

    def _calculate_table_4(self, purchase_invoices: List[Dict]) -> Dict:
        """
        Calculate Table 4: Eligible Input Tax Credit (ITC)

        ITC available from purchases
        """
        # Aggregate ITC by type
        itc_on_imports = 0
        itc_on_capital_goods = 0
        itc_on_inputs = 0
        itc_on_input_services = 0

        total_itc = 0

        for invoice in purchase_invoices:
            # Check if ITC is eligible
            if not invoice.get('itc_eligible', True):
                continue

            # Calculate ITC (CGST + SGST + IGST)
            itc_amount = (invoice.get('cgst', 0) +
                         invoice.get('sgst', 0) +
                         invoice.get('igst', 0))

            # For MVP, classify all as inputs (can be refined later)
            itc_on_inputs += itc_amount
            total_itc += itc_amount

        return {
            'itc_on_imports': round(itc_on_imports, 2),
            'itc_on_capital_goods': round(itc_on_capital_goods, 2),
            'itc_on_inputs': round(itc_on_inputs, 2),
            'itc_on_input_services': round(itc_on_input_services, 2),
            'total_itc': round(total_itc, 2)
        }

    def _calculate_table_5(self, sales_invoices: List[Dict],
                          purchase_invoices: List[Dict]) -> Dict:
        """
        Calculate Table 5: Values of exempt, nil-rated and non-GST supplies

        Supplies on which no GST is charged
        """
        exempt_sales = 0
        nil_rated_sales = 0
        non_gst_sales = 0

        for invoice in sales_invoices:
            # Check if GST rate is 0%
            if invoice.get('gst_rate', 18) == 0:
                nil_rated_sales += invoice.get('total_amount', 0)

        return {
            'exempt_supplies': round(exempt_sales, 2),
            'nil_rated_supplies': round(nil_rated_sales, 2),
            'non_gst_supplies': round(non_gst_sales, 2)
        }

    def calculate_net_tax(self, gstr3b_data: Dict) -> Dict:
        """
        Calculate net tax liability

        Args:
            gstr3b_data: Generated GSTR-3B data

        Returns:
            Net tax breakdown by type
        """
        # Extract data
        table_3_1 = gstr3b_data['table_3_1']
        table_4 = gstr3b_data['table_4']

        # Calculate output tax
        output_igst = table_3_1['inter_state_supplies']['igst']
        output_cgst = table_3_1['intra_state_supplies']['cgst']
        output_sgst = table_3_1['intra_state_supplies']['sgst']

        # Input tax credit
        total_itc = table_4['total_itc']

        # Net tax (simplified - in reality ITC adjustment is more complex)
        # First adjust IGST, then CGST, then SGST
        remaining_itc = total_itc

        # Adjust IGST
        igst_payable = max(0, output_igst - remaining_itc)
        remaining_itc = max(0, remaining_itc - output_igst)

        # Adjust CGST
        cgst_payable = max(0, output_cgst - remaining_itc / 2)
        remaining_itc = max(0, remaining_itc - output_cgst * 2)

        # Adjust SGST
        sgst_payable = max(0, output_sgst - remaining_itc / 2)

        total_tax_payable = igst_payable + cgst_payable + sgst_payable

        return {
            'igst_payable': round(igst_payable, 2),
            'cgst_payable': round(cgst_payable, 2),
            'sgst_payable': round(sgst_payable, 2),
            'cess_payable': 0,
            'total_tax_payable': round(total_tax_payable, 2)
        }

    def save_to_file(self, gstr3b_data: Dict, output_path: str):
        """
        Save GSTR-3B to JSON file

        Args:
            gstr3b_data: Generated GSTR-3B data
            output_path: Path to save JSON file
        """
        # Calculate net tax
        net_tax = self.calculate_net_tax(gstr3b_data)

        # Update table 6
        gstr3b_data['table_6'] = net_tax
        gstr3b_data['summary']['net_tax_liability'] = net_tax['total_tax_payable']

        # Save to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(gstr3b_data, f, indent=2, ensure_ascii=False)

        print(f"\n✓ GSTR-3B saved to: {output_path}")

    def print_summary(self, gstr3b_data: Dict):
        """Print human-readable summary of GSTR-3B"""
        print("\n" + "=" * 60)
        print("GSTR-3B SUMMARY")
        print("=" * 60)

        print(f"\nGSTIN: {gstr3b_data['gstin']}")
        print(f"Return Period: {gstr3b_data['ret_period']}")

        summary = gstr3b_data['summary']

        print(f"\nOUTWARD SUPPLIES (Sales)")
        print(f"  Total Taxable Value: ₹{summary['total_sales']:,.2f}")
        print(f"  Total Tax Collected: ₹{summary['total_tax_on_sales']:,.2f}")

        print(f"\nINPUT TAX CREDIT (Purchases)")
        print(f"  Total ITC Available: ₹{summary['total_purchases']:,.2f}")

        print(f"\nNET TAX LIABILITY")
        print(f"  Tax to Pay: ₹{summary['net_tax_liability']:,.2f}")

        table_6 = gstr3b_data['table_6']
        print(f"\n  Breakdown:")
        print(f"    IGST: ₹{table_6['igst_payable']:,.2f}")
        print(f"    CGST: ₹{table_6['cgst_payable']:,.2f}")
        print(f"    SGST: ₹{table_6['sgst_payable']:,.2f}")

        print("\n" + "=" * 60)


# CLI for testing
if __name__ == '__main__':
    import sys

    print("GSTR-3B Generator - Testing")
    print("=" * 60)

    # Example usage
    gstin = "27AABCT1234A1Z5"  # Example GSTIN

    generator = GSTR3BGenerator(gstin)

    # Add sample invoices for testing
    sample_sales = {
        'type': 'sales',
        'invoice_date': '2024-12-15',
        'total_amount': 59000,
        'cgst': 4500,
        'sgst': 4500,
        'igst': 0,
        'gst_rate': 18
    }

    sample_purchase = {
        'type': 'purchase',
        'invoice_date': '2024-12-10',
        'total_amount': 11800,
        'cgst': 900,
        'sgst': 900,
        'igst': 0,
        'gst_rate': 18,
        'itc_eligible': True
    }

    generator.add_invoice(sample_sales)
    generator.add_invoice(sample_purchase)

    # Generate GSTR-3B
    gstr3b = generator.generate(month=12, year=2024)

    # Print summary
    generator.print_summary(gstr3b)

    # Save to file
    output_file = '../data/gstr3b_sample.json'
    generator.save_to_file(gstr3b, output_file)

    print(f"\n✓ Test completed successfully!")
    print(f"📄 Check the generated file: {output_file}")
