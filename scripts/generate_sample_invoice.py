from PIL import Image, ImageDraw, ImageFont
import os

def create_invoice_image():
    # Create white image
    img = Image.new('RGB', (800, 1000), color='white')
    d = ImageDraw.Draw(img)
    
    # Try to load a font, otherwise use default
    try:
        # Mac standard font
        font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
        font_medium = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
        font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 12)
    except:
        # Fallback if specific font not found
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw text
    # Header
    d.text((50, 50), "TAX INVOICE", fill="black", font=font_large)
    d.text((50, 100), "Vendor: Tech Solutions Pvt Ltd", fill="black", font=font_medium)
    d.text((50, 130), "GSTIN: 29AABCT1234A1Z5", fill="black", font=font_medium)
    d.text((50, 160), "Address: 123 Tech Park, Bangalore, 560001", fill="black", font=font_small)

    # Invoice Details
    d.text((500, 100), "Invoice No: INV-2024-001", fill="black", font=font_medium)
    d.text((500, 130), "Date: 01-12-2024", fill="black", font=font_medium)

    # Line Items Header
    y = 250
    d.line((50, y, 750, y), fill="black", width=2)
    d.text((50, y+10), "Description", fill="black", font=font_medium)
    d.text((400, y+10), "HSN", fill="black", font=font_medium)
    d.text((500, y+10), "Qty", fill="black", font=font_medium)
    d.text((600, y+10), "Rate", fill="black", font=font_medium)
    d.text((700, y+10), "Amount", fill="black", font=font_medium)
    d.line((50, y+40, 750, y+40), fill="black", width=2)

    # Item 1
    y += 60
    d.text((50, y), "Laptop Dell Inspiron 15", fill="black", font=font_medium)
    d.text((400, y), "8471", fill="black", font=font_medium)
    d.text((500, y), "1", fill="black", font=font_medium)
    d.text((600, y), "50000", fill="black", font=font_medium)
    d.text((700, y), "50000", fill="black", font=font_medium)

    # Totals
    y += 100
    d.line((400, y, 750, y), fill="black", width=1)
    d.text((500, y+20), "Subtotal:", fill="black", font=font_medium)
    d.text((700, y+20), "50000", fill="black", font=font_medium)
    
    d.text((500, y+50), "CGST (9%):", fill="black", font=font_medium)
    d.text((700, y+50), "4500", fill="black", font=font_medium)
    
    d.text((500, y+80), "SGST (9%):", fill="black", font=font_medium)
    d.text((700, y+80), "4500", fill="black", font=font_medium)
    
    d.line((400, y+120, 750, y+120), fill="black", width=2)
    d.text((500, y+130), "Total:", fill="black", font=font_large)
    d.text((700, y+130), "59000", fill="black", font=font_large)

    # Ensure directory exists
    os.makedirs("backend/test_invoices", exist_ok=True)
    
    # Save
    output_path = "backend/test_invoices/sample_invoice_generated.png"
    img.save(output_path)
    print(f"Created invoice at {output_path}")

if __name__ == "__main__":
    create_invoice_image()
