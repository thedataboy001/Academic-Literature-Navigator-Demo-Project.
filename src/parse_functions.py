import warnings
warnings.filterwarnings("ignore")

import requests

from src.helper_functions import tei_to_text

# -------------- GROBID PDF PARSING --------------

GROBID_URL = "http://localhost:8070/api/processFulltextDocument"

def parse_pdf_with_grobid(pdf_path):
    with open(pdf_path, "rb") as f:
        files = {"input": f}
        response = requests.post(
            GROBID_URL,
            files=files,
            data={"consolidateHeader": "1"}
        )

    response.raise_for_status()
    return response.text  # TEI XML

# -------------- MAIN APP LOGIC --------------

def process_pdf_to_text(pdf_path):
    tei_xml = parse_pdf_with_grobid(pdf_path)
    plain_text = tei_to_text(tei_xml)
    return plain_text

if __name__ == "__main__":
    pdf_path = "../papers/optimizing-renewable-energy-systems-through-artificial-intelligence-review-and-future-prospects.pdf"
    text_content = process_pdf_to_text(pdf_path)
    print(text_content)