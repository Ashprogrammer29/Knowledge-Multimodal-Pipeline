import os
import fitz  # PyMuPDF
from docx import Document
import logging


class InputAbstractionLayer:
    """
    Handles multiple formats and implements semantic chunking for large files.
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.extension = os.path.splitext(file_path)[1].lower()
        self.extension = os.path.splitext(file_path)[1].lower()

    def extract_text(self):
        if self.extension == '.txt':
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        elif self.extension == '.pdf':
            text = ""
            with fitz.open(self.file_path) as doc:
                for page in doc:
                    text += page.get_text()
            return text
        elif self.extension == '.docx':
            doc = Document(self.file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            raise ValueError(f"Unsupported format: {self.extension}")

    def get_chunks(self, text, chunk_size=2000):
        """
        Splits 50,000+ words into manageable pieces for offline NLP models.
        """
        words = text.split()
        for i in range(0, len(words), chunk_size):
            yield " ".join(words[i:i + chunk_size])


# Quick Test Logic
if __name__ == "__main__":
    # Create a dummy test file or point to a real one
    # ial = InputAbstractionLayer("test_book.pdf")
    # full_text = ial.extract_text()
    # print(f"Extracted {len(full_text.split())} words.")
    pass