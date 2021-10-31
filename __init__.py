from flask import Flask
from flask import jsonify
from flask import request
import numpy as np
import base64
import io
#from PIL import Image
import keras
#from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import render_template
from imageio import imread
from skimage.transform import resize
import keras.models
import sys
import os
import re
import logging
#from keras import backend as K
#from keras.utils.conv_utils import convert_kernel
#from load import *
#initalize our flask app
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

def get_model():
    global model
    model=load_model('doodle.h5')
    app.logger.info('model loaded')

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
	app.logger.info('home fetched')
	#render out pre-built HTML file right on the index page
	return render_template("i.html")

get_model()

@app.route('/predict/',methods=['GET','POST'])
def predict():
   d={1:'banana',2:'apple',3:'bicycle',4:'car',5:'chair',6:'shoe',7:'lollipop',8:'sandwich',9:'headphones',10:'eyeglasses',11:'tshirt',12:'diamond'}
   imgData = request.get_data()
   convertImage(imgData)
   x = imread('output.png',pilmode='L')	
   app.logger.info('image created')
   x = np.invert(x)
   x = resize(x,(28,28))
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
   app.logger.info('guess made')
   #out = model.predict(x)
   #print(val)
   #print(np.argmax(val))
#print "debug3"
#convert the response to a string
   response = d[np.argmax(val)+1]
   return response


if __name__ == "__main__":
#decide what port to run the app in
    #app.jinja_env.auto_reload = True
    #app.config['TEMPLATES_AUTO_RELOAD'] = True
    #port = int(os.environ.get('PORT', 5000))
    app.run(debug=True)
	#optional if we want to run in debugging mode
	#app.run(debug=True)
