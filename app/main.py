import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
from typing import List

from clustered_summary import ClusteredSummary
from pdf_document import PdfDocument
from summary import Summary
from utils import count_tokens
from validator import Validator
from datetime import datetime

def main():
    st.title("Path to Publishing")

    input_method = "Upload documents"

    if input_method == "Upload documents":
        uploaded_files = st.file_uploader(
            "Upload documents",
            type=["pdf"],
            accept_multiple_files=True,
        )

    export_to_docx = st.checkbox("Export summary to a Word document")    

    st.sidebar.markdown("# [Contact me by email!](mailto:tsterite@gmail.com)")
    st.sidebar.markdown(
        "# [Check out my other projects!](https://github.com/Tina-Sterite)"
    )

    if st.button("Generate"):
        if input_method == "Upload documents":
            if uploaded_files is None:
                st.warning("Please upload a file.")
                return
            summarize_files(uploaded_files, export_to_docx)

def summarize_files(uploaded_files: List[UploadedFile], export_to_docx: bool):
    documents = [PdfDocument(file) for file in uploaded_files]
    text_contents = [doc.text_content for doc in documents]
    combined_text = "\n".join(text_contents)
    validation_errors = Validator.validate_text(combined_text)

    if validation_errors:
        st.warning(f"Invalid input: {','.join(validation_errors)}")
        return

    #st.markdown(run_summary(combined_text, f"documents"), unsafe_allow_html=True)
    summary = run_summary(combined_text)
    st.markdown(summary, unsafe_allow_html=True)
   
    if export_to_docx:
        # Generate the timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        Summary(combined_text).export_to_docx(summary, f"p2p_{timestamp}.docx")

def run_summary(combined_text: str):
    tokens = count_tokens(combined_text)

    if tokens > 100_000:
        return ClusteredSummary(combined_text).get_summary()
    else:
        return Summary(combined_text).get_summary()


if __name__ == "__main__":
    main()
