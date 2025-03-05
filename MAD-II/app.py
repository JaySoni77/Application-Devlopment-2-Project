import os
import pytz
from datetime import datetime, timedelta

from flask import Flask, redirect, url_for,session, jsonify, send_file
from flask import render_template
from flask import request

from flask_security.utils import verify_and_update_password
from flask_security import Security, current_user, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_security import login_required, roles_accepted, login_user,  hash_password, LoginForm, auth_required

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column , Integer , String, ForeignKey

from flask_restful import Resource,Api, marshal
from flask_cors import CORS

from datetime import datetime
from jinja2 import Template
import flask_excel as excel

from time import perf_counter_ns

from celery import Celery
from celery.schedules import crontab
from celery.result import AsyncResult
from flask_caching import Cache
from werkzeug.utils import secure_filename
# from flask import current_app as app

#celery setup

celery = Celery("app")

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
        
#############################################
#app setup
app = Flask(__name__, template_folder="Templates")
current_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(current_dir,"Nature's Nourish.db")
api = Api(app)
CORS(app, supports_credentials=True)

db = SQLAlchemy(app)
app.app_context().push()
excel.init_excel(app)


#configurations

app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_PASSWORD_SALT'] = 'another-super-secret'
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_UNAUTHORISED_VIEW'] = None
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_LOGIN_TEMPLATE'] = 'login.html'
app.config['UPLOAD_FOLDER'] = 'static'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authorization'
app.config['SECURITY_TRACKABLE'] = False
app.config["CELERY_BROKER_URL"] = "redis://localhost:6379/1"
app.config['CELERY_RESULT_BACKEND'] = "redis://localhost:6379/2"
app.config['CELERY_TASK_RESULT_EXPIRES'] = 3600
# app.config['CELERY_TIMEZONE'] = 'Asia/Calcutta'
app.config["CACHE_TYPE"] = "redis"
app.config['CACHE_REDIS_HOST'] = "localhost"
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 3
app.config['CACHE_DEFAULT_TIMEOUT'] = 300


cache = Cache(app)
cache.init_app(app)


app.app_context().push()


celery.conf.update(
    broker_url = app.config["CELERY_BROKER_URL"],
    result_backend = app.config['CELERY_RESULT_BACKEND'],
    timezone='Asia/Kolkata'
)

# Define models

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer,autoincrement = True, primary_key=True)
    full_name = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,backref=db.backref('users', lazy='subquery'))
    fs_uniquifier = db.Column(db.String, unique=True, nullable=False)

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Catagory(db.Model):
    __tablename__ = 'catagory'
    catagory_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String())

class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    expiry_date = db.Column(db.String())
    price = db.Column(db.Integer())
    unit = db.Column(db.String())
    catagory_id = db.Column(db.Integer(),ForeignKey("catagory.catagory_id"))
    image_name = db.Column(db.String())
    description = db.Column(db.String())
    quantity = db.Column(db.Integer())
    category = db.relationship('Catagory', backref='products', lazy='subquery')

class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(),ForeignKey ("user.user_id"))
    product_id = db.Column(db.Integer(),ForeignKey ("product.product_id"))
    quantity = db.Column(db.Integer())
    price = db.Column(db.Integer())
    product = db.relationship('Product', backref='carts', lazy='joined')

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(),ForeignKey ("user.user_id"))
    total = db.Column(db.Integer())
    order_date =  db.Column(db.DateTime, default=datetime.utcnow)
    delivery_date = db.Column(db.Numeric())
    status = db.Column(db.String())
    receiver = db.Column(db.String(50))
    address = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    pin_code = db.Column(db.Integer())
    order_details = db.relationship('Order_Details', backref='order', lazy='dynamic')
    
class Order_Details(db.Model):
    __tablename__ = 'order_details'
    order_details_id = db.Column(db.Integer(), primary_key=True)
    order_id = db.Column(db.Integer(), ForeignKey ("order.order_id"))
    product_id = db.Column(db.Integer(),ForeignKey ("product.product_id"))
    product_name = db.Column(db.String(), ForeignKey ("product.name"))
    quantity = db.Column(db.Integer())
    per_unit_price = db.Column(db.Integer())
    price = db.Column(db.Integer())
    product = db.relationship('Product', foreign_keys=[product_id], backref='order_details')

class CreateReq(db.Model):
    __tablename__ = 'createReq'
    request_id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), ForeignKey("user.user_id"))
    name = db.Column(db.String())
    description = db.Column(db.String())
    message = db.Column(db.String())
    user = db.relationship('User', lazy='subquery')

class DeleteReq(db.Model):
    __tablename__ = 'deleteReq'
    dr_id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), ForeignKey("user.user_id"))
    category_id = db.Column(db.Integer(), ForeignKey("catagory.catagory_id"))
    category = db.relationship('Catagory', lazy='subquery')
    user = db.relationship('User', lazy='subquery')

class EditReq(db.Model):
    __tablename__ = 'editReq'
    request_id = db.Column(db.Integer(), primary_key = True)
    user_id = db.Column(db.Integer(), ForeignKey("user.user_id"))
    category_id = db.Column(db.Integer(), ForeignKey("catagory.catagory_id"))
    name = db.Column(db.String())
    description = db.Column(db.String())
    message = db.Column(db.String())
    user = db.relationship('User', lazy='subquery')


