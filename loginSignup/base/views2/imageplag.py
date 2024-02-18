import io
import json
import os
from bs4 import BeautifulSoup
from django.http import HttpResponse
import requests
from django.shortcuts import render
from PIL import Image, UnidentifiedImageError
import imagehash
from base.forms import FileUploadForm
from django.core.files.uploadedfile import InMemoryUploadedFile

API_KEY = 'AIzaSyAzVIn1Z6yzRKrwon26f-JP-5_BoWR8jok'
SEARCH_ENGINE_ID = 'a57946bf7faf24ae1'

def image_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                if uploaded_file.name.lower().endswith(('.jpg', '.png', '.avif')):
                    img1 = Image.open(uploaded_file)

                    # Step 1: Search Google for the user-uploaded image
                    search_results = search_google(uploaded_file.name)

                    similarity_results = []

                    for result in search_results:
                        img2_url = result.get('link', '')

                        # Step 2: Scrape images from the website related to the Google result
                        website_images = scrape_website_images(img2_url)

                        for website_image_url in website_images:
                            # Step 3: Compare similarity between the user-uploaded image and each website image
                            similarity = image_similarity(img1, website_image_url)
                            
                            # Step 4: Display results
                            similarity_results.append({'result': result, 'website_image': website_image_url, 'similarity': similarity})

                    return render(request, 'results2.html', {'search_results': similarity_results})

                else:
                    # Handle other file types or show an error message
                    return render(request, 'image.html', {'form': form, 'error_message': 'Unsupported file format'})

    else:
        form = FileUploadForm()

    return render(request, 'image.html', {'form': form})

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


def scrape_website_images(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract unique image URLs from the website content
        images = set(img['src'].strip() for img in soup.find_all('img', src=True))

        return list(images)
    except requests.exceptions.RequestException as e:
        print(f"Error scraping website: {e}")
        return []
def image_similarity(image1, image2_url):
    try:
        # Convert the first image to 'RGB' mode if it's not already
        if isinstance(image1, InMemoryUploadedFile):
            image1 = Image.open(image1)

        # Calculate hash for the first image
        hash1 = imagehash.average_hash(image1)

        # Download the content of the second image
        response = requests.get(image2_url)
        response.raise_for_status()  # Raise an exception for unsuccessful HTTP responses

        # Open the downloaded image content
        with Image.open(io.BytesIO(response.content)) as image2:
            # Convert the second image to 'RGB' mode if it's not already
            if image2.mode != 'RGB':
                image2 = image2.convert('RGB')

            # Calculate the hash for the second image
            hash2 = imagehash.average_hash(image2)

            # Calculate normalized hamming distance
            hamming_distance = hash1 - hash2
            hash_length = len(str(hash1))

            # Calculate similarity percentage
            normalized_distance = hamming_distance / hash_length
            similarity_percentage = (1 - normalized_distance) * 100

            # Set a threshold to determine similarity
            similarity_threshold = 90  # Adjust the threshold as needed

            return similarity_percentage, similarity_percentage >= similarity_threshold
    except (UnidentifiedImageError, requests.exceptions.RequestException) as e:
        # Handle errors when opening images or downloading from the web
        print(f"Error in image_similarity: {e}")
        return 0, False
