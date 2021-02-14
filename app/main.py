from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pycaret.regression import *
import pandas as pd
import pickle
import numpy as np
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="templates/")

# app.mount(
#     "/static",
#     StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
#     name="static",
# )
#<!-- <link href="{{ url_for('static', path='/style.css') }}" rel="stylesheet" type='text/css'> -->


model = load_model('deployment_model')
cols = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.get('/predict')
def predict_get(request: Request):
    return templates.TemplateResponse('home.html', context={'request': request, 'pred': ''})

@app.post("/predict")
async def predict_post(request: Request, age: int = Form(...), 
                                    sex: str = Form(...),
                                    bmi: int = Form(...),
                                    children: str = Form(...),
                                    smoker: str = Form(...),
                                    region: str = Form(...)):
    int_features = [age, sex, bmi, children, smoker, region]
    final = np.array(int_features)
    data_unseen = pd.DataFrame([final], columns = cols)
    prediction = predict_model(model, data=data_unseen, round = 0)
    prediction = int(prediction.Label[0])

    return templates.TemplateResponse("home.html", context={'request': request, 'pred': f"Expected Bill will be {'${:,.2f}'.format(prediction)}"})

# curl -X POST "http://127.0.0.1:8000/predict/" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"age\":0,\"bmi\":0}"
