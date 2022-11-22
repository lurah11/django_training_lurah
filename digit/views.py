from django.shortcuts import render
from django.http import JsonResponse
import numpy as np 

from PIL import Image, ImageOps
import io
from tensorflow import keras
import urllib



#helper Function 
def is_grey_scale(img):
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i,j))
            if r != g != b: 
                return False
    return True

model_1 = keras.models.load_model('digit\lurah_cnn_handwriting_classifier_rgb_1.h5')
model_2 = keras.models.load_model('digit\lurah_cnn_handwriting_mobilenet_2.h5')

print(model_1.summary())
print(model_2.summary())



# Create your views here.
def digit_home_view(request): 
    
    return render(request,'digit/digit.html')
def predict_digit_view(request):
    print(request)
    if request.method == 'POST': 
        
        image_data_url = request.POST.get("img_data")

        response = urllib.request.urlopen(image_data_url)
        resp = response.file.read()
        img = Image.open(io.BytesIO(resp))
        
        bg_image = Image.new('RGBA',size=img.size,color="white")
        bg_image.paste(img,(0,0),img)
        
        
        conv_img = bg_image.convert('RGB')
        final_img = conv_img.resize((32,32))
        final_img2 = conv_img.resize((64,64))

        # prediction for lurah_net
        arr = np.array(final_img)
        yhat_prob = model_1.predict(np.expand_dims(arr/255,0))
        pred = np.argmax(yhat_prob)
        prob = np.max(yhat_prob)

        # prediction for mobilenet 
        arr2 = np.array(final_img2)
        yhat_prob2 = model_2.predict(np.expand_dims(arr2/255,0))
        pred2 = np.argmax(yhat_prob2)
        prob2 = np.max(yhat_prob2)


        # img = bg_image.convert('RGB')
        
                
       
        # is_gscale = is_grey_scale(img)
        # if is_gscale:
        #     img = img.resize((256,256))
        #     img.show()
        #     print(img.size)
        #     arr = np.array(img)
            
        #     print(model.summary())
        #     print(arr.shape)
        #     yhat = model.predict(np.expand_dims(arr/255, 0))
        #     pred = np.argmax(yhat)
        #     print(yhat)
        #     print(pred)
  
        return JsonResponse({'res1':str(pred),"res2":str(prob),"res1_2":str(pred2),"res2_2":str(prob2)})


