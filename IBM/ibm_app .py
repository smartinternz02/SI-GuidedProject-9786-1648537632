
# importing the necessary dependencies
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "QtLGvFscqlQSWq7Y-G2B-RC-9NHBfdT9OWrAuX6epfVQ"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__) # initializing a flask app


@app.route('/')# route to display the home page
def home():
    return render_template('home.html') #rendering the home page

@app.route('/Prediction',methods=['POST','GET'])
def prediction():
    return render_template('indexnew.html')

@app.route('/Home',methods=['POST','GET'])
def my_home():
    return render_template('home.html')

@app.route('/predict',methods=['POST'])# route to show the predictions in a web UI
def predict():
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    #  reading the inputs given by the user
    
    blood_urea= request.form["blood_urea"]
    blood_glucose= request.form["blood glucose random"]
    anemia = request.form["anemia"]
    coronary_artery_disease = request.form["coronary_artery_disease"]
    pus_cell = request.form["pus_cell"]
    red_blood_cell = request.form["red_blood_cell"]
    diabetesmellitus = request.form["diabetesmellitus"]
    pedal_edema = request.form["pedal_edema"]
    
    t = [[int(blood_urea),int(blood_glucose),int(anemia),int(coronary_artery_disease),int(pus_cell),
          int(red_blood_cell),int(diabetesmellitus),int(pedal_edema)]]
    
    payload_scoring = {"input_data": [{"field": [['blood_urea', 'blood glucose random', 'anemia', 'coronary_artery_disease', 'pus_cell', 'red_blood_cells',
       'diabetesmellitus', 'pedal_edema']], "values": t}]}
    
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/4dddf767-317f-47ab-9c91-c66b5ef7b480/predictions?version=2022-04-28', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    pred = predictions['predictions'][0]['values'][0][0]
    print("Final prediction :",pred)
    
    # showing the prediction results in a UI# showing the prediction results in a UI
    return render_template('result.html', prediction_text=pred)

if __name__ == '__main__':
    # running the app
    app.run(debug=True)
