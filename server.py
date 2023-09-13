from flask import Flask, render_template, redirect, url_for, flash,request,jsonify
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from firebase_admin import credentials, initialize_app, storage
from flask_cors import CORS,cross_origin
load_dotenv()

jsonFile = os.environ.get('GETJSON')
cred = credentials.Certificate(jsonFile)
initialize_app(cred, {
    'storageBucket':'photo-671df.appspot.com'
                       
})
bucket = storage.bucket()
app = Flask(__name__)
CORS(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(basedir, "instance/photo.db")
app.config['SECRET_KEY'] = 'goremi'
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATA')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
class Photo(db.Model):
    __tablename__ = "photo"
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255))
    url = db.Column(db.String(255))
with app.app_context():
    db.create_all()
    
   
@app.route('/',methods=['GET'])
@cross_origin()
def main():
    data={'message':'안녕하세요'}
    return jsonify(data)
@app.route('/data')
@cross_origin()
def home():
      photos= db.session.query(Photo).all()

      photo_list = [{'filename': photo.filename, 'url': photo.url} for photo in photos]
      return jsonify(photodata=photo_list)
@app.route('/api',methods=['POST'])
def api():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected video file'
    destination = 'image/' + file.filename
    blob = bucket.blob(destination)
    blob.upload_from_file(file)
    file_url = blob.public_url
    # file_url = client.get_bucket('photo-671df.appspot.com') 
    
    photo=Photo(filename=file.filename,url=file_url)
    db.session.add(photo)
    db.session.commit()
    return jsonify(message=f'{file}uploaded successfully')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5500)
