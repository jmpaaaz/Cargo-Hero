import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")


order_management_db = myclient["order_management"]

#get password
def get_user(username):
    customers_coll = order_management_db['customers']
    user=customers_coll.find_one({"username":username})
    return user
def get_password(username):
    return get_user(username)["password"]
def update_password(username,newpassword):
    customers_coll = order_management_db["customers"]
    updatepassword = customers_coll.update_one({"username":username}, {"$set":{"password":newpassword}})
    return updatepassword
