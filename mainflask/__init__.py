from flask import Flask, render_template,Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from mainflask.blinkdetect import gen_frames
import time

timeout = time.time() + 10  # 10 s

app = Flask(__name__)
app.config["SECRET_KEY"]='123456789gowrinandana'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from mainflask import routes



@app.route('/blink')
def index():

    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    while time.time() < timeout:
  
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
