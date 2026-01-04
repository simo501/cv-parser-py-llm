import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

input_dir = "ready pdfs"
output_dir = "ready text"
os.makedirs(output_dir, exist_ok=True)

def convert_pdf(filename):
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
    
    try:
        # capture_output=True cattura gli errori di pdftotext
        result = subprocess.run(["pdftotext", input_path, output_path], 
                                capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Errore su {filename}: {result.stderr.strip()}")
    except Exception as e:
        print(f"Errore di sistema su {filename}: {e}")

if __name__ == "__main__":
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
    
    with ProcessPoolExecutor(max_workers=8) as executor:
        executor.map(convert_pdf, files)
