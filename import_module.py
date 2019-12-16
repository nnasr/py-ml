"""
This file imports and cleans any .xlsx file
"""
import re
import pandas as pd
import werkzeug
import xlrd
import xlsxwriter
from flask import Flask
from flask_restplus import Namespace, Api, fields, Resource, reqparse
from flask_cors import CORS

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
    'targetOccurrenceColumn': fields.Integer(min=1), #alter for button select on ui
    'outputOccurrenceColumns': fields.List(fields.Integer(min=1)), #same alteration here
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
        '''
        This reads the imported file
        '''

        result = []

        try:

            data = API.payload
            target_occ_column = data['targetOccurrenceColumn']
            output_occ_columns = data['outputOccurrenceColumns']
            tot_columns = target_occ_column.append(output_occ_columns)
            data_set = data['File_UPLOAD'].add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
            data_frame = pd.DataFrame(data_set)
            total_rows = len(data_frame)  # altering file to user input
            med_dict = pd.read_excel('DrugNames.xlsx', na_values="null",
                             sheet_names='DrugNames.xlsx')

            med_dict_array = med_dict.values
            for row in data_frame.items():
                for i in range(0, total_rows):
                    tri_guys = []
                    data_lowercase = str(data_frame[target_occ_column][i]).lower()
                    data_stripped = [c.strip() for c in re.split(r'(\W+)',
                                                                 data_lowercase) if c.strip() != '']
                for current_word in data_stripped:
                    tri_guys = tri_guys + [data_lowercase]

                response = tri_guys

                if response:
                    result.append(response)
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
