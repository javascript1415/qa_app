import docx
import PyPDF2
import io

class DocumentProcessor:
    @staticmethod
    def extract_text(file):
        file_name = file.name.lower()
        file_content = file.read()
        
        if file_name.endswith('.txt'):
            # For text files, decode the content
            return file_content.decode('utf-8')
            
        elif file_name.endswith('.docx'):
            # For Word documents
            doc = docx.Document(io.BytesIO(file_content))
            return '\n'.join([para.text for para in doc.paragraphs])
            
        elif file_name.endswith('.pdf'):
            # For PDF files
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ''
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
            
        else:
            raise ValueError("Unsupported file format. Please upload .txt, .docx, or .pdf files.")
