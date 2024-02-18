# base/views2/views.py
'''from django.shortcuts import render
from image_match.goldberg import ImageSignature
from google_images_search import GoogleImagesSearch
import requests

def download_image(url):
    response = requests.get(url)
    return response.content

def image_search(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Your Google Custom Search API key and CX
        api_key = 'AIzaSyAzVIn1Z6yzRKrwon26f-JP-5_BoWR8jok'
        cx = 'a57946bf7faf24ae1'

        # Search parameters
        search_params = {
            'num': 10,    # Number of search results
            'fileType': 'jpg|gif|png',  # Image file types
            # Other search parameters...
        }

        # Initialize GoogleImagesSearch
        gis = GoogleImagesSearch(api_key, cx)

        # Perform image search
        gis.search(search_params)

        # Download the uploaded image
        uploaded_image = request.FILES['image'].read()

        # Initialize ImageSignature for image matching
        img_signature = ImageSignature()

        # Calculate the signature of the uploaded image
        uploaded_signature = img_signature.generate_signature(uploaded_image)

        # Compare the uploaded image signature with the signatures from Google Images
        similar_results = []
        for image in gis.results():
            image_url = image.url
            google_image = download_image(image_url)
            google_signature = img_signature.generate_signature(google_image)

            # Set a threshold for similarity, you may need to adjust this based on your needs
            similarity_threshold = 0.5

            if img_signature.normalized_distance(uploaded_signature, google_signature) < similarity_threshold:
                similar_results.append({'url': image_url, 'similarity': img_signature.normalized_distance(uploaded_signature, google_signature)})

        return render(request, 'results2.html', {'search_results': similar_results})

    return render(request, 'imagesearch.html')'''