class LoginReq(db.Model):
    __tablename__ = 'loginReq'
    lr_id = db.Column(db.Integer(), primary_key = True)
    full_name = db.Column(db.String())
    email = db.Column(db.String())
    message = db.Column(db.String())
    # user = db.relationship('User', lazy='subquery')


db.create_all()
app.app_context().push()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security=Security(app, user_datastore)


#Controllers
import task

@app.route('/')
def home():
        # return render_template('index.html')
        return ("Please Visit  http://localhost:8080/#/")

# report test
@app.route('/report')
def report():
    user = 4
    current_date = datetime.now()
    last_day = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day = (last_day - timedelta(days=1)).replace(day=1)
    user_obj = User.query.filter_by(user_id = user).first()
    orders = Order.query.filter(Order.user_id == user and (Order.order_date >= first_day, Order.order_date < last_day)).all()
    grand_total = 0
    for i in orders:
        grand_total = grand_total + i.total 
    return render_template('pdf-report.html', user_obj = user_obj, orders = orders, grand_total = grand_total)
##################################################################################################################
# Asynchronous Csv Generator And Download end point

@auth_required('token')
@roles_accepted('storeManager')
@app.get('/download_csv')
def download_csv():
        t = task.download_csv_file.delay()
        return jsonify({"task-id": t.id})

@app.get('/download_csv/<task_id>')
def download(task_id):
        res = celery.AsyncResult(task_id)
        if res.ready():
            filename = res.result
            return send_file(filename, as_attachment = True)
        else:
            return jsonify({"message":"Task Pending"}),404

####################################################################################################################
#API

from flask_restful import Resource, reqparse
from flask_restful import fields,marshal_with
from werkzeug.exceptions import HTTPException
from flask import make_response
import json
# import optimize

class NotFoundError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code":error_code, "error_message":error_message}
        self.response = make_response(json.dumps(message), status_code)

class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message = {"error_code":error_code, "error_message":error_message}
        self.response = make_response(json.dumps(message), status_code)



########################################## Api for user login and signup ##########################################
class user_login(Resource):
    def post(self):
        email= request.get_json()["email"]
        password= request.get_json()["password"]
        user=User.query.filter_by(email=email).first()
        if user:
            if verify_and_update_password(password, user):
                #login_user(user)
                Role = "User"
                if user.roles != []:
                    Role = user.roles[0].name
                return {"Token":user.get_auth_token(), "Role": Role, "Email": user.email}
            else: 
                return {"message":"Incorrect password"}, 401
        else:
            return {"message":"Incorrect email or password"}, 401
    # def get(self):
    #     return 

    def put(self):

        full_name = request.get_json()["name"]
        email = request.get_json()["email"]
        password = request.get_json()["password"]
        c_password = request.get_json()["confirmPassword"]
        check=User.query.filter_by(email=email).first()
        if check:
            return ({'message':'email you entered already belongs to an account. Try another email.'}), 400
        else:
            if password == c_password :
                user_datastore.create_user(email=email,full_name=full_name,password=hash_password(password))
                db.session.commit()
                return {"message": "Signup Successful."}
            if password != c_password:
                return {'message':'Password and Confirm password are not same'}, 401
    

api.add_resource(user_login, "/custom_login")

########################################## Request Admin to Grant "Manager" Role ##########################################
view_order = {"order_details_id": fields.Integer, "order_id": fields.Integer, "product_id": fields.Integer,
                    "product_name": fields.String, "quantity": fields.Integer, "price": fields.Integer,
                    "image_name": fields.String(attribute=lambda x:x.product.image_name)}
class req(Resource):
    def post(self):
        try:
            email= request.get_json()["email"]
            pw= request.get_json()["password"]
            message= request.get_json()["message"]
            user=User.query.filter_by(email=email).first()
            lr = LoginReq.query.filter_by(email=email).first()
            if user:
                if lr:
                    return{"message": "Request is Already Sent Wait For Admin's Approval."}
                if verify_and_update_password(pw, user):
                    if user.roles == "storeManager":
                        return{"Error": "You Are Already Manager. Login To Access Manager Dashboard"}
                    else:
                        name = user.full_name
                        e = LoginReq(full_name = name, email = email, message = message)
                        db.session.add(e)
                        db.session.commit()
                        return {"message":"Your Request Has Been Sent To Admin. Wait For Admin's Approval."}
                else: 
                    return {"Error":"Incorrect password"}
            else:
                return {"Error":"Please Signup And Generate Credentials First."}
        except Exception as a:
            print(a)
            print('hello')
            return{'Error':str(a)}
        
    # User order page (/req, get)#
    @auth_required("token")
    def get (self):
        try:
            userID=current_user.user_id
            d = Order.query.filter_by(user_id = userID).order_by(Order.order_id.desc()).all()
            if d:
                i = marshal(d,order_list)
                return i
            if not d: 
                return {"message":"No Order Found"}
        except Exception as e:
            print(e)
            return {"message": str(e)}
    
    @auth_required('token')
    def put(self,id):
        try:
            result = Order_Details.query.filter_by(order_id = id).all()
            if result :
                i = marshal(result, view_order)
                return i
            elif not result:
                return {"message": "No Result Found!"}
        except Exception as e:
            print(e)
            return {"message": str(e)}

api.add_resource(req, "/req", "/req/<int:id>")
####################################################################################################################
############################################## Api for User page ###################################################
####################################################################################################################

