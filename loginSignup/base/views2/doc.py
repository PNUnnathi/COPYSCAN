from datetime import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

from base.forms import TextForm

# views.py
from django.urls import reverse
from xml.dom.minidom import Document
from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from base.forms import TextForm, FileUploadForm
from django.http import HttpResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader
import requests
from docx import Document
from django.template.loader import get_template
import io
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login
from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.html import escape
from base.utils import highlight_plagiarized_content
from base.models.useractivity import UserActivity
from base.models.customer import Customer

import urllib.parse


API_KEY = 'AIzaSyAzVIn1Z6yzRKrwon26f-JP-5_BoWR8jok'
SEARCH_ENGINE_ID = 'a57946bf7faf24ae1'

def extract_text_from_docx(uploaded_file):
    try:
        content = uploaded_file.read()
        doc = Document(io.BytesIO(content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""



def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""

def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                if uploaded_file.name.endswith(('.doc', '.docx')):
                    text = extract_text_from_docx(uploaded_file)
                elif uploaded_file.name.endswith('.pdf'):
                    text = extract_text_from_pdf(uploaded_file)
                else:
                    # Handle other file types or show an error message
                    return render(request, 'doc.html', {'form': form, 'error_message': 'Unsupported file format'})

                search_results = search_google(uploaded_file.name)
                similarity_results = []
                for result in search_results:
                    text2 = result.get('snippet', '')
                    similarity = calculate_similarity(text, text2)
                    similarity_results.append({'result': result, 'similarity': similarity})

                return render(request, 'results.html', {'input_text': text, 'search_results': similarity_results})

    else:
        form = FileUploadForm()

    return render(request, 'doc.html', {'form': form})
def search_google(query):
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        results = response.json()
        print(results)  # Print the entire JSON response
        return results.get('items', [])
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
    return []

def calculate_similarity(text1, text2):
    if text1 == text2:
        return 100.0
    else:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        similarity = cosine_sim[0][1]
        return round(similarity * 100, 2)