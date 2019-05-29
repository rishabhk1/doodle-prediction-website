from flask import Flask
from flask import jsonify
from flask import request
import numpy as np
import base64
import io
#from PIL import Image
import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import render_template
from scipy.misc import imsave, imread, imresize
import keras.models
import sys
import os
import re
from keras import backend as K
from keras.utils.conv_utils import convert_kernel
#from load import *
#initalize our flask app
app = Flask(__name__)

def get_model():
    global model
    model=load_model('doodle.h5')
    print('Model loaded')

#decoding an image from base64 into raw representation
def convertImage(imgData1):
     imgstr = re.search(b'base64,(.*)',imgData1).group(1) #print(imgstr)
     with open('output.png','wb') as output:
          output.write(base64.b64decode(imgstr))
def normalize(data):
    "Takes a list or a list of lists and returns its normalized form"
    return np.interp(data, [0, 255], [0, 1])

@app.route('/')
def index():
	#initModel()
	#render out pre-built HTML file right on the index page
	return render_template("index.html")

get_model()

@app.route('/predict/',methods=['GET','POST'])
def predict():
   d={1:'banana',2:'apple',3:'bicycle',4:'car',5:'chair',6:'shoe',7:'lollipop',8:'sandwich',9:'headphones',10:'eyeglasses',11:'tshirt',12:'diamond'}
   imgData = request.get_data()
   convertImage(imgData)
   print("debug")
	#read the image into memory
   x = imread('output.png',mode='L')
   x = np.invert(x)
#make it the right size
   x = imresize(x,(28,28))
#imshow(x)
#convert to a 4D tensor to feed into our model
   x = np.invert(x)
   for i in range(len(x)):
        for j in range(len(x)):
            if x[i][j] >100:
                 x[i][j] = min(255, x[i][j] + x[i][j] * 1)
#print("debug2")
#in our computation graph
#perform the prediction
   x=x[:,:,np.newaxis]
   x=normalize(x)
   val = model.predict(np.array([x]))
   #out = model.predict(x)
   print(val)
   print(np.argmax(val))
#print "debug3"
#convert the response to a string
   response = d[np.argmax(val)+1]
   return response


if __name__ == "__main__":
#decide what port to run the app in
    #app.jinja_env.auto_reload = True
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
	#optional if we want to run in debugging mode
	#app.run(debug=True)