#output formate
op_home = {
    "product_id":fields.Integer,
    "name" :fields.String,
    "expiry_date" : fields.String,
    "price" : fields.Integer,
    "unit" : fields.String,
    "catagory_id" : fields.Integer,
    "image_name" : fields.String,
    "description" : fields.String,
    "quantity" : fields.Integer
}
op_category_page ={
    "catagory_id" : fields.Integer,
    "name" : fields.String,
    "description" : fields.String

}
op_product_by_category = {
    "product_id" : fields.Integer,
    "name" : fields.String,
    "expiry_date" : fields.String,
    "price" : fields.Integer,
    "unit" : fields.String,
    "catagory_id" : fields.Integer,
    "image_name" : fields.String,
    "description" :fields.String ,
    "quantity" : fields.Integer,
    "catagory" : fields.String(attribute=lambda x: x.category.name),
    "catagory description" : fields.String(attribute=lambda x:x.category.description)
    }
cart_product = {
    "cart_id" : fields.Integer,
    "quantity" : fields.Integer,
    "price" : fields.Integer,
    "product_id" : fields.Integer,
    "name" : fields.String(attribute=lambda x:x.product.name),
    "expiry_date" : fields.String(attribute=lambda x:x.product.expiry_date),
    "catagory_id" : fields.Integer(attribute=lambda x:x.product.catagory_id),
    "image_name" : fields.String(attribute=lambda x:x.product.image_name),
    "description" :fields.String(attribute=lambda x:x.product.description) ,
}
order_list ={
    "order_id": fields.Integer, "user_id" : fields.Integer, "total" : fields.Integer, "order_date" : fields.String,
                    "delivery_date" : fields.String, "status" : fields.String, "receiver" :fields.String, "address" : fields.String,
                    "city" : fields.String , "state" : fields.String, "pin_code" : fields.Integer}


#Create parser
create_parser = reqparse.RequestParser()
create_parser.add_argument('product_id')


class user_page(Resource):

    # User home page  (/api, get) #

    @auth_required("token")
    @cache.cached(timeout=50, key_prefix='Get all Products.')
    #@marshal_with(op_home)
    def get(self):
        print("inside api for user home page.")
        display_product = Product.query.all()
        if display_product:
            ans = marshal(display_product, op_home)
            return ans
        else:
            return {'message': 'No Product Found!'}
        # i = marshal(op_home, display_product)
        #     return i
        # elif not display_product:
        #     return {"Message": "No product is available"}
    
    # User Product page (/api, post)#

    @auth_required("token")
    #@marshal_with(op_home)
    def post(self):

        data= request.get_json()["id"]
        v = data['id']
        print(v)
        
        display_item = Product.query.filter_by(product_id=v).first()
        if display_item:
            i = marshal(display_item,op_product_by_category)
            return i
        else:
            print('else block')
            return {'error': 'Product not found'}, 404
        
    # User category page (/api, put) #
    @auth_required("token")
    @cache.cached(timeout=50, key_prefix='Get All Categories')
    def put(self):
        print("inside cetegory api")
        ctgry = Catagory.query.all()
        if ctgry:
            i = marshal(ctgry, op_category_page)
            return i
        else:
            return 


    
api.add_resource(user_page, "/api","/api/<string:product_id>", "/api/<int:catagory_id>")
#########################################Api for editing user page ##################################################

class edit (Resource):

    # User product by category page (/edit, get/category_id) #
    @auth_required("token")
    def get (self, id):
        cProduct=Product.query.filter_by(catagory_id=id).all()
        if cProduct:
            i = marshal(cProduct, op_product_by_category)
            return i
        else:
            return
        
        
    #edit quantuty in cart page (/edit, post) #
    @auth_required("token")
    #@marshal_with(cart_product)
    def post (self):

        quantity=request.get_json()["q"]
        cart_id=request.get_json()["cId"]
        product_id = request.get_json()["productId"]

        product = Product.query.get(product_id)
        p=product.price
        price=int(quantity)*int(p)

        try:
            cart = Cart.query.get(cart_id)
            cart.quantity = quantity
            cart.price = price
            db.session.commit()
        except Exception as e:
            print(e)
            return {"Error": e}
        else:
            return {"Message": "Quantity is updated"} 
        
    # Delete Item from cart((/edit, delete)) #
    @auth_required("token")
    #@marshal_with()
    def delete (self):
        cart_id=request.get_json()["cId"]

        try:
            cart = Cart.query.get(cart_id)
            db.session.delete(cart)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'Error': e}
        else: 
            return {"message": "Item removed successfully"}


api.add_resource(edit, "/edit", "/edit/<int:id>")

######################################### Api for buying ###########################################################

