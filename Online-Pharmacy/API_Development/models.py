from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

class Gender(str, Enum):
    male = "Male"
    female = "Female"


class Products(BaseModel):
    _id: Optional[str] = uuid4()
    ProductImage: str
    ProductName: str
    ProductPrice: str
    ProductDescription: str
    ProductRatings: str
    Category: str
    #ProductManufactorer: str
    #ProductComposition: str
    #ProductUse: str
    #ProductBenefits: str
    #ProductSideEffects: str


class OrderProducts(BaseModel):
    Products: Products
    Quantity: int


class Orders(str, Enum):
    OrderId: Optional[str] = uuid4()
    OrderDate: str
    Total: float
    Products: List[OrderProducts]


class PersonDetails(BaseModel):
    _id: Optional[UUID] = uuid4()
    Email: str
    ContactNumber: str
    FName: str
    LName: str
    Street: str
    City: str
    State: str
    Pincode: str
    Gender: Gender
    Orders: List[Orders]


class Users(PersonDetails):             #inheritance
    DateofBirth: str
    Gender: Gender
    Orders: List[Orders]


class Pharmacists(PersonDetails):
    Store: str


class CardDetails(BaseModel):
    CardType: str
    Owner: str
    CardNumber: str
    CardExpiry: str
    CVV: str


class Feedback(BaseModel):
    Name: str
    Email: str
    Message: str