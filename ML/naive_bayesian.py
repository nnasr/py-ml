
"""
This file has the framework for conducting a naive bayesian ml test on ingested data
"""

import numpy as np
import pandas as pd
import re
import werkzeug
from flask import Flask
from flask_restplus import Namespace, Api, fields, Resource
from flask_cors import CORS
from sklearn.naive_bayes import GaussianNB

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
        '''
        This reads the imported file
        ''' 
        result = []

        try:

            data = API.payload
            data_set = data['File_UPLOAD'].add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
            train_df = data_frame = pd.DataFrame(data_set)
            Y = data['targetOccurrenceColumn']
            X = train_df.drop(columns=Y)


            clf = GaussianNB()
            clf.fit(X, Y)
            GaussianNB()
            clf_pf = GaussianNB()
            clf_pf.partial_fit(X, Y, np.unique(Y))
            GaussianNB()

            response = [clf, clf_pf]

            if response:
                result.append(response, {'result': ('This shows the Accuracy of a '
                                                    'Naive Bayesian model that is first completely fitted to the data and then partially fitted')})
            else:
                result.append({'result': ('No result was produced '
                                          'with the given data. Make sure the file you are importing is an .xlsx, .xls, or .csv file')})

        except ValueError as error:
            report = ('ValueError retrieving data', error)
        except TypeError as error:
            report = ('TypeError in retrieving data', error)
        except RuntimeError as error:
            report = ('RuntimeError in retrieving data', error)
        except NameError as error:
            report = ('NameError in retrieving data', error)
        except KeyError as error:
            report = ('KeyError in retrieving data', error)
        return report, 500


if __name__ == '__main__':
    APP_E.run(host='0.0.0.0', debug=True)