class buy(Resource):

    #User cart page (/buy, get) #
    @auth_required("token")
    def get (self):
        # userEmail = request.get_json()["userEmail"]
        # currentUser = User.query.filter_by(email = userEmail).with_entities(User.user_id).scalar()
        currentID = current_user.user_id
        start = perf_counter_ns()
        c = Cart.query.filter_by(user_id = currentID).all()
        # c =  cart_cache(currentID)
        end = perf_counter_ns()
        print("Time-Taken", end-start)
        if c:
            i = marshal(c, cart_product)
            return i
        else: 
            return 

    # add to cart (/buy , put) #
    @auth_required("token")
    def put(self):
        pId = request.get_json()["id"]
        quan = request.get_json()["q"]
        userID = current_user.user_id
        p = Product.query.get(pId)
        unitPrice = p.price

        price = unitPrice*quan

        cart=Cart(product_id=pId, price=price, user_id=userID, quantity=quan)
        db.session.add(cart)
        db.session.commit()
        return {"message": "product is added into cart"}, 200

    # buying (/buy, post) #
    @auth_required("token")
    def post(self):

        userID = current_user.user_id
        out_of_stock=""
        inStock = ""
        samay = pytz.timezone('Asia/Kolkata')
        order_date = datetime.now(samay)
        status = "To be updated soon"

        order_data = request.get_json()
        # Extract individual fields
        info = order_data.get('info', {})
        receiver = info.get('receiver', None)
        address = info.get('address', None)
        city = info.get('city', None)
        state = info.get('state', None)
        pin_code = info.get('pincode', None)
        contact_number = info.get('contact_number', None)

        c = Cart.query.filter_by(user_id = userID).all()
        if not c :
            return {"Error" : "Can't Place empty order"}, 200
        
        #add into order table
        order=Order(user_id=userID, order_date=order_date, receiver=receiver,
                     address=address, city=city, state=state, pin_code=pin_code, status = status)
        db.session.add(order)
        db.session.commit()

        #Get generated order_id
        order_id=order.order_id

        
        for pro in c:
               
            productId= pro.product_id
            name=pro.product.name
            quan=pro.quantity
            pr=pro.price
        
            calculate_total = 0
            p = Product.query.filter_by(product_id=productId).first()
            if p.quantity >= quan:
                order=Order_Details(product_id=productId, quantity=quan, price=pr, order_id=order_id, product_name=name)
                p.quantity=p.quantity-(int(quan))                    
                db.session.add(order)
                db.session.commit()
                calculate_total = calculate_total + pr
                if inStock != "" :
                    inStock = inStock + ", " + name
                else:
                    inStock = name
            else:
                if out_of_stock != "":
                    out_of_stock=out_of_stock+ ", " +name
                else:
                    out_of_stock = name
                
        p = Order.query.filter_by(order_id = order_id).first()
        p.total = calculate_total
        db.session.commit()
        
        Cart.query.filter_by(user_id=userID).delete()
        db.session.commit()
        inStock = inStock.split(',')
        out_of_stock = out_of_stock.split(',')
        message = ""
        
        if out_of_stock != [""] and inStock != [""] :
            message += f'Your order for "{",".join(inStock)}" is placed. and Your order for "{",".join(out_of_stock)}" couldn\'t be placed as items are unavailable.'
            return message, 200
        if out_of_stock == [""] and inStock != [""] :
            message += f'Your order for "{",".join(inStock)}" is placed.'
            return message , 200
        if inStock == [""] and out_of_stock != [""] :
            message += f'Your order for "{",".join(out_of_stock)}" couldn\'t be placed as items are unavailable.'
            Order.query.filter_by(order_id = order_id).delete()
            db.session.commit()
            return message, 201
        else: 
            message = "invalid request"
            return message, 400

api.add_resource(buy, "/buy","/buy/<int:producId>/<int:q>")   


####################################################################################################################
######################################### Api for Store Manager #####################################################
####################################################################################################################

# CRUD operation on product
class productCRUD(Resource):

    # home page of storeManager (/productCRUD, get)
    @auth_required("token")
    @roles_accepted("storeManager")
    def get(self):
        start = perf_counter_ns()
        # display_product = mAllProduct()
        display_product =Product.query.all()
        end = perf_counter_ns()
        print("Time-Taken", end-start)
        if display_product:
            a = marshal(display_product, op_home)
            return a
        else:
            return
        
    
    # add product (/product, post)
    @auth_required("token")
    @roles_accepted('storeManager')   
    def post (self):
            try:
                # Access form data using request.form
                name = request.form.get('name')
                price = int(request.form.get('price'))
                quantity = int(request.form.get('quantity'))
                unit = request.form.get('unit')
                print("debuging.......!!!!")
                print(unit)
                category = request.form.get('category')
                expiryDate = request.form.get('expiryDate')
                description = request.form.get('description')

                # Save the image
                if 'image' in request.files:
                    image = request.files['image']
                    image_filename = image.filename  # Adjust the file naming as needed
                    image_path = os.path.join(os.path.dirname(__file__), 'front-end/public/img', image_filename)
                    image.save(os.path.join(image_path))

                if not 'image' in request.files:
                    return {'Error': 'Image requires.'}
                # Save product data to the database or perform other processing...
                product = Product(
                    name = name,
                    expiry_date = expiryDate,
                    price = price,
                    unit = unit,
                    catagory_id = category ,
                    image_name=image.filename,
                    description = description,
                    quantity = quantity
                )
                db.session.add(product)
                db.session.commit()
                # Respond with success message
                return {'message': 'Product created successfully'}
            except Exception as e:
                # Handle any exceptions and respond with an error message
                print(e)
                return {'Error': str(e)}
            

    # edit product (/product, put) 
    @auth_required("token")
    @roles_accepted('storeManager')
    def put(self):

        try:    
            pId = request.form.get('product_id')
            print(pId)
            prdct = Product.query.filter_by(product_id = pId).first()
            if not prdct :
                return {"Error": "Product not found"}, 400
        
            if 'image' in request.files:
                    image = request.files['image']
                    image_filename = image.filename  # Adjust the file naming as needed
                    image_path = os.path.join(os.path.dirname(__file__), 'front-end/public/img', image_filename)
                    image.save(os.path.join(image_path))
        
            name = request.form.get('name')
            price = int(request.form.get('price'))
            quantity = int(request.form.get('quantity'))
            unit = request.form.get('unit')
            category = request.form.get('category')
            expiryDate = request.form.get('expiryDate')
            description = request.form.get('description')

            prdct.name=name
            prdct.expiry_date=expiryDate
            prdct.price=price
            prdct.unit=unit
            prdct.catagory_id=category
            prdct.description=description
            prdct.quantity=quantity

            db.session.commit()

        except Exception as e:
            print(e)
            return {"Error": e}
        else:
            return {"message": "Product updated Successfully!"}  

    # delete product (/product, delete) 
    @auth_required("token")
    @roles_accepted('storeManager')   
    def delete(self, productId):
        try:
            # pId = request.get_json()["pID"]
            prdct = Product.query.get(productId)
            q = Order_Details.query.filter_by(product_id = productId).first()

            if q:
                print("solve")
                return {"Error": "Product can't be deleted as there are orders connected with it."}
            db.session.delete(prdct)
            db.session.commit()
        except Exception as e:
            print (e)
            return {"error": str(e)}
        else:
            return {"Message": "Product deleted successfully."}


