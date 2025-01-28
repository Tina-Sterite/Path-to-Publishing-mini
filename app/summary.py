from magic import Magician
import os
from docx import Document
from datetime import datetime
from bs4 import BeautifulSoup

class Summary(Magician):

    SUMMARIZE_SYSTEM_MESSAGE = """
    You will be given a complete %s. It will be enclosed in triple backticks.
    Please provide a comprehensive, thoughtful, and cohesive personal brand statement and unique value proposition using the %s, 
    do not use "I" statements.
    Additionally, with these crafted statements and the %s, provide the candidate with 10 LinkedIn posts that the candidate should 
    post to engage their audience (leaders and colleagues in their line of work and industry), these posts should be 
    thought-provoking and engage the candidate's professional community. Include a strong hook, clear content, call to
    action, and relevant hashtags. Use storytelling and address the audience's interests and challenges. Vary post 
    types among questions, statements, facts, and polls.  Do not include emoticons, emojis, or icons in the statements or posts.

    Format these statements in HTML. It should be structured as follows:

    - Personal Brand Statement.
    - Unique Value Proposition.
    - The suggested LinkedIn posts.
    
    Format for maximum readability and clarity.
    """

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text
        self.media_type = "documents"

    def get_summary(self) -> str:

        system_message = self.SUMMARIZE_SYSTEM_MESSAGE % (
            self.media_type,
            self.media_type,
            self.media_type
        )
        user_message = f"'''{self.text}'''"
        full_summary = self.wave_wand(system_message, user_message)

        return self.extract_code(full_summary)
    
    def export_to_docx(self, summary: str, file_name: str):
        # Strip Markdown formatting
        new_summary = summary.replace("<h1>", "\n").replace("</h1>", "\n").replace("</strong>", "\n").replace("</p>", "\n").replace("<li>","\n\n")
        soup = BeautifulSoup(new_summary, "html.parser")
        text = soup.get_text()
        
        # def format_text(text: str) -> str:
        #     # Example formatting: Add a title and separate sections with new lines
        #     formatted_text = "Path to Publishing" + text.replace("\n", "\r\n\r\n")
        #     return formatted_text

        # formatted_summary = format_text(summary)
        
        doc = Document()
        doc.add_paragraph(text)

        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir)

        # Generate the timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        docx_output_path = os.path.join(downloads_dir, f"p2p_{timestamp}.docx")
        doc.save(docx_output_path)