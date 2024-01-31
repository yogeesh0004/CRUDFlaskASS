# from flask import Flask,redirect,render_template,request,url_for,flash
# import json
# from flask_sqlalchemy import SQLAlchemy
# import pypyodbc as odbc
from flask_mail import Mail, Message
from flask import Flask,redirect,render_template,request,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import pyodbc

app=Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dummy.python10@gmail.com'
app.config['MAIL_PASSWORD'] = 'tbkqmfolwjmjwnfk'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

app.secret_key="^%$^$^^*&&FGGY9178"
 
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://ubnu5joorskluqkm:CvubLkhKYsjNI674n656@bfkg0pvnjiimudyocios-mysql.services.clever-cloud.com:3306/bfkg0pvnjiimudyocios'
db = SQLAlchemy(app)
# DRIVER_NAME='SQL SERVER'
# SERVER_NAME='APINP-ELPTTQSW3\SQLEXPRESS'
# DATABASE_NAME='crudApp'
 
 
# connnection_string=connection_string = (
#     'DRIVER={SQL Server};'
#     'SERVER=APINP-ELPTTQSW3\SQLEXPRESS;'
#     'DATABASE=crudApp;'
#     'UID=tap2023;'
#     'PWD=tap2023;'
# )
# conn=odbc.connect(connnection_string)
# print(conn)
 
 
 
# local_server= True
# app=Flask(__name__)
# app.secret_key="^%$^$^^*&&FGGY9178"
 
 
# database configuration
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databasename'
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/flaskcrudapp'
# db=SQLAlchemy(app)
 
 
# app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 2525
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'yogeeshpavas@gmail.com'  # Replace with your Gmail address
# app.config['MAIL_PASSWORD'] = 'Yogeesh1999$'  # Replace with your Gmail password
# mail = Mail(app)
 
 
# configuration of database tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(15))
 
class Products(db.Model):
    pid=db.Column(db.Integer,primary_key=True)
    productName=db.Column(db.String(50))
    productDescription=db.Column(db.String(100))
    rating=db.Column(db.Integer)
    stocks=db.Column(db.Integer)
    price=db.Column(db.Integer)
 
@app.route("/test/")
def test():
    try:
        # query=Test.query.all()
        # print(query)
        sql_query="Select * from test"
        with db.engine.begin() as conn:
            response=conn.exec_driver_sql(sql_query).all()
            print(response)
        return f"Database is connected"
 
    except Exception as e:
        return f"Database is not connected {e} "
 
 
@app.route("/")
def home():
    products=Products.query.all()
    return render_template("index.html",products=products)
 
# create operation
@app.route("/create",methods=['GET','POST'])
def create():
    if request.method=="POST":
        pName=request.form.get('productname')
        pDesc=request.form.get('productDesc')
        pRating=request.form.get('rating')
        pStocks=request.form.get('stocks')
        pPrice=request.form.get('price')
        # query=Products(productName=pName,productDescription=pDesc,rating=pRating,stocks=pStocks,price=pPrice)
        # db.session.add(query)
        # db.session.commit()
        sql_query=f"INSERT INTO `products` (`productName`, `productDescription`, `rating`, `stocks`, `price`) VALUES ('{pName}', '{pDesc}', '{pRating}', '{pStocks}', '{pPrice}')"
        with db.engine.begin() as conn:
            conn.exec_driver_sql(sql_query)
            flash("Product is Added Successfully","success")
            return redirect(url_for('home'))
       
 
 
    return render_template("index.html")
 
# update operation
@app.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    product=Products.query.filter_by(pid=id).first()
    if request.method=="POST":
        pName=request.form.get('productname')
        pDesc=request.form.get('productDesc')
        pRating=request.form.get('rating')
        pStocks=request.form.get('stocks')
        pPrice=request.form.get('price')
        # query=Products(productName=pName,productDescription=pDesc,rating=pRating,stocks=pStocks,price=pPrice)
        # db.session.add(query)
        # db.session.commit()
        sql_query=f"UPDATE `products` SET `productName`='{pName}',`productDescription`='{pDesc}',`rating`='{pRating}',`stocks`='{pStocks}',`price`='{pPrice}' WHERE `pid`='{id}'"
       
        with db.engine.begin() as conn:
            conn.exec_driver_sql(sql_query)
            flash("Product is Updated Successfully","primary")
            return redirect(url_for('home'))
 
 
    return render_template("edit.html",product=product)
 
 
 
# delete operation
@app.route("/delete/<int:id>",methods=['GET'])
def delete(id):
    # print(id)
    query=f"DELETE FROM `products` WHERE `pid`={id}"
    with db.engine.begin() as conn:
        conn.exec_driver_sql(query)
        flash("Product Deleted Successfully","danger")
        return redirect(url_for('home'))
   
@app.route("/search", methods=['POST'])
def search():
    search = request.form.get('search')
    # check if the input string can be converted to an integer
    if search.isdigit():
        products = Products.query.filter_by(pid=int(search)).all()
    else:
        products = Products.query.filter(Products.productName.like("%"+search+"%")).all()
 
    return render_template("index.html", products=products)
 
@app.route("/contact")
def contact():
    return render_template("contact.html")
   
   
@app.route('/contact', methods=['GET','POST'])
def contactmail():
    if 'name' in request.form and 'email' in request.form and 'message' in request.form:
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
 
        # Send email
        sender_email = f'{email}'
        msg = Message(f'{message}', sender=sender_email, recipients=['yogeeshpavas@gmail.com'])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
       
        mail.send(msg)
       
        flash("Mail sent Successfully","success")
       
        return redirect(url_for("home"))
   
   
@app.route('/mail')
def mail():
    print("dsdv")
    msg = Message('Hello', sender = 'dummy.python10@gmail.com', recipients = ['dummy.python10@gmail.com'])
    msg.body = "This is the email body"
    
    
    mail.send(msg)
    return "Sent"   
 
   
 
 
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)