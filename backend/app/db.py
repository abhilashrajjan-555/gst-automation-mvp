import os
from typing import Dict, List, Optional
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    """
    Supabase Database Handler
    
    Manages connection and operations with Supabase PostgreSQL database.
    """
    
    def __init__(self):
        self.url: str = os.environ.get("SUPABASE_URL")
        self.key: str = os.environ.get("SUPABASE_KEY")
        self.client: Optional[Client] = None
        
        if self.url and self.key:
            try:
                self.client = create_client(self.url, self.key)
                print("✓ Connected to Supabase")
            except Exception as e:
                print(f"❌ Failed to connect to Supabase: {str(e)}")
        else:
            print("⚠️  Supabase credentials not found. Running in local-only mode (JSON storage).")

    def is_connected(self) -> bool:
        """Check if connected to Supabase"""
        return self.client is not None

    def save_invoice(self, invoice_data: Dict, user_id: Optional[str] = None) -> Dict:
        """
        Save invoice to Supabase 'invoices' table
        """
        if not self.client:
            return {"error": "Database not connected"}

        try:
            # Prepare payload for 'invoices' table
            # Note: We need to map the JSON structure to our SQL columns
            payload = {
                "id": invoice_data.get("invoice_id"),
                "user_id": user_id,  # Can be None for now
                "file_path": invoice_data.get("original_file", ""),
                "file_name": os.path.basename(invoice_data.get("original_file", "")),
                "invoice_number": invoice_data.get("invoice_number"),
                "invoice_date": invoice_data.get("invoice_date"),
                "invoice_type": invoice_data.get("type"),
                "vendor_gstin": invoice_data.get("vendor_gstin"),
                "total_amount": invoice_data.get("total_amount"),
                "cgst_amount": invoice_data.get("cgst"),
                "sgst_amount": invoice_data.get("sgst"),
                "igst_amount": invoice_data.get("igst"),
                "gst_rate": invoice_data.get("gst_rate"),
                "ocr_confidence": invoice_data.get("ocr_confidence"),
                "status": "processed"
            }

            # Insert into invoices table
            data, count = self.client.table("invoices").insert(payload).execute()
            
            # If successful, insert line items
            if invoice_data.get("line_items"):
                items_payload = []
                for item in invoice_data["line_items"]:
                    items_payload.append({
                        "invoice_id": invoice_data.get("invoice_id"),
                        "description": item.get("description"),
                        "hsn_code": item.get("hsn_code"),
                        "quantity": item.get("quantity", 1),
                        "rate": item.get("rate"),
                        "amount": item.get("amount"),
                        "gst_rate": item.get("gst_rate"),
                        "confidence_score": item.get("confidence")
                    })
                
                self.client.table("invoice_items").insert(items_payload).execute()

            return {"success": True, "data": data}

        except Exception as e:
            print(f"❌ Database Error: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_invoices(self, user_id: Optional[str] = None) -> List[Dict]:
        """Fetch invoices from Supabase"""
        if not self.client:
            return []

        try:
            query = self.client.table("invoices").select("*")
            if user_id:
                query = query.eq("user_id", user_id)
            
            response = query.order("created_at", desc=True).execute()
            return response.data
        except Exception as e:
            print(f"❌ Database Fetch Error: {str(e)}")
            return []

# Singleton instance
db = Database()
