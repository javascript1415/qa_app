from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Document, Question
from .forms import DocumentForm, QuestionForm
from .document_processor import DocumentProcessor
from .gemini_client import GeminiClient

def index(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            
          
            try:
                document.content = DocumentProcessor.extract_text(request.FILES['file'])
                print(document.content)
                document.save()
                return redirect('qa', document_id=document.id)
            except ValueError as e:
                messages.error(request, str(e))
    else:
        form = DocumentForm()
    foorm = Document.objects.all()
    
    return render(request, 'qa_app/index.html', {'form': form , 'foorm':foorm})

def qa(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    api_key = "AIzaSyD8ebSsbgZBgIWlATkNbjjt2Wfp4WdfKSg"  
    gemini_client = GeminiClient()
    
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.document = document
            
            # Get answer from Gemini
            try:
                question.answer_text = gemini_client.ask_question(document.content, question.question_text)
                question.save()
            except Exception as e:
                messages.error(request, f"Error getting answer: {str(e)}")
    else:
        form = QuestionForm()
    
    questions = document.questions.order_by('-asked_at')
    
    return render(request, 'qa_app/qa.html', {
        'document': document,
        'form': form,
        'questions': questions
    })

def delete(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    messages.success(request, "Document deleted successfully.")
    return redirect('index')
