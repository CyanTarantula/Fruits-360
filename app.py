import pickle
from sklearn.ensemble import RandomForestClassifier
import cv2
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import cv2
from sklearn.model_selection import train_test_split as tts

from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.neighbors import KNeighborsClassifier

from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, AveragePooling2D
import tensorflow as tf
from tensorflow import keras

from flask import Flask, jsonify, send_from_directory, request, flash, redirect, url_for, session, Response
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from api.HelloApiHandler import HelloApiHandler
from werkzeug.utils import secure_filename
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')

app = Flask(__name__, static_url_path='', static_folder='fruits360/build')

UPLOAD_FOLDER = 'E:/IIT Jodhpur/Semester 4/Classes/PRML/Main Project/Website/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app) #comment this on deployment
api = Api(app)

model = pickle.load(open('model.pkl', 'rb'))

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(HelloApiHandler, '/flask/hello')

@app.route('/upload', methods=['POST'])
def fileUpload():
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info(" welcome to upload")

    file = request.files['file']
    filename = secure_filename(file.filename)
    
    destination="/".join([target, filename])
    file.save(destination)
    
    logger.info(" Image saved at "+ str(destination))
    # print("File info:", filename, destination)

    image = mpimg.imread(destination)
    image = cv2.resize(image, (20, 20), interpolation=cv2.INTER_AREA)
    image = image.flatten().astype(np.uint8).reshape(1, 1200)
    prediction = model.predict(image)[0]

    # cnnModel, cnnClasses = pickle.load(open('model_cnn.pkl', 'rb'))
    # cnnModel = keras.model.load_model('model_cnn2.h5')
    # prediction = cnnClasses[cnnModel.predict(np.array([image.reshape((20, 20, 3))])).argmax()]

    logger.info(" Prediction: " + str(prediction[0]))

    ret_msg = prediction
    # session['uploadFilePath']=destination
    
    # response = {"status": "Success", "message": ret_msg}
    response = {
        "status": 200,
        "data": {"message": ret_msg}
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

# api.add_resource(HelloApiHandler, 'api/uploadimage/<string:fname?>')

# @app.route('/predict',methods=['POST'])
# def predict():
#     '''
#     For rendering results on HTML GUI
#     '''
#     int_features = [float(x) for x in request.form.values()]
#     final_features = [np.array(int_features)]
#     prediction = model.predict(final_features)

#     output = round(prediction[0], 2)

#     # return render_template('index.html', prediction_text='CO2 Emission of the vehicle is :{}'.format(output))
#     return send_from_directory(app.static_folder, 'index.html', prediction_text=str(prediction))

# @app.route('/add_todo', methods=['POST'])
# def add_todo():
#     todo_data = request.get_json()
#     print(todo_data)
#     return 'Done', 201

# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         # if user does not select file, browser also
#         # submit an empty part without filename
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file:
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file',
#                                     filename=filename))
#     # return send_from_directory(app.static_folder,'index.html')
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)