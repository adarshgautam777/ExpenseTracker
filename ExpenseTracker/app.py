from flask import Flask, request, jsonify
from uuid import uuid1, uuid4
import os, json, pytz
from datetime import date, datetime
import pandas as pd

db = {}
db_filename = "db.json"

# Check whether  db.json exists in the directory or not
if os.path.exists(db_filename):
    # print("DB Exists")
    with open(db_filename, 'r') as f:
        db = json.load(f)
else:
    # print("DB NOT FOUND")
    accessKey =  str(uuid1())
    secretKey =  str(uuid4())
    item_type = [
        "Food", "Beverage", "Clothing", 
        "Stationaries", "Electronic Devices", "Wearables"
    ]
    
    db = {
        "accessKey": accessKey,
        "secretKey": secretKey,
        "item_types": item_type,
        "users": []
    }
    
    with open(db_filename, "w+") as f:
        json.dump(db, f, indent = 4)
        
app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        print(request.form)
        # print(request.method)
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        username = request.form['username'],
        
        
        userDict = {
            "name": name,
            "email": email,
            "password": password,
            "username": username,
            "purchases": {}
        }
        
        
        emailList = []
    
    for user in db["users"]:
        emailList.append(user["email"])
        
    print(emailList)
    if len(db["users"]) == 0 or userDict["email"] not in emailList:
        db["users"].append(userDict)
        
        with open(db_filename, "r") as f:
            f.seek(0)
            json.dump(db,f,indent=4)
        return "User signed up succesfully"
    
        if len(db["users"]) == 0 or userDict not in db["users"]:
            db["users"].append(userDict)
            
            with open(db_filename, "r+") as f:
                f.seek(0)
                json.dump(db, f, indent = 4)
            return "User signed up successfully"
                
        else:
            return "User already exists"
    return "Method not allowed"
    return "dsdrfj"

@app.route('/login', methods=['POST'])
def login():
    email = request.form["email"]
    password = request.form["password"]
    
    user_idx = None
        # Check for user which matches with the email and password
        
    
    for user in db["users"]:
        if user["email"] == user["email"] and user["password"] == password:
            user_idx = db["users"].index(user)
            response = {
                "message": "Login successful",
                "user_index": user_idx
                }
            return response        
        else:
            continue
    return "Wrong email or password"


@app.route('/add_puchase', methods=['POST'])
def add_puchase():
    if request.method == "POST":
         user_idx  = int(request.form["user_idx"])
         item_name = request.form["item_name"]
         item_type = request.form["item_type"]
         item_price = request.form["item_price"]
         
         curr_date = str(date.today())
         curr_time = str(datetime.now(pytz.timezone("Asia/Kolkata")))
         
         itemDict = {
             "item_name": item_name,
             "item_type": item_type,
             "item_price": item_price,
             "purchase_time": curr_time
         }
         
         existing_dates = list(db["users"][user_idx]["purchases"].keys())
         print(existing_dates)
         
         if len(db["users"][user_idx]["purchases"]) == 0 or curr_date not in existing_dates:
             db["users"][user_idx]["purchases"][curr_date] = []
             db["users"][user_idx]["purchases"][curr_date].append(itemDict)
             with open(db_filename, "r+") as f:
                f.seek(0)
                json.dump(db, f, indent = 4)
             return "Item added successfully"
                
         else :
             db["users"][user_idx]["purchases"][curr_date].append(itemDict)
             with open(db_filename, "r+") as f:
                f.seek(0)
                json.dump(db, f, indent = 4)
             return "Item added successfully"
        
    return "asds"

# -> Get all purchases for today
#     route: /get_purchases_today
#     method: GET
#     request_body:
#         data: user_idx
#     response_body:
#         list of all purchases in the following format:
#             [
#                 {
#                     "item_name": "", "item_price":"", "item_type":"", "purchase_time":""
#                 }
#             ]

@app.route('/get_purchases_today', methods=['GET'])
def get_purchases_today():
         user_idx  = int(request.args["user_index"])
    
         curr_date = str(date.today())
         
         purchases_today = db["users"][user_idx]["purchases"][curr_date]
         
         if len(purchases_today) == 0:
             return jsonify(msg="No item purchased today.")
         
         return jsonify(purchases_for_today=purchases_today)
     
     
@app.route('/get_purchases', methods=['GET'])
def get_purchases():
    data = request.json
    print(data)
    user_idx = data["user_index"]
    start_date = data["start_date"]
    end_date = data["end_date"]
    
    date_range = pd.date_range(start_date,end_date)
    #print(dates)
    db_dates = list(db["users"][user_idx]["purchases"].keys())
    print(db_dates)
    
    purchase_list = {}
    for dt in db_dates:
        if dt in date_range:
            purchase_list[dt] = db["users"][user_idx]["purchases"][dt]
            
        else:
            continue
        
    return purchase_list

       
     
if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 5000, debug = True)
    
