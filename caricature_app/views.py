import requests
import json
import time
import base64, os, uuid
from django.conf import settings
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import os
import uuid
import mimetypes




from django.shortcuts import render

def home(request):
    return render(request, 'caricature_app/home.html')





API_KEY = '947b54b0c6694d4fa413608294950954_b31ac7d90a6944adbf4b79ab09bb254a_andoraitools'


def save_image_from_base64(data_url):
    try:
        format, imgstr = data_url.split(';base64,')
        ext = format.split('/')[-1]
        image_data = base64.b64decode(imgstr)

        filename = f"{uuid.uuid4()}.{ext}"
        image_path = os.path.join(settings.MEDIA_ROOT, 'captured', filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        with open(image_path, 'wb') as f:
            f.write(image_data)            
        return image_path, filename
    except Exception as e:
        raise Exception(f"Image saving failed: {str(e)}")







API_KEY = "947b54b0c6694d4fa413608294950954_3842e0a454764af88987cffb0cfb96e0_andoraitools"





def upload_image_to_lightx(api_key, file_path):
    """
    Uploads an image to LightX API and returns the image URL for caricature generation
    """
    try:
        # Get file metadata
        file_size = os.path.getsize(file_path)
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = 'application/octet-stream'

        # Step 1: Get upload URL
        url = "https://api.lightxeditor.com/external/api/v2/uploadImageUrl"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }
        payload = {
            "uploadType": "imageUrl",
            "size": file_size,
            "contentType": content_type
        }

        # Get signed URL
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        upload_data = response.json()
        
        # Extract URLs from response
        if 'body' not in upload_data or 'uploadImage' not in upload_data['body']:
            raise ValueError("Invalid API response structure")

        upload_url = upload_data['body']['uploadImage']
        final_image_url = upload_data['body']['imageUrl']

        # Step 2: Upload file using PUT request
        with open(file_path, 'rb') as file:
            put_headers = {'Content-Type': content_type}
            upload_response = requests.put(upload_url, headers=put_headers, data=file)
            upload_response.raise_for_status()

        return {
            'status': 'success',
            'image_url': final_image_url,  # Use this URL for caricature generation
            'upload_response': upload_data,
            'put_status': upload_response.status_code
        }

    except requests.exceptions.HTTPError as http_err:
        return {
            'status': 'error',
            'message': f"HTTP error: {http_err}",
            'status_code': http_err.response.status_code if http_err.response else None,
            'response': http_err.response.text if http_err.response else None
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'error_type': type(e).__name__
        }
    


# def upload_image_to_lightx(image_path, filename):
# def generate_caricature_from_url(user_image_url, reference_image_url):
#     try:
#         headers = {
#             "Content-Type": "application/json",
#             "x-api-key": API_KEY
#         }

#         payload = {
#             "imageUrl": user_image_url,
#             "styleImageUrl": reference_image_url,
#             "textPrompt": "match face style with reference image"
#         }

#         response = requests.post(
#             "https://api.lightxeditor.com/external/api/v1/caricature",
#             headers=headers,
#             json=payload
#         )

#         if response.status_code == 200:
#             return response.json().get("outputImageUrl")
#         else:
#             raise Exception(f"Caricature generation failed: {response.text}")
#     except Exception as e:
#         raise Exception(f"Caricature API error: {str(e)}")

