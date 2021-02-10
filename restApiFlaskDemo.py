#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 10:50:57 2021

@author: AditiVerma
In NodeJs
app = express()
app.get('',())
app.post('',())

"""

import json
from flask import Flask,jsonify,request,Response,make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__) 

#establishing connection to DB
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://admin:admin@localhost:3306/devops'

db = SQLAlchemy(app) #share connection


class Product(db.Model):  #Product inherits Model
    __tablename__="pyproducts"
    productId = db.Column(db.Integer,primary_key=True)
    productName = db.Column(db.String(40))
    description = db.Column(db.String(60))
    productCode = db.Column(db.String(40))
    price = db.Column(db.Float)
    starRating = db.Column(db.Float)
    imageUrl = db.Column(db.String(40))
    
    def create(self): #overriding, logical connection establish to DB
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self,productName,description,productCode,price,starRating,imageUrl):
        self.productName = productName
        self.description = description
        self.productCode = productCode
        self.price = price
        self.starRating = starRating
        self.imageUrl = imageUrl
    def __repr__(self): #repr is used for representation
         return "% self.productId"
     
        
     
db.create_all() #method to create all the tables

#ORM-object relational mapping is done below, mapping columns to my object        
class ProductSchema(ModelSchema): #Product Schema inherits Model Schema
    class Meta(ModelSchema.Meta): #nested class in which it inherits ModelSchema.Meta
        model = Product
        sqla_session = db.session#design our code
        
    productId = fields.Number(dump_only=True)
    productName = fields.String(required=True)
    description = fields.String(required=True)
    productCode = fields.String(required=True)
    price = fields.Number(required=True) 
    starRating = fields.Number(required=True) 
    imageUrl = fields.String(required=True)     
        
@app.route('/products',methods=['POST']) #POST API    
def createProduct():
    data = request.get_json()
    product_schema = ProductSchema() #creating obj
    product = product_schema.load(data) #unmarshallowing ie getting json data and passing to product object
    result = product_schema.dump(product.create()) # to inserting value in DB i.e it perform insert query into table  #deserializing i.e converting json to objects
    return make_response(jsonify({"product":result},201)) #201 means obj is created succesfully

@app.route('/products',methods=['GET'])
def getAllProducts():
    get_products = Product.query.all()
    productSchema = ProductSchema(many=True)
    products = productSchema.dump(get_products)
    return make_response(jsonify({"products":products}),200)

@app.route('/products/<int:productId>',methods=['GET'])
def getProductsById(productId):
    get_products = Product.query.get(productId)
    productSchema = ProductSchema()
    product = productSchema.dump(get_products)
    return make_response(jsonify({"products":product},200))

@app.route('/products/<int:productId>',methods=['DELETE']) #int:productId it is dependency injection
def deleteProductsById(productId):
    get_products = Product.query.get(productId)
    db.session.delete(get_products)
    db.session.commit() #it is a CRUD operation i.e why we are doing commit
    return make_response(jsonify({"result":"product deleted"},204))

@app.route('/products/<int:productId>',methods=['PUT']) #int:productId it is dependency injection
def updateProducts(productId):
    data = request.get_json()
    get_products = Product.query.get(productId)
    if data.get('price'):
        get_products.price = data['price']
    db.session.add(get_products)
    db.session.commit()
    
    product_schema = ProductSchema(only=['productId','price'])
    result = product_schema.dump(get_products)
    return make_response(jsonify({"products":result}),200)

@app.route('/products/find/<productName>',methods=['GET']) # QUERY => SELECT * FROM pyproducts where productName=?
def getProductsByName(productName):
    get_products = Product.query.filter_by(productName=productName)
    productSchema = ProductSchema(many=True)
    product = productSchema.dump(get_products)
    return make_response(jsonify({"products":product}),200)

app.run(port=4002) 



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    