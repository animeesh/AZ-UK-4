import base64
import tempfile

import streamlit as st
from pdf2image import convert_from_path
import json
import pandas as pd
from pathlib import Path
from utils import extract_and_append_to_csv, extract_from_pdf

def show_pdf(file_path:str):
    """Show the PDF in Streamlit
    That returns as html component

    Parameters
    ----------
    file_path : [str]
        Uploaded PDF file path
    """

    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)


def main():
    """Streamlit application
    """

    st.title("Pet plan claim form analyzer")
    uploaded_file = st.file_uploader("Choose your .pdf file", type="pdf")

    if uploaded_file is not None:
        # Make temp file path from uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            st.markdown("## Original PDF file")
            fp = Path(tmp_file.name)
            fp.write_bytes(uploaded_file.getvalue())
            st.write(show_pdf(tmp_file.name))
            #imgs = convert_from_path(tmp_file.name)
            st.markdown(f"Converted images from PDF")

            pdf_path = tmp_file.name
            case3_dict = {
                "policy holder full_name": " ",
                "claim_paid_by": " ",
                "email": " ",
                "pet_name": " ",
                "breed": " ",
                "reference_letter_number": " "
            }
            pdf_text = ""
            case3_prompt = (
                f"Extract the following fields from the PDF content below and fill in this dictionary:\n"
                f"{case3_dict}\n\n"
                f"PDF content:\n{pdf_text}"
                f"give the response in the JSON format as shown in the template.\n"
            )
            st.write(extract_from_pdf(pdf_path,case3_prompt) or "No data extracted from PDF")


    st.title("Pet plan claim updater to csv")
    print("--------------------------END OF CASE 1--------------------------")
    csv_uploaded_file = st.file_uploader("Choose your invoice file", type="pdf")

    if csv_uploaded_file is not None:
        # Make temp file path from uploaded file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            st.markdown("## Original PDF file")
            fp = Path(tmp_file.name)
            fp.write_bytes(csv_uploaded_file.getvalue())
            st.write(show_pdf(tmp_file.name))

            imgs = convert_from_path(tmp_file.name)

            st.markdown(f"Converted images from PDF")
            pdf_path = tmp_file.name
            case2_dict = {
                "total_amount": " ",
                "invoice_date": " ",
                "session": " ",
            }
            pdf_text = ""
            case2_prompt = (
                f"Extract the following fields from the PDF content below and fill in this dictionary:\n"
                f"Note: session refers to the specific session of the invoice or small consolidated session of any rows.\n"
                f"{case2_dict}\n\n"
                f"PDF content:\n{pdf_text}"
                f"give the response in the JSON format as shown in the template.\n"
            )
            #st.write(extract_from_pdf(pdf_path,case2_prompt) or "No data extracted from PDF")

            case2_extraction=extract_from_pdf(pdf_path,case2_prompt) 
            #json_str = json.dumps(case2_extraction, indent=4)
            # case2_extraction = case2_extraction.replace("'", "\"")
            # data_dict = json.loads(case2_extraction)
            # #print(data_dict)
            # print(type(data_dict))
            #print(case2_extraction)
            extract_and_append_to_csv(case2_extraction, csv_file="test.csv")
            spectra_df = pd.read_csv("test.csv")
            st.write(spectra_df.tail(5))


if __name__ == "__main__":
    main()  