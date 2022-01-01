from flask import Flask, redirect
from flask import Flask, flash
from flask import render_template
from flask import request
from flask import session
from bson.json_util import loads, dumps
from flask import make_response
import database as db
import authentication
import pymongo
import logging
import bcrypt


app = Flask(__name__)
# Set the secret key to some random bytes.
# Keep this really secret!
app.secret_key = b's@g@d@c0ff33!'
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
db = myclient.get_database('order_management')
records = db.customers

logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.INFO)

@app.route("/", methods=['post', 'get'])
def index():
    message = ''
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        user = request.form.get("username")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"username": user})

        if user_found:
            message = 'This user already exists'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            user_input = {'username': user, 'password': password1, 'first_name':first_name, 'last_name':last_name}
            records.insert_one(user_input)

            user_data = records.find_one({"username": user})
            new_user = user_data['username']

            return render_template('dashboard.html', username=new_user)
    return render_template('index.html')

#end of code to run it
if __name__ == "__main__":
  app.run(debug=True)

#app route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/scheduled', methods=['GET', 'POST'])
def scheduled():
    return render_template('scheduled.html')

@app.route('/cancelled', methods=['GET', 'POST'])
def cancelled():
    return render_template('cancelled.html')

#app route for authentication
@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    username = request.form.get('username')
    password = request.form.get('password')

    is_successful, user = authentication.login(username, password)
    app.logger.info('%s', is_successful)
    if(is_successful):
        session["user"] = user
        return redirect('/dashboard')
    else:
        return render_template('loginfailed.html')
#THIS MAKES IT WORK YEHEY for wrong users and no field input
    try:
        return users[USERNAME]
    except KeyError:
        return render_template('loginfailed.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

#app route logout
@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', page="Dashboard")

@app.route("/changepassword",methods=["GET","POST"])
def changepassword():
    username = session["user"]["username"]
    password = db.get_password(username)
    currentpassword = request.form.get("currentpassword")
    newpassword = request.form.get("newpassword")
    updatepassword = None
    error = None

    if currentpassword == None:
        print(currentpassword)
        error=None
    elif currentpassword == password:
        print(currentpassword)
        updatepassword=db.update_password(username,newpassword)
    elif currentpassword != password:
        print(currentpassword)
        error="Current Password Does Not Match."

    return render_template('changepassword.html', page="Change Password",updatepassword=updatepassword,error=error)