api.add_resource(productCRUD, "/productCRUD", "/productCRUD/<int:productId>")

######################################### Api for out of stock product,all orders #######################################

class manager(Resource):

    # out of stock product (/manager, get)

    @auth_required("token")
    @roles_accepted('storeManager')
    # @marshal_with(op_home)
    def get(self):
        display_product = Product.query.filter_by(quantity=0).all()
        if display_product:
            i = marshal(display_product, op_home)
            return i
        elif not display_product:
            return 

    # all orders (/manager, post)
    @auth_required("token")
    @roles_accepted("storeManager")
    def post(self):
        orders = Order.query.order_by(Order.order_date.desc()).all()
        if orders:
            i = marshal(orders, order_list)
            return i
        else: 
            return

    # Product page for manager(/manager, put)
    @auth_required("token")
    @roles_accepted('storeManager')
    def put(self, productId):
        display_item = Product.query.filter_by(product_id=productId).first()
        if display_item:
            a = marshal (display_item, op_product_by_category)
            return a
        else: 
            return{'message':'Something Went Wrong!'}
        

    def delete(self):
        pass

api.add_resource(manager, "/manager", "/manager/<int:productId>")

###################################################################################################################

class managerWork(Resource):
    # View Order
    @auth_required('token')
    @roles_accepted('storeManager')
    def get(self, id):
        try:
            result = Order_Details.query.filter_by(order_id = id).all()
            if result :
                i = marshal(result, view_order)
                return i
            elif not result:
                return {"message": "No Result Found!"}
        except Exception as e:
            print(e)
            return {"message": str(e)}
    
    #update status
    @auth_required('token')
    @roles_accepted('storeManager')
    def post(self):
        try:
            message = request.get_json()['status']
            orderId = request.get_json()['orderId']
            order = Order.query.get(orderId)
            order.status = message
            db.session.commit()
        except Exception as e:
            print(e)
            return {"ErRoR": str(e)}
        else:
            return {"message": "Status is updated"}


    # Delete order
    @auth_required('token')
    @roles_accepted('storeManager')
    def delete(self):
        order_id = request.get_json()['orderId']
        try:
            Order_Details.query.filter_by(order_id = order_id).delete()
            Order.query.filter_by(order_id = order_id).delete()
            db.session.commit()
        except Exception as e:
            print(e)
            return {"ErRoR": str(e)}
        else:
            return {"message": "Order is Deleted."}
    
    #Update quantity of out of stock product
    @auth_required('token')
    @roles_accepted('storeManager')
    def put(self):
        id = request.get_json()['productId']
        quantity = request.get_json()['quantity']
        product = Product.query.get(id)
        try: 
            if product:
                product.quantity = quantity
                db.session.commit()
        except Exception as e:
            return {"ErRor": str(e)}
        else: 
            return {"message": "Quantity is Updated"}, 200

api.add_resource(managerWork, "/managerWork", "/managerWork/<int:id>")

###################################################################################################################
################################################## Api for Admin ###################################################
######################################### Api for crud operatoin on category #######################################

#output formate
output_fields = {
    "catagory_id":fields.Integer,
    "name" :fields.String,
    "description" : fields.String
}
user_list = {
    "name": fields.String,
    "email": fields.String,
    "role" : fields.String(attribute=lambda x:x.roles.name),
}

#Create parser
create_parser = reqparse.RequestParser()
create_parser.add_argument('name')
create_parser.add_argument('description')

update_parser = reqparse.RequestParser()
update_parser.add_argument('name')
update_parser.add_argument('description')

