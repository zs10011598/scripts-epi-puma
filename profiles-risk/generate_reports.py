import pandas as pd 
import requests
import json
import datetime as dt


target_clases = ['CONFIRMADO', 'HOSPITALIZADO', 'NEUMONIA', 'INTUBADO', 'FALLECIDO']

#url = 'https://covid19.c3.unam.mx/gateway/api/analysis-population/time-validation-dge/'
body = json.loads("""
	{
	  "target": "FALLECIDO",
	  "initial_date": "2020-02-01",
	  "period": 90
	}
""")

initial_date = dt.datetime.strptime(initial_date, '%Y-%m-%d')
delta_period = dt.timedelta(days = 90)
today = dt.date.today()

while initial_date < today:
	for target in target_clases:
		body['target'] = target
		body['initial_date'] = initial_date
		
		print('<<<====================Start======================>>>')
		url = 'http://127.0.0.1:8000/api/dge/covariables/'
		print("URL {0}".format(url))
		print("Body {0}".format(json.dumps(body)))
		response = requests.post(url, json=body).json()
		print("Response {0}".format(json.dumps(response)))
		print('<<<=====================End=======================>>>')

		pd.DataFrame(response).to_csv('./reports/dge-covariables-{0}-{1}-{2}.csv'.format(target, initial_date.strftime('%Y-%m-%d'), period))

		print('<<<====================Start======================>>>')
		url = 'http://127.0.0.1:8000/api/dge/cells/'
		print("URL {0}".format(url))
		print("Body {0}".format(json.dumps(body)))
		response = requests.post(url, json=body).json()
		print("Response {0}".format(json.dumps(response)))
		print('<<<=====================End=======================>>>')

		pd.DataFrame(response).to_csv('./reports/dge-occurrences-{0}-{1}-{2}.csv'.format(target, initial_date.strftime('%Y-%m-%d'), period))
	
	initial_date += delta_period
