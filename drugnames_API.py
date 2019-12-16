'''Drug Names Dictionary API '''
from flask import Flask
from flask_restful import Resource, Api
import pandas as pd

APP_DRUGS = Flask(__name__)
API_DRUGS = Api(APP_DRUGS)

class Drugs(Resource):
    ''' Gets drug names database'''
    def get(self):
        ''' see above '''
        data = pd.read_excel('DrugNames.xlsx', na_values="null",
                             sheet_names='DrugNames.xlsx')
        return data # Fetches drug name data



API_DRUGS.add_resource(Drugs, '/drugnames') # Route_1


if __name__ == '__main__':
    APP_DRUGS.run(port='5002')
