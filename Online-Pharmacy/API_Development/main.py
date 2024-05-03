from fastapi import FastAPI, Depends
from pymongo import MongoClient
from models import Products, Users, Pharmacists, CardDetails, Feedback
from typing import Dict, Any
import json
from uuid import UUID, uuid4
from datetime import datetime

app = FastAPI()

DatabaseNname = "Online-Pharmacy"
ProdColName = "ProductDetails"
UserColName = "UserDetails"
PharmacistColName = "PharmacistDetails"
CardColName = "CardDetails"
FeedbackColName = "Feedbacks"

today = datetime.now().strftime("%m-%y")


client = MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.1.5')

db = client[DatabaseNname]
ProdCollection = db[ProdColName]
UserCollection = db[UserColName]
PharmacistCollection = db[PharmacistColName]
CardCollection = db[CardColName]
FeedbackCollection = db[FeedbackColName]


# home
@app.get("/")
async def root():
    return {"Hello" : "Vishv"}


# get all data
@app.get("/products")
async def fetchProducts():
    data_cursor = ProdCollection.find()
    
    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return data_list


# add product data - only admin has access to this
@app.post("/products/add")
async def addProducts(product: Products):
    try:
        ProdCollection.insert_one(product.dict())
    except Exception as e:
        print(e)
    return {"id": product._id}


# get specific product data
@app.get("/products/prod={product_name}")
async def fetchAllProducts(product_name: str):
    data_cursor = ProdCollection.find({
        "ProductName": {
            "$regex": product_name,
            "$options": 'i'
        }
    })

    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return list(data_list)


# get category based product
@app.get("/products/cate={category}")
async def fetchAllProducts(category: str):
    data_cursor = ProdCollection.find({
        "Category": {
            "$regex": category,
            "$options": 'i'
        }
    })

    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return list(data_list)


# user registration
@app.post("/users/add")
async def registerUser(user: Users):
    try:
        UserCollection.insert_one(user.dict())
    except Exception as e:
        print(e)
    return {"id": user._id}


# get user details
@app.get("/users/{userEmail}")
async def getUserDetails(userEmail: str):
    data_cursor = UserCollection.find({
        "UserEmail": {
            "$regex": userEmail,
            "$options": 'i'
        }
    })
    
    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return data_list


# pharamacist registration
@app.post("/pharamacist/add")
async def registerPharamacist(pharamacist: Pharmacists):
    try:
        PharmacistCollection.insert_one(pharamacist.dict())
    except Exception as e:
        print(e)
    return {"id": pharamacist._id}


# get pharamacist details
@app.get("/pharamacist/{phmEmail}")
async def getUserDetails(phmEmail: str):
    
    data_cursor = PharmacistCollection.find({
        "PhmEmail": {
            "$regex": phmEmail,
            "$options": 'i'
        }
    })

    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return list(data_list)


# payment check
@app.get("/paymentCheck/")
async def checkPayment(cardDetails: CardDetails):
    
    data_cursor = CardCollection.find({ "CardNumber": cardDetails.CardNumber })
    
    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    repsonse = False

    try:
        if data_list[0]['Owner'] == cardDetails.Owner:
            if datetime.strptime(data_list[0]['CardExpiry'], '%m-%y') >= datetime.strptime(today, '%m-%y') and data_list[0]['CardExpiry'] == cardDetails.CardExpiry:
                if data_list[0]['CVV'] == cardDetails.CVV:
                    repsonse = True
    except Exception as e:
        print(e)

    return repsonse


# cart add
@app.get("/addCart/{product_id}")
async def checkPayment(product_id: str):
    
    data_cursor = ProdCollection.find({ "_id": product_id })

    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return data_list


# feedback
@app.post("/feedback/")
async def checkPayment(feedback: Feedback):

    response = False
    try:
        FeedbackCollection.insert_one(feedback.dict())
        response = True
    except Exception as e:
        print(e)

    return response