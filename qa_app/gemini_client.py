# qa_app/gemini_client.py
import google.generativeai as genai
from django.conf import settings

class GeminiClient:
    def __init__(self):
        api_key = settings.GEMINI_API_KEY
        self.api_key = api_key
        if not api_key or api_key == "AIzaSyD6AzqABIcG03KKonxiAYTEQjpE3G7okaU":
            raise ValueError("Invalid Gemini API key. Please set a valid key in your .env file.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def ask_question(self, document_content, question):
        prompt = f"""
        I have the following document content:
        
        {document_content}
        
        Based only on the information in the document above, please answer this question:
        {question}
        
        If the answer cannot be found in the document, please state "The answer is not in the provided document."
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Log detailed error information
            print(f"Gemini API error: {str(e)}")
            raise