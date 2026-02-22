from fastapi import FastAPI,HTTPException,Query,status,Depends
from fastapi.security import APIKeyHeader
import pandas as pd
import numpy as np
import joblib
from pydantic import BaseModel,Field
from dotenv import load_dotenv
import os
load_dotenv()
api_key_secret='Hassan007'
env=os.getenv(api_key_secret)
api_header=APIKeyHeader(name=api_key_secret)

def authorized(api_key:str = Depends(api_header)):
    if api_key !=env:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='unauthorized')


app=FastAPI()

class model(BaseModel):
    product: str
    Price: float
    quantity:int
    discounts:int =Field(0,ge=0,le=100)

@app.post('/request service')
def request_service(api_key:str = Depends(authorized),data:model=None):
    total:float=0.0
        
    if len(data.product)>0:
        sub_total=(data.Price*data.quantity)
        discounts_amount=sub_total*(data.discounts/100)
        total=sub_total-discounts_amount
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='please enter ur product')
    return {"status": "success",
            "calculation": {
                "sub_total": sub_total,
                "discount_subtracted": discounts_amount,
                "final_purchase": total}}

@app.post('/payment')
def payment(api_key: str = Depends(authorized), amount: float = Query(gt=0)):
    return {
        "status": "Payment Authorized",
        "transaction_id": "TXN-9928374",
        "amount_captured": amount
    }



