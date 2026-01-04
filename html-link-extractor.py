from bs4 import BeautifulSoup
import argparse

def extract_links(input_path, output_path):
    with open(input_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    links = [a["href"] for a in soup.find_all("a", title="Curriculum vitae")]

    with open(output_path, "w") as f:
        f.write("\n".join(links))
    print(f"Estratti {len(links)} link.")
            
parser = argparse.ArgumentParser(description="Parser CV Elezioni 2022")
parser.add_argument("-i", "--input-html", help="File HTML sorgente", required=True)
parser.add_argument("-o", "--output-links", help="File TXT per link estratti", required=True)
# parser.add_argument("-ipl", "--input-links", help="File TXT con link da scaricare")
args = parser.parse_args()  

extract_links(args.input_html, args.output_links)
