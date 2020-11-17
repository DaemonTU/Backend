from flask import render_template,request,Blueprint,redirect,url_for,session,jsonify,flash
from passlib.hash import pbkdf2_sha256
from os import environ
from functools import wraps
import datetime
import uuid
import jwt
def create_blueprint(cluster):
    admin = Blueprint("admin",__name__,url_prefix="/admin")

    def isLoggedIn(f):                  #LOGIN CHECKER
        @wraps(f)
        def inner_wrapper(*args,**kwargs):
            if session.get('token',None) is not None:
                try:
                    jwt.decode(session['token'],environ.get('SECRET_KEY'))
                except jwt.ExpiredSignatureError:
                    return redirect(url_for('admin.admin_login'))
                return f(*args,**kwargs)
            return redirect(url_for('admin.admin_login'))
        return inner_wrapper

    @admin.route("/login",methods=['GET','POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")
            response = cluster.db.admins.find_one({"username" : username})
            if response:
                if(pbkdf2_sha256.verify(password,response["password"])):
                    jwt_encoded = jwt.encode({"username" : response["username"], "exp" : datetime.datetime.utcnow()+datetime.timedelta(days=1)},environ.get("SECRET_KEY"))
                    session["token"] = jwt_encoded
                    print("True")
                    return redirect(url_for('admin.add_members'))
        return render_template('adminLogin.html')

    @admin.route("/member",methods=['GET'])
    @isLoggedIn
    def add_members():
        return render_template('addMembers.html')


    @admin.route("/",methods=['GET','POST'])         #VIEW ADMINS
    @isLoggedIn
    def admin_dash():
        admins = cluster.db.admins.find()
        output = []
        if admins:
            for admin in admins:
                output.append({
                    "username" : admin["username"],
                    "admin_id" : admin["admin_id"]
                })
            return render_template('addAdmin.html',admins= output)
        return render_template('addAdmin.html')

    @admin.route("/delete/<admin_id>",methods=['GET'])         #DELETE ADMIN
    @isLoggedIn
    def admin_delete(admin_id):
        admins = cluster.db.admins.find_one({"admin_id" : admin_id})
        if admins:
            status = cluster.db.admins.delete_one({"admin_id" : admin_id})
            if status:
                flash('Admin deleted successfully','success')
                return redirect(url_for('admin.admin_dash'))
            flash('Admin cannot be deleted','error')
            return redirect(url_for('admin.admin_dash'))

    @admin.route("/add",methods=['GET','POST'])         #CREATE NEW ADMIN
    @isLoggedIn
    def add_admin():
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")
            hashed_pass = pbkdf2_sha256.hash(password)
            response = cluster.db.admins.insert_one({"username" : username, "password" : hashed_pass,"admin_id": str(uuid.uuid4())})
            if response:
                flash('Admin added successfully','success')
                return redirect(url_for('admin.admin_dash'))
            flash('Admin cannot be added','error')
            return redirect(url_for('admin.admin_dash'))
    


    @admin.route("/logout",methods=['GET'])         #LOGOUT ADMIN
    @isLoggedIn
    def logout_admin():
        session.pop('token')
        return redirect(url_for('admin.admin_login'))

    return admin