#Api for crud operatoin on category 
class categoryCRUD(Resource):
    @auth_required('token')
    @roles_accepted('Admin')
    def get(self):
        list = Catagory.query.all()
        if list:
            a = marshal(list, output_fields)
            return a
        else: 
            return
    
    @auth_required('token')
    @roles_accepted('Admin')    
    def post(self):
        try:
            name =request.get_json()['name']
            description =request.get_json()['description']
            query = db.session.query(Catagory).filter(Catagory.name == name).first()
            if query:
                return {"ErRor": "Category already exists on this name."}
            
            new_category = Catagory(name = name, description = description)
            db.session.add(new_category)
            db.session.commit()
        
        except Exception as e:
            print(e)
            return {'Error': str(e)}
        else:
            return {"message": "Category is created"}
            
        

        # if name is None:
        #     raise BusinessValidationError(status_code=400, error_code= 101, error_message="name is required" )

        # if description is None:
        #     raise BusinessValidationError(status_code=400, error_code= 102, error_message="description is required" )
        
        # if query:
        #     raise BusinessValidationError(status_code=400, error_code= 103, error_message="duplicate name")
        
    @auth_required('token')
    @roles_accepted('Admin')
    def put(self):
        try:
            id = request.get_json()['id']
            name =request.get_json()['name']
            description =request.get_json()['d']
            query = Catagory.query.get(id)
            if not query:
                return {"ErRoR": "Category Not Found!"}
            namecheck = Catagory.query.filter_by(name = name).filter(Catagory.catagory_id != id).first() 
            if namecheck:
                return {"ErRoR": "Name Already Exists Try Another Name"}
            query.name = name
            query.description = description
            db.session.commit()
        
        except Exception as e:
            print(e)
            return {'Error': str(e)}
        else:
            return {"message": "Changes In Category Is Saved"}
    
    def delete(self):
        try:
            id = request.get_json()['catagoryId']
            category = Catagory.query.get(id)
            if category is None:
                return {"message": "Category Not Found"}
            p = Product.query.filter_by(catagory_id = category.catagory_id).first()
            if p :
                return {"message": "Can't delete category. As there are product in this category"}
            db.session.delete(category)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'Error': str(e)}
        else: 
            return {"message": "Category Deleted Successfully"}

        #delete product associated with this category
        #Product.query.filter_by(catagory_id = q.catagory_id).delete()




    # def get(self):
    #     email= request.get_json()["email"]
    #     password= request.get_json()["password"]
    #     user=User.query.filter_by(email=email).first()
    #     if user:
    #         if verify_and_update_password(password, user):
    #             login_user(user)
    #             Role = "User"
    #             if user.roles != []:
    #                 Role = user.roles[0].name
    #             return {"Token":user.get_auth_token(), "Role": Role}

api.add_resource(categoryCRUD, "/categoryCRUD", "/categoryCRUD/<string:name>")

###################################################################################################################
###################################################################################################################

class Admin(Resource):
    # All users
    @auth_required('token')
    @roles_accepted('Admin')
    def get(self):
        try:
            users = User.query.all()
            users = marshal(users, user_list)
        except Exception as e:
            print(e)
            return {"ErRoR": str(e)}
        else:
            return users
        
    @auth_required('token')
    @roles_accepted('Admin')
    def put(self, id):
        try:
            c = Catagory.query.filter_by(catagory_id = id).first()
            if not c:
                return{"error": "Category Not Found!"}
            ca = marshal(c, output_fields)
        except Exception as e:
            print(e)
            return {"ErRoR": str(e)}
        else:
            return ca

api.add_resource(Admin, "/admin", "/admin/<int:id>")

###################################################################################################################
###################################################################################################################

class request_page(Resource):
    #shows categorys to manager
    @marshal_with(output_fields)
    @auth_required('token')
    @roles_accepted('storeManager')
    def get(self):
        #get category name
        q = Catagory.query.all()

        if q:
            return q
        else: 
            raise NotFoundError(status_code=404, error_code= 104, error_message="category not found")
    
    #shows existing information in edit request form to manager
    @auth_required('token')
    @roles_accepted('storeManager')
    def put(self, id):
        try:
            c = Catagory.query.filter_by(catagory_id = id).first()
            if not c:
                return{"error": "Category Not Found!"}
            ca = marshal(c, output_fields)
        except Exception as e:
            print(e)
            return {"ErRoR": str(e)}
        else:
            return ca    
    
api.add_resource(request_page, "/request", "/request/<int:id>")

###################################################################################################################
###################################################################################################################

class manager_req(Resource):
    # Delete Category Request
    @auth_required('token')
    @roles_accepted('storeManager')
    def get(self, id):
        try:
            user = current_user.user_id
            # m =request.get_json()['reqMessage']

            query = Catagory.query.get(id)
            if not query:
                return {"ErRoR": "Category Not Found!"}

            re = DeleteReq(user_id=user, category_id=id)
            db.session.add(re)
            db.session.commit()
        
        except Exception as e:
            print(e)
            return {'Error': str(e)}
        else:
            return {"message": "Request is sent"}
    
    # Create Category Request
    @auth_required('token')
    @roles_accepted('storeManager')
    def post(self):
        try:
            user = current_user.user_id
            name =request.get_json()['name']
            description =request.get_json()['description']
            m =request.get_json()['reqMessage']

            namecheck = Catagory.query.filter_by(name = name).first() 
            if namecheck:
                return {"ErRoR": "Name Already Exists Try Another Name"}

            re = CreateReq(user_id=user, message=m, name=name, description=description)
            db.session.add(re)
            db.session.commit()
        except Exception as e:
            print(e)
            return {'Error': str(e)}
        else:
            return {"message": "Request is sent"}
  
    # Edit Category Request
    @auth_required('token')
    @roles_accepted('storeManager')
    def put(self):
        try:
            user = current_user.user_id
            id = request.get_json()['id']
            name =request.get_json()['name']
            description =request.get_json()['d']
            m =request.get_json()['reqMessage']

            query = Catagory.query.get(id)
            if not query:
                return {"ErRoR": "Category Not Found!"}
            namecheck = Catagory.query.filter_by(name = name).filter(Catagory.catagory_id != id).first() 
            if namecheck:
                return {"ErRoR": "Name Already Exists Try Another Name"}

            re = EditReq(user_id=user, message=m, category_id=id, name=name, description=description)
            db.session.add(re)
            db.session.commit()
        
        except Exception as e:
            print(e)
            return {'Error': str(e)}
        else:
            return {"message": "Request is sent"}

