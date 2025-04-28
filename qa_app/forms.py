from django import forms
from .models import Document, Question

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        labels = {
            'question_text': 'Ask a question about the document',
        }
        widgets = {
            'question_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'What would you like to know?'}),
        }
