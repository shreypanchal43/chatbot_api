from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import pickle
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from tensorflow import keras
# from sklearn.preprocessing import LabelEncoder
from keras.models import load_model
import requests


model = load_model('masters/chat_model')

intents = json.loads(open('masters/data (1).json').read())
tokenizer = pickle.load(open('masters/tokenizer.pkl','rb'))

# pickle.dump('masters/label_encoder.pkl', open('masters/label_encoder.pkl', 'wb'))
lbl_encoder = pickle.load(open('masters/label_encoder.pkl', 'rb'))
print(lbl_encoder)


# lbl_encoder = pickle.load(open('masters/label_encoder.pkl','rb'))
# Create your views here.
@api_view(['GET', 'POST'])
def prediction_api(request):
    request = json.loads(request.body.decode('utf-8'))
    
    msg = request["message"]
    flag = request["flag"]
    if flag == 0:
        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([msg]),
                                                    truncating='post', maxlen=20))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        for i in intents['intents']:
            if i['tag'] == tag:
                return_list = np.random.choice(i['responses'])
        if return_list == "food":
            data = {
                "userName": "qatesting@test.com",
                "password": "qatesting",
                "deviceId": "12345"
                }
        
            url = "https://dev.enterprise.heywoohoo.com/v1/user/login"

            res = requests.post(url, data=data)

            sessiontoken = res.json()["data"]["sessionToken"]
            header = {"Authorization": sessiontoken,}
                
            url3 = "https://dev.enterprise.heywoohoo.com/v1/fnb/subCategories/9"
            return_list = requests.get(url3, headers = header)
            return HttpResponse(json.dumps(return_list.json()["data"]["subCategories"], indent=4,default=str),content_type = "application/json")
        elif return_list == "There are lot of facilities and services available along with the price-\n\n Gym - 10$\n Pool - 10$\n Dinner Table - 50$\n Yoga Session - 20$\n Spa Services - 30$\n Taxi Services - depends on your route":
            data = {
                     "userName": "qatesting@test.com",
                     "password": "qatesting",
                     "deviceId": "12345"
                    }
 
            url = "https://dev.enterprise.heywoohoo.com/v1/user/login"

            res = requests.post(url, data=data)

            sessiontoken = res.json()["data"]["sessionToken"]

            header = {"Authorization": sessiontoken,}

            url = "https://dev.enterprise.heywoohoo.com/v1/propertyServices/property/159"
            res = requests.get(url, headers = header)
            return HttpResponse(json.dumps(res.json()["data"], indent=4,default=str),content_type = "application/json")
    elif flag == 1:
        data = {
                "userName": "qatesting@test.com",
                "password": "qatesting",
                "deviceId": "12345"
                }
        
        url = "https://dev.enterprise.heywoohoo.com/v1/user/login"
        res = requests.post(url, data=data)
        sessiontoken = res.json()["data"]["sessionToken"]
        header = {"Authorization": sessiontoken,}
        url4 = "https://dev.enterprise.heywoohoo.com/v1/fnb/products?subCategoryId=" + msg
        res4 = requests.get(url4, headers = header)
        print(res4.json()["data"]["products"])
        return HttpResponse(json.dumps(res4.json()["data"]["products"], indent=4,default=str),content_type = "application/json")
    
    elif flag == 2:
        date = request["date"]
        id = request["id"]
        data = {
                "userName": "qatesting@test.com",
                "password": "qatesting",
                "deviceId": "12345"
                }
        
        url = "https://dev.enterprise.heywoohoo.com/v1/user/login"
        res = requests.post(url, data=data)
        sessiontoken = res.json()["data"]["sessionToken"]
        header = {"Authorization": sessiontoken,}
        url = "https://dev.enterprise.heywoohoo.com/v1/propertyServices/allSlots/" + id + "/" + date
        res = requests.get(url, headers = header)
        return HttpResponse(json.dumps(res.json()["data"], indent=4,default=str),content_type = "application/json")
        
    # return return_list
    return HttpResponse(json.dumps({"reply":return_list}, indent=4,default=str),content_type = "application/json")





#############################################################################################################################################
def home(request, template_name="home.html"):
	context = {'title': 'Chatbot Version 1.0'}
	return render(request, template_name, context)

@csrf_exempt
def get_response(request):
    response = {'status':None}
    if request.method == 'POST':
        data = json.loads(request.body)
        msg = data['city']
        output = chatbot_response(msg)
        response['message'] = {'text':output, 'user':False, 'chat_bot':True}
        response['status'] = 'ok'
    else:
        response['error'] = 'no data found'
    return response
    
    # return HttpResponse(
    #     json.dumps(response),
    #     content_type='application/json'
    # )

