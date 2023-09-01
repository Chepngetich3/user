@app.route("/register",methods=['POST','GET'])
def Register():
   return render_template("register.html")
 #mpesa intergration route
import requests
import base64
import datetime
from requests.auth import HTTPBasicAuth
@app.route("/mpesa_payment",methods=['POST','GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "cAR4LrWpeDV7mN3AsCSpXPxlvaLZCCZo"
        consumer_secret = "enG5ojDkAL2cRQ4U"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
               '<a href="/getproducts" class="btn btn-dark btn-sm">Back to Products</a>'
    else:
       return render_template("single_html.html")
    

@app.route("/edit/<username>",methods=['POST','GET'])
def Edit(username):
 if request.method == 'POST':
   #TODO
   name=request.form['username']
   email=request.form['email']
   password=request.form['password']
   phone=request.form['phone']
   #sql query to update
   sql_update='update users set username=%s,email=%s,password=%s,phone=%s where username=%s'
   cursor_update=connection.cursor()
   cursor_update.execute(sql_update,(name,email,password,phone,username))
   connection.commit()
   return "records Updated /n "
   
 else:
   sql='select* from users where username=%s'
   cursor=connection.cursor()
   cursor.execute(sql,username)
   user=cursor.fetchone()
   return render_template('edit.html',user=user)
 
   
from flask import*
app=Flask(__name__)
#create a route()
@app.route('/loans',methods=['POST','GET'])
def Loan():
    if request.method=='POST':
        #TODO
        import pandas as pd
        data=pd.read_csv("bank.csv")
        #divide the data into predictors and outcome
        array=data.values
        X=array[:,0:8]#predictors
        Y=array[:,8]#outcome
        from sklearn import model_selection
        X_train,X_test,Y_train,Y_test=model_selection.train_test_split(X,Y,test_size=0.20,random_state=42)
        #import the algorithms
        from sklearn.ensemble import GradientBoostingClassifier
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.naive_bayes import GaussianNB
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.svm import SVC
        from sklearn.linear_model import LogisticRegression
        # define the model to use
        model=GaussianNB()
        model.fit(X_train,Y_train)
        #GET THE USER INPUT FROM THE FORM
        Gender=request.form['gender']
        Married=request.form['married']
        Education=request.form['education']
        Self_employed=request.form['self_employed']
        Income=request.form['income']
        Loan_Amount=request.form['amount']
        
        user_input=[[varchar(Gender),text(Married),text(Education),text(Self_employed),int(Income),int(Loan_Amount)]]
        model_prediction=model.predict(user_input)
        print(model_prediction)
        return render_template("loan.html",outcome=model_prediction)
        pass
    else:
        return render_template("loan.html")

app.run(debug=True)

   