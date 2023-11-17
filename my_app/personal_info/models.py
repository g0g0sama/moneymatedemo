from my_app import db


class Personal_info(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    address = db.Column(db.Float, nullable=True)
    country = db.Column(db.String(255), nullable =True) #find the iso codes and country list by language
    city = db.Column(db.String(255), nullable = True) #find the cities by country
    ##national_identity = db.Column(db.enum("TC vatandaşı", "Yabancı uyruklu"), default="TC vatandaşı")
    birth_month = db.Column(db.Integer, nullable=True)
    birth_day = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __init__(self,  address, country, city, 
           user_id, birth_month, birth_day, user_file_path):
        self.address = address
        self.country = country
        self.city = city
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.user_file_path = user_file_path
        self.user_id = user_id