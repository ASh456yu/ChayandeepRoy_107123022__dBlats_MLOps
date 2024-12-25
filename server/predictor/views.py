from django.http import JsonResponse
from django.shortcuts import render
import numpy as np
from PIL import Image
import pickle


from server.settings import BASE_DIR

loaded_model1 = pickle.load(open(BASE_DIR/'Saved models/model_pickle1', 'rb'))
loaded_model2 = pickle.load(open(BASE_DIR/'Saved models/model_pickle2', 'rb'))

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def predict(request):
    if request.method == "POST":
        image_file = request.FILES.get('image_file')
        if not image_file:
            return JsonResponse({'error': 'No image file uploaded'}, status=400)

        model_name = request.POST.get('model')
        if not model_name:
            return JsonResponse({'error': 'No model specified'}, status=400)
        
        
        image = Image.open(image_file).convert('RGB')
        image = image.resize((256, 256))
        image_array = np.array(image)
        image_array = np.expand_dims(image_array, axis=0)
        if model_name == "Deep Neural Network":
            prediction = loaded_model1.predict(image_array)
            result_message = "It's a dog." if prediction > 0.5 else "It's a cat."
        if model_name == "Resnet 152":
            prediction = loaded_model2.predict(image_array)
            result_message = "It's a dog." if prediction > 0.5 else "It's a cat."

            return JsonResponse({'result': result_message})
        else:
            return JsonResponse({'error': 'Invalid request model'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)