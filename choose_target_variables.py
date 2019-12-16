"""
This file allows the user to choosing their "target" variable for performing machine learning on
"""
#import fileinput
import re
import pandas as pd
import sys
sys.path.append('/src/machine_learning/')
import werkzeug
import xlrd
import xlsxwriter
from flask import Flask
from flask_restplus import Namespace, Api, fields, Resource, reqparse
from flask_cors import CORS
from tkinter import Tk, Label, IntVar, Entry, Button

# app defaults
VERSION = '1.0'
TITLE = 'Machine Learning Functionality API'
DESCRIPTION = ('This section of the API uses the file imported from import_module to allow the user to select the target variable column')
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
    'outputOccurrenceColumns': fields.List(fields.Integer(min=1))
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
        This allows the user to choose the target variable to be predicted by the ML model
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

#Preliminary setup for allowing user to select column of the data as the ingested column                
top = Tk()
top.title("Occurrence algorithm")
top.geometry("700x640+0+0")

theLabel = Label(top, text = "Occurrence algorithm", font=("arial", 40, "bold"), fg="black")

theLabel1 = Label(top, text = "Enter the column of interest:", font=("arial", 12, "bold"), fg="black").place(x=0, y=0)

input1 = IntVar()
entry_box = Entry(top, textvariable=input1, width=25, bg="lightgreen").place(x=3, y=25)
column = IntVar()

def do_it(): 
    global input1
    global column
    column = input1.get()
    top.destroy()

button1 = Button(top, text="Submit", width=30, height=5, bg="lightblue", command=do_it).place(x=3, y=300)

top.mainloop()

if __name__ == '__main__':
    APP_E.run(host='0.0.0.0', debug=True)
