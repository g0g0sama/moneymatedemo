from my_app import db
from datetime import datetime


class Personal_info(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    address = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    country = db.Column(db.String(255), nullable =True) #find the iso codes and country list by language
    city = db.Column(db.String(255), nullable = True, default= None) #find the cities by country
    ##national_identity = db.Column(db.enum("TC vatandaşı", "Yabancı uyruklu"), default="TC vatandaşı")
    birth_month = db.Column(db.Integer, nullable=True, default= None)
    birth_day = db.Column(db.Integer, nullable=True, default= None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __init__(self,user_id):
        self.user_id = user_id

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_name = db.Column(db.String(255), nullable=True, default= None)
    address = db.Column(db.String(255), nullable=True, default= None)
    country = db.Column(db.String(255), nullable =True) #find the iso codes and country list by language
    city = db.Column(db.String(255), nullable = True, default= None) #find the cities by country
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __init__(self,user_id):
        self.user_id = user_id

class Termsandconditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kvkk = db.Column(db.Boolean, nullable=True, default= False)
    terms = db.Column(db.Boolean, nullable=True, default= False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    success = db.Column(db.Boolean, nullable=True, default= False)

class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id_front = db.Column(db.String(255), nullable=True, default= None)
    user_id_back = db.Column(db.String(255), nullable=True, default= None)
    success = db.Column(db.String(255), nullable=True, default= False)






