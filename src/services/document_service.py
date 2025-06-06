import PyPDF2
import docx
from bs4 import BeautifulSoup
import requests
from io import BytesIO

class DocumentService:
    async def process_resume(self, file) -> str:
        """Extract text from uploaded resume file."""
        content = await file.read()
        
        if file.filename.endswith('.pdf'):
            return self._extract_from_pdf(content)
        elif file.filename.endswith('.docx'):
            return self._extract_from_docx(content)
        else:
            raise ValueError("Unsupported file format")
    
    def _extract_from_pdf(self, content: bytes) -> str:
        pdf_file = BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    
    def _extract_from_docx(self, content: bytes) -> str:
        docx_file = BytesIO(content)
        doc = docx.Document(docx_file)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])
    
    async def extract_job_description(self, url: str) -> str:
        """Extract job description from URL."""
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text 