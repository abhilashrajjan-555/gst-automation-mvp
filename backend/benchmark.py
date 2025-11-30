import time
import sys
from pathlib import Path
from app.processor import InvoiceProcessor

def benchmark_processing(file_path):
    print(f"🚀 Benchmarking processing for: {file_path}")
    
    processor = InvoiceProcessor()
    
    # 1. PDF to Image Conversion (if PDF)
    start_time = time.time()
    if file_path.endswith('.pdf'):
        print("Step 1: Converting PDF to Image...", end='', flush=True)
        # We can't easily isolate this without modifying code, but we can infer
        pass
    
    # 2. Full Processing
    print("\nStarting full processing...")
    start_total = time.time()
    
    result = processor.process_invoice(file_path, invoice_type='purchase', auto_confirm=True)
    
    end_total = time.time()
    duration = end_total - start_total
    
    print(f"\n{'='*40}")
    print(f"⏱️  Total Time: {duration:.2f} seconds")
    print(f"{'='*40}")
    
    if duration > 5.0:
        print("⚠️  Processing is SLOW (> 5s)")
    else:
        print("✅ Processing is FAST (< 5s)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 benchmark.py <invoice_file>")
        sys.exit(1)
        
    benchmark_processing(sys.argv[1])
