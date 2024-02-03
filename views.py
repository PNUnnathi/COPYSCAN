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


API_KEY = 'AIzaSyAzVIn1Z6yzRKrwon26f-JP-5_BoWR8jok'
SEARCH_ENGINE_ID = 'a57946bf7faf24ae1'


class TextInputView(View):
    template_name = 'text.html'

    def get(self, request):
        form = TextForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TextForm(request.POST)

        if form.is_valid():
            text1 = form.cleaned_data['text']
        
            # Perform the Google search
            search_results = search_google(text1)
            similarity_results = []

            # Calculate similarity for each result
            for result in search_results:
                text2 = result.get('snippet', '')
                similarity = calculate_similarity(text1, text2)
                highlighted_snippet = highlight_plagiarized_content(text1, text2)
                similarity_results.append({'result': result, 'similarity': similarity, 'highlighted_snippet': highlighted_snippet})
              
            if 'customer' in request.session:
            # Retrieve the customer ID from the session
                customer_id = request.session['customer']
                
                # Use the customer ID to get the Customer object
                logged_in_customer = Customer.objects.get(id=customer_id)
                UserActivity.save_text(user=logged_in_customer, input_text=text1,search_res=search_results)

            request.session['paraphrase_input_text'] = text1
            return render(request, 'results.html', {'input_text': text1, 'search_results': similarity_results})

        return render(request, self.template_name, {'form': form})
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
                if uploaded_file.name.endswith('.pdf'):
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    search_results = search_google(pdf_text)
                    similarity_results = []
                    for result in search_results:
                        text2 = result.get('snippet', '')
                        similarity = calculate_similarity(pdf_text, text2)
                        similarity_results.append({'result': result, 'similarity': similarity})
                    return render(request, 'base/results.html', {'input_text': pdf_text, 'search_results': similarity_results})
                elif uploaded_file.name.endswith(('.doc', '.docx')):
                    doc_text = extract_text_from_docx(uploaded_file)
                    search_results = search_google(doc_text)
                    similarity_results = []
                    for result in search_results:
                        text2 = result.get('snippet', '')
                        similarity = calculate_similarity(doc_text, text2)
                        similarity_results.append({'result': result, 'similarity': similarity})
                    return render(request, 'results.html', {'input_text': doc_text, 'search_results': similarity_results})
                
                else:
                    # Handle other file types or show an error message
                    pass
    else:
        form = FileUploadForm()

    return render(request, 'doc.html', {'form': form})

def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    similarity = cosine_sim[0][1]
    return round(similarity * 100, 2)

def search_google(query):
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'q': query,
    }

    response = requests.get(url, params=params)
    results = response.json()
    return results.get('items', [])


def home(request):
 return render(request, "home.html", {})


def text_page(request):
  # Adjust the URL name for your login view

    return render(request, 'text.html')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class TextSaveView(View):


    def get(self , request ):
        
        customer = request.session.get('customer')
        texts = UserActivity.get_text_by_customer(customer)
        print(texts)
        return render(request , 'results.html'  , {'texts' :texts})