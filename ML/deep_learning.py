"""
This section is the structure for running a deep learning model on ingested data 
"""

import re
import pandas as pd
import werkzeug
from flask import Flask
from flask_restplus import Namespace, Api, fields, Resource, reqparse
from flask_cors import CORS
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping

# app defaults
VERSION = '1.0'
TITLE = 'Machine Learning Functionality API'
DESCRIPTION = ('This section of the API takes an import of an .xls, '
               '.xlsx, or a .csv converted into a .xls or .xslx through the excel import wizard. '
               'Upon ingestion of this information, this will clean the data and prepare it for '
               'machine learning to be enacted upon it')
APP_E = Flask(__name__)
CORS(APP_E)

# api defaults
API = Api(
    app=APP_E,
    version=VERSION,
    title=TITLE,
    description=DESCRIPTION,
    doc='/swagger-ui.html'
)

#API.namespaces.pop(0)
NS = Namespace('machine learning', description='Machine Learning Algorithm')
API.add_namespace(NS)

OCC_MODEL_E = API.model('occurrence inputs', {
    'targetOccurrenceColumn': fields.Integer(min=1),
    'FILE_UPLOAD': reqparse.RequestParser()
})

# Routes #
@NS.route('/xlsx')

class Occur(Resource):
    '''Data ingestion Endpoint'''

    @staticmethod
    @NS.expect(OCC_MODEL_E)
    @NS.doc(responses={
        200: 'Success',
        400: 'Validation Error',
        500: 'Internal Server Error'
    })
    def post():
        result = []

        try:
            data = API.payload
            data_set = data['File_UPLOAD'].add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
            train_df = data_frame = pd.DataFrame(data_set)
            Y = data['targetOccurrenceColumn']
            #total_rows = len(data_frame)

            #create a dataframe with all training data except the target column
            train_X = train_df.drop(columns=Y)

            #check that the target variable has been removed
            train_X.head()

            #create a dataframe with only the target column
            train_y = train_df[Y]

            #view dataframe
            train_y.head()

            #######################
            #create model
            model = Sequential()

            #get number of columns in training data
            n_cols = train_X.shape[1]

            #add model layers
            model.add(Dense(10, activation='relu', input_shape=(n_cols,)))
            model.add(Dense(10, activation='relu'))
            model.add(Dense(1))

            #compile model using mse as a measure of model performance
            model.compile(optimizer='adam', loss='mean_squared_error')

            ###########################
            #set early stopping monitor so the model stops training when it won't improve anymore
            early_stopping_monitor = EarlyStopping(patience=3)
            #train model
            model.fit(train_X, train_y, validation_split=0.2, epochs=30, callbacks=[early_stopping_monitor])

            #example on how to use our newly trained model on how to make predictions on unseen data (we will pretend our new data is saved in a dataframe called 'test_X').
            test_X = pd.DataFrame(columns=[Y, train_X])
            test_y_predictions = model.predict(test_X)

            #training a new model on the same data to show the effect of increasing model capacity

            #create model
            model_mc = Sequential()

            #add model layers
            model_mc.add(Dense(200, activation='relu', input_shape=(n_cols,)))
            model_mc.add(Dense(200, activation='relu'))
            model_mc.add(Dense(200, activation='relu'))
            model_mc.add(Dense(1))

            #compile model using mse as a measure of model performance
            model_mc.compile(optimizer='adam', loss='mean_squared_error')
            #train model
            model_mc.fit(train_X, train_y, validation_split=0.2, epochs=30, callbacks=[early_stopping_monitor])

            #read in training data
            train_df_2 = pd.read_csv('documents/data/diabetes_data.csv')

            #view data structure
            train_df_2.head()

            #create a dataframe with all training data except the target column
            train_X_2 = train_df_2.drop(columns=['diabetes'])

            #check that the target variable has been removed
            train_X_2.head()

            from keras.utils import to_categorical
            #one-hot encode target column
            train_y_2 = to_categorical(train_df_2.diabetes)

            #vcheck that target column has been converted
            train_y_2[0:5]

            #create model
            model_2 = Sequential()

            #get number of columns in training data
            n_cols_2 = train_X_2.shape[1]

            #add layers to model
            model_2.add(Dense(250, activation='relu', input_shape=(n_cols_2,)))
            model_2.add(Dense(250, activation='relu'))
            model_2.add(Dense(250, activation='relu'))
            model_2.add(Dense(2, activation='softmax'))

            #compile model using accuracy to measure model performance
            model_2.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

            #train model- define X_2 and target
            X_2 = train_X_2
            target = train_y_2
            model_2.fit(X_2, target, epochs=30, validation_split=0.2, callbacks=[early_stopping_monitor])