@csrf_exempt
def camera_view(request):
    if request.method == 'POST':
        try:
            data_url = request.POST.get('image')
            # # Step 1: Save image
            # image_path, filename = save_image_from_base64(data_url)
            # # Step 2: Upload to LightX
            # uploaded_url = upload_image_to_lightx(image_path, filename)
            # Step 1: Save and upload user photo
            image_path, filename = save_image_from_base64(data_url)


            upload_result = upload_image_to_lightx(API_KEY, image_path)
            user_image_url =upload_result['image_url']
            # user_image_url="https://lightx-ai-version-2.s3-accelerate.amazonaws.com/apikey/c226202445f04781b3ac46808760149c.jpeg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20250513T092513Z&X-Amz-SignedHeaders=content-length%3Bcontent-type%3Bhost&X-Amz-Expires=3600&X-Amz-Credential=AKIA2Y6AHIB47OUAEN64%2F20250513%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Signature=fea749182f0e6d36609b8b22c052618cda988f158101a5bb3287ebf41a7c0671"
            # user_image_url = "https://server9.groupthink.events/caricatureimg/profile/test1.jpg"                       
            request.session['user_image_url'] = upload_result['image_url']

            return redirect('style_selection')
            # text_prompt = "match face style with reference image"

            # caricature_url = generate_caricature_from_url(user_image_url, reference_image_url, text_prompt)
            # return render(request, 'caricature_app/result.html', {'image_url': caricature_url})
        except Exception as e:
            return render(request, 'caricature_app/result.html', {'error': str(e)})
    return render(request, 'caricature_app/camera.html')




def generate_caricature_from_url(user_image_url, reference_image_url,image_prompt):  
    try:
        headers = {
            'x-api-key': '947b54b0c6694d4fa413608294950954_3842e0a454764af88987cffb0cfb96e0_andoraitools',  # Replace with your actual API key
            'Content-Type': 'application/json'
        }

        # Step 1: Submit caricature generation request
        payload = {
            "imageUrl": user_image_url,
            "styleImageUrl": reference_image_url,
            "textPrompt": image_prompt
        }

        response = requests.post(
                "https://api.lightxeditor.com/external/api/v1/caricature",
                headers=headers,
                json=payload
            )       
        
        if response.status_code != 200:
            raise Exception(f"Caricature generation failed: {response.text}")

        # Step 2: Extract orderId
        order_id = response.json().get("body", {}).get("orderId")
        print("Order ID:", order_id)
        time.sleep(10)  # Wait for a few seconds before checking the status
        output_url = get_output_image_url(order_id)
        return output_url
    except Exception as e:
        raise Exception(f"Caricature API error: {str(e)}")



def get_output_image_url(order_id):
    url = 'https://api.lightxeditor.com/external/api/v1/order-status'
    api_key = '947b54b0c6694d4fa413608294950954_3842e0a454764af88987cffb0cfb96e0_andoraitools'

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key
    }

    payload = {
        "orderId": order_id
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        data = response.json()
        print(response.text)  # Optional: for debugging

        body = data.get("body", {})
        status = body.get("status")
        output_url = body.get("output")

        print("Output URL rajan shukla:", output_url)
        print(f"Status: {status}")
        return output_url
    
    except Exception as e:
        return {"error": str(e)}




from django.core.paginator import Paginator
from django.shortcuts import render
from .models import StyleImage


# views.py
from django.shortcuts import redirect, get_object_or_404

def style_selection(request):
    all_styles = StyleImage.objects.all()
    paginator = Paginator(all_styles, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'caricature_app/style_selection.html', {'page_obj': page_obj})

def generate_caricature(request):
    if request.method == 'POST':
        # Get selected style from POST data
        selected_style_id = request.POST.get('style_id')
        selected_style = get_object_or_404(StyleImage, id=selected_style_id)
        
        # Get user image URL from session (set in camera_view)
        user_image_url = request.session.get('user_image_url')
        
        if not user_image_url:
            return redirect('camera_view')
        
        # Generate caricature using both images and prompt
        caricature_url = generate_caricature_from_url(
            user_image_url=user_image_url,
            reference_image_url=selected_style.image_url,  # From selected style
           image_prompt=selected_style.prompt  # From selected style's prompt
        )
        
        return render(request, 'caricature_app/result.html', {
            'image_url': caricature_url,
            'prompt': selected_style.prompt,
            'reference_style': selected_style.name
        })
    
    return redirect('style_selection')
