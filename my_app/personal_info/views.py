from my_app import api
from flask_restx import Resource, Api, fields
# from .info_utils import get_account_balance, m2mtransaction, save_transaction
from flask import jsonify, Blueprint
from ..auth.models import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import decode_token

from flask import request, redirect, flash, render_template

from my_app import db

import os

personal_info = Blueprint('personal_info', __name__)

@api.route('/user/<int:id>')
class Userhome(Resource):
    def get(self, id):
        existing_user = User.query.filter_by(id=id).first()
        if not existing_user:
            return {"message": "User does not exist"}, 400
        return jsonify(existing_user)
    


@api.route("/user/gen_confirmation")
class Gen_email_confirmation(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, additional_claims={"confirm": True}, expires_delta=datetime.timedelta(seconds=3600))

        ##email_verification("goksucanerkoc@gmail.com", access_token)
        print(access_token)
        return jsonify({"message": "confirmation token sent"})


@api.route("/user/verify-email/<token>")
class Emailverification(Resource):
    @jwt_required()
    def get(self, token):
        user_identity = get_jwt_identity()
        current_user = User.query.filter_by(national_identity_number=user_identity).first()
        decoded_token = decode_token(token)
        
        if decoded_token['sub'] == user_identity and decoded_token['confirm']:
            return jsonify({"message": "user confirmed"})
        return jsonify({"message": "invalid confirmation token"})



@api.route('/user/phone-verification')
class Phone_verification(Resource):
    def get(self):
        return {'hello': 'world'}
    


@api.route('/user/terms_and_conditions')
class Terms_and_conditions(Resource):
    def get(self):
        return {'hello': 'world'}
    
@api.route('/user/id_verification')
class Document_verification(Resource):
    def post():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                pepo = os.path.join(app.config['UPLOAD_FOLDER'], f"{current_user.id}/")
                f = os.makedirs(pepo, exist_ok=True)
                file.save(os.path.join(pepo, filename))

                user_file = Authfiles(id_front_file= pepo, user_id=current_user.id, id_back_file=pepo)
                db.session.add(user_file)
                db.session.commit()
                return  "success"
        return render_template('file-upload.html')