api.add_resource(manager_req,"/manager_req","/manager_req/<int:id>")

###################################################################################################################
###################################################################################################################
login_request = {
    "lr_id" :fields.Integer ,
    "full_name" : fields.String,
    "email" : fields.String,
    "message" : fields.String
}
deleteReq = {
    "dr_id" :fields.Integer ,
    "user_name" : fields.String(attribute=lambda x:x.user.full_name),
    "category_id" : fields.Integer,
    "message" : fields.String,
    "status" : fields.String ,
    "catagory_name" : fields.String(attribute=lambda x:x.category.name),
    "catagory_description" : fields.String(attribute=lambda x:x.category.description)

}
createReq = {
    "request_id" :fields.Integer ,
    "user_name" : fields.String(attribute=lambda x:x.user.full_name),
    "name" : fields.String,
    "description" : fields.String,
    "message" : fields.String ,
}
editReq = {
    "request_id" :fields.Integer ,
    "category_id":fields.Integer ,
    "user_name" : fields.String(attribute=lambda x:x.user.full_name),
    "name" : fields.String,
    "description" : fields.String,
    "message" : fields.String ,
}

class admin_req(Resource):
    # role request page
    @auth_required('token')
    @roles_accepted('Admin')
    def get(self):
        req = LoginReq.query.all()
        if req:
            a = marshal(req, login_request)
            return a
        else: 
            return {"e": "No Request is Pending!"} 

    # delete category request page
    @auth_required('token')
    @roles_accepted('Admin')
    def delete(self):
        req = DeleteReq.query.all()
        if req:
            a = marshal(req, deleteReq)
            return a
        else: 
            return {"e": "No Request is Pending!"}

    # create request page
    @auth_required('token')
    @roles_accepted('Admin')
    def post(self):
        req = CreateReq.query.order_by(CreateReq.request_id.desc()).all()
        if req:
            a = marshal(req, createReq)
            return a
        else: 
            return {"e": "No Request is Pending!"}

    # edit request page.
    @auth_required('token')
    @roles_accepted('Admin')
    def put(self):
        req = EditReq.query.order_by(EditReq.request_id.desc()).all()
        if req:
            a = marshal(req, editReq)
            return a
        else: 
            return {"e": "No Request is Pending!"}
    
api.add_resource(admin_req, "/admin_req")

###################################################################################################################
###################################################################################################################
class req_action(Resource):
    # role approval
    @auth_required('token')
    @roles_accepted('Admin')
    def get(self, email):
        try:
            user = User.query.filter_by(email = email).first()
            role_i = Role.query.filter_by(id = 2).first()
            user.roles.append(role_i)
            db.session.commit()
            LoginReq.query.filter_by(email = email).delete()
            db.session.commit()

            return {"message":"Manager Role Granted To The User!"}
        except Exception as e:
            print(e)
            return {"Error": str(e)}

    # delete category
    @auth_required('token')
    @roles_accepted('Admin')
    def delete(self):
        try:    
            id = request.get_json()['dr_id']
            dr_obj = DeleteReq.query.filter_by(dr_id = id).first()
            cat = Catagory.query.filter_by(catagory_id = dr_obj.category_id).first()
            if cat is None:
                return {"message": "Category Not Found"}
            p = Product.query.filter_by(catagory_id = cat.catagory_id).first()
        
            if p :
                return {"message": "Can't delete category. As there are product in this category"}
            row = DeleteReq.query.filter_by(category_id = cat.catagory_id).all()
            for i in row:
                db.session.delete(i)
                db.session.commit()
            db.session.delete(cat)
            db.session.commit()

        except Exception as e:
            print(e)
            return {'Error': str(e)}
        else: 
            return {"message": "Category Deleted Successfully"}
    
    #create category
    @auth_required('token')
    @roles_accepted('Admin')    
    def post(self):
        try:
            rq_id = request.get_json()['id']
            name =request.get_json()['name']
            description =request.get_json()['description']
            query = db.session.query(Catagory).filter(Catagory.name == name).first()
            if query:
                return {"Error": "Category already exists on this name."}
            
            new_category = Catagory(name = name, description = description)
            db.session.add(new_category)
            db.session.commit()
            ea = CreateReq.query.filter_by(request_id = rq_id).first()
            db.session.delete(ea)
            db.session.commit()
            return {"message": "Category is created"}

        except Exception as e:
            print(e)
            return {'Error': str(e)}

    # edit category
    @auth_required('token')
    @roles_accepted('Admin')
    def put(self):
        try:
            rq_id = request.get_json()['rq_id']
            cat_id = request.get_json()['cId']
            name =request.get_json()['name']
            description =request.get_json()['d']
            query = Catagory.query.filter_by(catagory_id = cat_id).first()
            if not query:
                return {"Error": "Category Not Found!"}
            namecheck = Catagory.query.filter_by(name = name).filter(Catagory.catagory_id != cat_id).first() 
            if namecheck:
                return {"Error": "Name Already Exists Try Another Name"}
            query.name = name
            query.description = description
            db.session.commit()
            EditReq.query.filter_by(request_id = rq_id).delete()
            db.session.commit()
            return {"message": "Changes In Category Is Saved"}

        except Exception as e:
            print(e)
            return {'Error': str(e)}          

