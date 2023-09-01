from flask import*
import pymysql
#create app
app=Flask(__name__)
app.secret_key="ehwewrf"
#define connection
connection=pymysql.connect(host="localhost",user="root",password="",database="loans_project")
#home page
@app.route('/')
def main():
   return render_template('index.html')
#create save
@app.route("/save_vendor",methods=['POST','GET'])
def Save_vendor():
    #check is user has posted any data
    if request.method=='POST':
       
       #TODO
       #get data from the form
       name=request.form['name']
       email=request.form['email']
       password=request.form['password']
       phone=request.form['phone']
       location=request.form['location']
       desc=request.form['desc']
       
       #get image
       #check if image has been uploaded
       
       if not name or not email or not password or not phone or not location or not desc:
            return render_template("signup.html",message="please fill in all the areas")
       #create cursor
       cursor=connection.cursor()
       sql='insert into lendors(lendor_name,lendor_email,lendor_password,lendor_contact,lendor_location,lendor_desc)values(%s,%s,%s,%s,%s,%s)'
        
            
    #execute
       cursor.execute(sql,(name,email,password,phone,location,desc))
       connection.commit()
       cursor.close()
       return render_template("signup.html",message="lendor saved successfully")
        # except:
        #     return render_template("signup.html",message="failed vendor not saved")
        
    else:
       return render_template("signup.html")
#signature
@app.route("/signin",methods=['POST','GET'])
def Signin():
   #check if tthe user has posted 
   if 'key'in session:
     return render_template("lendor.html")
   
   if request.method=='POST':
      #GET DATA FROM THE FORM
      username=request.form['username']
      password=request.form['password']
      #create a cursor function
      cursor=connection.cursor()
      #sql
      sql='select* from lendors where lendor_name=%s and lendor_password=%s'
      #execute the sql query
      values=(username,password)
      cursor.execute(sql,(username,password))
      #check if vendor exists
      if cursor.rowcount==0:
       return render_template("signup.html",message="Wrong credentials \n User Does Not exist")
      else:
         session['key']= username
         #fetch th records of the vendor
         data=cursor.fetchone()
         #other sessions
         session['id']=data[0]
         session['email']=data[2]
         session['desc']=data[5]
         session['location']=data[6]
         session['image']=data[7]
         print(data)
         return render_template("lendor.html",lendor=data)
   else:
      return render_template("signup.html")
#log out route
@app.route("/logout")
def Logout():
   session.clear()
   return redirect("/signin")
#logout route vendor
@app.route("/logout/user")
def Logout_user():
   session.clear()
   return redirect("/login")



#add product route
@app.route("/add_loan",methods=['POST','GET'])
def Add_loan() :
   if 'key'not in session:
      return redirect("signin")
   if request. method=="POST":
   #TODO
   #get data from the form
      
      lendor_id=request.form['lendor_id']
      category=request.form['loan_category']
      amount=request.form['loan_amount']
      interest=request.form['loan_interest']
      desc=request.form['loan_desc']
      #input validation
      if  not lendor_id or not category or not amount or not interest or not desc:
       return "please provide all the loan details"
      #get the image 
      image=request.files['product_image']
      image.save('static/images/'+image.filename)
      image_url=image.filename
      #create cursor function
      cursor=connection.cursor()
      sql='insert into loans(lendor_id,loan_desc,loan_category,loan interest,loan_amount,image_url)values(%s,%s,%s,%s,%s,%s)'
      #execute sql query
      cursor.execute(sql,(lendor_id,desc,amount,interest,category,image_url))
      connection.commit()
      return 'loan saved\n <a href="/signin">Go Back</a>'
   else:
    return render_template("add_loan.html")     
#get products
@app.route('/getloans',methods=['GET'])
def GetLoans():
   #create the cursor
   cursor_electronics=connection.cursor()
   sql_electronics='select* from products where product_category="Electronics"'
  #grade1
   cursor_grade1=connection.cursor()
   sql_grade1='select* from products where product_category="Grade1"'
   #scent
   cursor_scent=connection.cursor()
   sql_scent='select* from products where product_category="Scent"'
   #execute the sql query
   cursor_electronics.execute(sql_electronics)
   # execute grade1
   cursor_grade1.execute(sql_grade1)
    #execute the sql query
   cursor_scent.execute(sql_scent)
   #fetch all th products
   electronics=cursor_electronics.fetchall()
   #fetch all th products
   grade1=cursor_grade1.fetchall()
   scent=cursor_scent.fetchall()
   #check if there are products to display
   if cursor_electronics.rowcount==0:
      return render_template('getproducts.html',message='No Products to display')
   else:
      
      # products=jsonify(products)#converts products into json format
      # return products
      return render_template('getproducts.html',data=electronics,Grade1=grade1,Scent=scent)
#fetch products by vendor_id
@app.route("/vendor_products/<vendor_id>",methods=['GET'])
def Vendor_products(vendor_id):
   if 'key' not in session:
      return redirect("/signin")
   else:
    sql='select* from products where vendor_id=%s'
   cursor=connection.cursor()
   #execute the sql query
   cursor.execute(sql,vendor_id)
   #fetch the products
   vendor_products=cursor.fetchall()
   #check if there are products to display
   if cursor.rowcount==0:
      return render_template("vendor_products.html",error="No products Available")
   else:
      return render_template("vendor_products.html",data=vendor_products)
   #delete product
@app.route("/delete/<loan_id>",methods=['POST','GET','DELETE'])
def delete_product(product_id):
   if 'key'not in session:
      return redirect("/signin")
   else:
      sql="delete from products where product_id=%s"
      #cuesor
      cursor=connection.cursor()
      #execue
      cursor.execute(sql,product_id)
      connection.commit()
      return "Loan deleted "
   pass
#view products basd on categories

#create another route for user to signin
@app.route("/login",methods=['POST','GET'])
def Login():
   if request.method=='POST':

       #TODO
       #get the posted data
       data=request.form['name']
       password=request.form['password']
       #create cursor
       cursor=connection.cursor()
       #sql
       sql='select * from users where (username=%s or email=%s or phone=%s) and password=%s'
       #execute the sql query
       values=(data,data,data,password)
       cursor.execute(sql,values)
       #check if user exist
       if cursor.rowcount==0:
          return render_template("signin.html",message='wrong log in credentials')
       else:
          #fetch
          user=cursor.fetchone()
          username=user[0]
          session['user']=username
          return redirect("/getloans")
         #  return render_template("signin.html",message='signin successfully')

      
   else:
      return render_template("signin.html")





#run app
if __name__=="__main__":
 app.run(debug=True,port=8000)