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

period = 90
initial_date = dt.datetime.strptime('2020-02-01', '%Y-%m-%d').date()
delta_period = dt.timedelta(days = 90)
today = dt.date.today()

while initial_date < today:
	for target in target_clases:
		body['target'] = target
		body['initial_date'] = initial_date.strftime('%Y-%m-%d')
		
		print('<<<====================Start======================>>>')
		url = 'https://covid19.c3.unam.mx/gateway/api/dge/covariables/'
		print("URL {0}".format(url))
		print("Body {0}".format(json.dumps(body)))
		response = requests.post(url, json=body)
		print("Response {0}".format(response))
		print('<<<=====================End=======================>>>')

		try:
			df = pd.DataFrame(response.json())
			df.to_csv('./reports/dge-covariables-{0}-{1}-{2}.csv'.format(target, initial_date.strftime('%Y-%m-%d'), period), index=False)
		except Exception as e:
			print(str(e))

		print('<<<====================Start======================>>>')
		url = 'https://covid19.c3.unam.mx/gateway/api/dge/cells/'
		print("URL {0}".format(url))
		print("Body {0}".format(json.dumps(body)))
		response = requests.post(url, json=body)
		print("Response {0}".format(response))
		print('<<<=====================End=======================>>>')

		try:
			df = pd.DataFrame(response.json())
			df.to_csv('./reports/dge-occurrences-{0}-{1}-{2}.csv'.format(target, initial_date.strftime('%Y-%m-%d'), period), index=False)
		except Exception as e:
			print(str(e))
	
	initial_date += delta_period
