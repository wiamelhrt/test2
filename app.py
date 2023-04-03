from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
import uvicorn
import csv
from typing import List
import pickle
import pandas as pd
from models import Client

app=FastAPI()
model=pickle.load(open("final_model.sav","rb"))

@app.post("/predict")
def predict(data:Client):
    data = data.dict()
    BALANCE=data['BALANCE']
    BALANCE_FREQUENCY=data['BALANCE_FREQUENCY']
    PURCHASES=data['PURCHASES']
    ONEOFF_PURCHASES=data['ONEOFF_PURCHASES']
    INSTALLMENTS_PURCHASES=data['INSTALLMENTS_PURCHASES']
    CASH_ADVANCE=data['CASH_ADVANCE']
    PURCHASES_FREQUENCY=data['PURCHASES_FREQUENCY']
    ONEOFF_PURCHASES_FREQUENCY=data['ONEOFF_PURCHASES_FREQUENCY']
    PURCHASES_INSTALLMENTS_FREQUENCY=data['PURCHASES_INSTALLMENTS_FREQUENCY']
    CASH_ADVANCE_FREQUENCY=data['CASH_ADVANCE_FREQUENCY']
    CASH_ADVANCE_TRX=data['CASH_ADVANCE_TRX']
    PURCHASES_TRX=data['PURCHASES_TRX']
    CREDIT_LIMIT=data['CREDIT_LIMIT']
    PAYMENTS=data['PAYMENTS']
    MINIMUM_PAYMENTS=data['MINIMUM_PAYMENTS']
    PRC_FULL_PAYMENT=data['PRC_FULL_PAYMENT']
    TENURE=data['TENURE']
    print(data)
    prediction=model.predict([[BALANCE,BALANCE_FREQUENCY,PURCHASES,ONEOFF_PURCHASES,INSTALLMENTS_PURCHASES,
    CASH_ADVANCE,
    PURCHASES_FREQUENCY,
    ONEOFF_PURCHASES_FREQUENCY,PURCHASES_INSTALLMENTS_FREQUENCY,CASH_ADVANCE_FREQUENCY,CASH_ADVANCE_TRX,PURCHASES_TRX,
    CREDIT_LIMIT,PAYMENTS,MINIMUM_PAYMENTS,PRC_FULL_PAYMENT,TENURE]])[0]
    
    print(prediction)
   
    return {"this client is assigned to":"cluster {}".format(prediction)}



@app.post("/predictt")
def predict(file: UploadFile):
    df = pd.read_csv(file.file)
    features = df[['BALANCE', 'BALANCE_FREQUENCY', 'PURCHASES', 'ONEOFF_PURCHASES', 'INSTALLMENTS_PURCHASES',
                   'CASH_ADVANCE', 'PURCHASES_FREQUENCY', 'ONEOFF_PURCHASES_FREQUENCY',
                   'PURCHASES_INSTALLMENTS_FREQUENCY', 'CASH_ADVANCE_FREQUENCY', 'CASH_ADVANCE_TRX',
                   'PURCHASES_TRX', 'CREDIT_LIMIT', 'PAYMENTS', 'MINIMUM_PAYMENTS', 'PRC_FULL_PAYMENT', 'TENURE']]

    # Make a prediction for each row in the CSV file
    predictions = model.predict(features)

    # Convert the predictions to a list
    predictions = predictions.tolist()
    print(predictions)
    return {"predictions": predictions}

feature_names = ['BALANCE', 'BALANCE_FREQUENCY', 'PURCHASES', 'ONEOFF_PURCHASES', 'INSTALLMENTS_PURCHASES',
                 'CASH_ADVANCE', 'PURCHASES_FREQUENCY', 'ONEOFF_PURCHASES_FREQUENCY', 'PURCHASES_INSTALLMENTS_FREQUENCY',
                 'CASH_ADVANCE_FREQUENCY', 'CASH_ADVANCE_TRX', 'PURCHASES_TRX', 'CREDIT_LIMIT', 'PAYMENTS',
                 'MINIMUM_PAYMENTS', 'PRC_FULL_PAYMENT', 'TENURE']

@app.post("/predicttt")
def predict_batch(inputs: List[dict]):
    # Select only the relevant features from the input data
    features = [[input_dict[feat] for feat in feature_names] for input_dict in inputs]

    # Make predictions for all the input samples at once
    predictions = model.predict(features)

    # Convert the predictions to a list
    predictions = predictions.tolist()

    return {"predictions": predictions}

@app.get("/run_job")
def run_job():
    # Loaaad the input CSV file (only the first 100 rows)
    df = pd.read_csv("Data.csv").head(100)
    # Select only the relevant features from the input data
    input_data = df[feature_names]
    # Make a prediction for each row in the CSV file
    predictions = model.predict(input_data)
    # Convert the predictions to a list
    predictions = predictions.tolist()
    # Write the predictions to a new CSV file 
    with open("predictions.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Prediction"])
        for prediction in predictions:
            writer.writerow([prediction])

    return {"message": "Job completed successfully"}


if __name__=="__main__":
    uvicorn.run(app)