api.add_resource(req_action, "/req_action", "/req_action/<string:email>")

###################################################################################################################
###################################################################################################################

class extra(Resource):
    @auth_required('token')
    @roles_accepted('Admin')
    def get(self, id):
        req = CreateReq.query.filter_by(request_id = id).first()
        if req:
            a = marshal(req, createReq)
            return a
        else: 
            return
    @auth_required('token')
    @roles_accepted('Admin')    
    def put(self, id):
        try:
            DeleteReq.query.filter_by(dr_id = id).delete()
            db.session.commit()
            return{"message": "Request is Deleted!"}
        except Exception as e:
            print(e)
            return{"message":str(e)}

    @auth_required('token')
    @roles_accepted('storeManager')
    def post(self):
        list = Catagory.query.all()
        if list:
            a = marshal(list, output_fields)
            return a
        else: 
            return

    @auth_required('token')
    @roles_accepted('Admin')
    def delete(self,id):
        try:
            CreateReq.query.filter_by(request_id = id).delete()
            db.session.commit()
            return{"message": "Request is Deleted!"}
        except Exception as e:
            print(e)
            return{"message":str(e)}
        
api.add_resource(extra, "/extra", "/extra/<int:id>")

###################################################################################################################
###################################################################################################################
class delete_req(Resource):
    @auth_required('token')
    @roles_accepted('Admin')
    def delete(self,id):
        try:
            LoginReq.query.filter_by(lr_id = id).delete()
            db.session.commit()
            return{"message": "Request is Deleted!"}
        except Exception as e:
            print(e)
            return{"message":str(e)}

    @auth_required('token')
    @roles_accepted('Admin')
    def get(self,id):
        try:
            EditReq.query.filter_by(request_id = id).delete()
            db.session.commit()
            return{"message": "Request is Deleted!"}
        except Exception as e:
            print(e)
            return{"message":str(e)}
             
api.add_resource(delete_req, "/delete_req", "/delete_req/<int:id>")

###################################################################################################################
###################################################################################################################


class searchQuery(Resource):
    # admin search category
    @auth_required('token')
    @roles_accepted('Admin')
    def post(self):
        try:
            Query = request.get_json()['aQuery']
            query='%'+Query+'%'
            result=Catagory.query.filter(Catagory.name.like(query)).all()
            if result:
                a = marshal(result, output_fields)
                return a
            else:
                return {"no_result":"No Result Found!"}
        except Exception as e:
            print(e)
            return{"Error":str(e)}
        
    #manager search product
    @auth_required('token')
    @roles_accepted('storeManager')
    def get(self, Query, price):
        try:
            query='%'+Query+'%'
            if price == 0:
                result=Product.query.filter(Product.name.like(query)).all()
            elif price :
                result=Product.query.filter(Product.name.like(query), Product.price <= price ).all()
            if result:
                a = marshal(result, op_home)
                return a
            if not result:
                {"message":"No Result Found!"}
        except Exception as e:
            print(e)
            return{"Error":str(e)}

    @auth_required('token')
    def put(self, Query, price):
        try:
            query='%'+Query+'%'
            if price == 0:
                result=Product.query.filter(Product.name.like(query)).all()
            elif price :
                result=Product.query.filter(Product.name.like(query), Product.price <= price ).all()
            if result:
                a = marshal(result, op_home)
                return a
            if not result:
                {"message":"No Result Found!"}
        except Exception as e:
            print(e)
            return{"Error":str(e)}

api.add_resource(searchQuery,"/searchQuery/<string:Query>/<int:price>", "/searchQuery")    
###################################################################################################################
###################################################################################################################

# #Error Handler
# # @app.errorhandler(404)
# # def page_not_found(a):
# #     return render_template('404.html') , 404

# @app.errorhandler(403)
# def page_not_found(a):
#     return render_template('403.html') , 403

###################################################################################################################
#Cached functions:
@cache.cached(timeout=50, key_prefix='Get All Product For Manager')
def mAllProduct():
    d = Product.query.all()
    return d

@cache.memoize(timeout=50)
def cart_cache(id):
    c = Cart.query.filter_by(user_id = id).all()
    return c


def html_report():
    user = 4
    current_date = datetime.now()
    last_day = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    first_day = (last_day - timedelta(days=1)).replace(day=1)
    # users = User.query.all()
    user_obj = User.query.filter_by(user_id = user).first()
    orders = Order.query.filter(Order.user_id == user,Order.order_date >= first_day,Order.order_date < last_day).all()
    message = render_template('pdf-report.html', user_obj = user_obj, order = orders)
    # for user in users:
    #     user_obj = User.query.filter_by(user_id = user).first()
    #     orders = Order.query.filter(Order.user_id == user,Order.order_date >= first_day,Order.order_date < last_day).all()
    #     message = render_template('pdf-report.html', user_obj = user_obj, order = orders)
    return message


if __name__ == '__main__':
    app.run(debug=True)