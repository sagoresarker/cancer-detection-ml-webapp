import io
import json
from django.http import HttpResponse, JsonResponse
from .models import Image
import tensorflow as tf
import numpy as np
from django.shortcuts import redirect, render

import uuid

def generate_random_filename():
    # Generate a random UUID
    random_uuid = uuid.uuid4()

    # Convert the UUID to a string and remove hyphens
    filename = str(random_uuid).replace('-', '')

    return filename


def detect_cancer(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Retrieve the uploaded image from the request
        user = request.user

        image_file = request.FILES['image']

        image_bytes = image_file.read()  # Read the file content
        image_stream = io.BytesIO(image_bytes)  # Convert to byte stream
        
        # Load the .h5 model
        model = tf.keras.models.load_model('model/oralCancerVggg19.h5')

        # Preprocess the image
        img = tf.keras.preprocessing.image.load_img(image_stream, target_size=(224, 224))
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = np.expand_dims(img, axis=0)

        # Make predictions
        prediction = model.predict(img)
        cancer_probability = prediction[0][1]  # Assuming 1 is the index for cancer probability

        cancer_probability = float(cancer_probability)

        response_data = {
            'cancer_probability': cancer_probability
        }

        name = generate_random_filename()
        json_data = json.dumps(response_data)

        # Save the image and label it with the model output
        Image.objects.create(user=user, name=name, image=image_file, label='Cancer' if cancer_probability >= 0.5 else 'Non-Cancer', probability=cancer_probability)

        return redirect('dashboard')
        # Return the response as a JSON object
        #return JsonResponse({'cancer_probability': cancer_probability})

    return render(request, 'upload_file.html')


