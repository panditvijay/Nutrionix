from flask import Response, request
from flask_restful import Resource
import uuid
import datetime
from pytz import timezone
format = "%Y-%m-%d %H:%M:%S %Z%z"
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token,decode_token
from flask_bcrypt import bcrypt

from pymongo import MongoClient 
  
try: 
    conn = MongoClient("mongodb://127.0.0.1:27017/") 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB")
    




col= conn['mydb']['users']


def getTime():
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    date =now_asia.strftime(format)
    
    return date


def getId():
    
    return str(uuid.uuid4())



class UserApi(Resource):
    @jwt_required
    def get(self):
        access_token=request.headers.get('Authorization')[7:]
        user_id = decode_token(access_token)['identity']
        
        return col.find_one({"_id":user_id})
    
    @jwt_required    
    def put(self):
        user = request.get_json(force=True)
        access_token=request.headers.get('Authorization')[7:]
        id = decode_token(access_token)['identity']
        
        if user.get('firstName') is not None:
            col.update_one({"_id":id},{"$set":{'firstName':user.get('firstName')}})
            
        if user.get('lastName') is not None:
            col.update_one({"_id":id},{"$set":{'lastName':user.get('lastName')}})
            
        if user.get('email') is not None:
            col.update_one({"_id":id},{"$set":{'email':user.get('email')}})
        
        if user.get('phone') is not None:
            col.update_one({"_id":id},{"$set":{'phone':user.get('phone')}})
            
        return 'Your details updated successfully'
    
class UserSignup(Resource):
    def post(self):
        user = request.get_json(force=True)
        bvalue = bytes(user.get('password'), 'utf-8')
        temp_hash = bcrypt.hashpw(bvalue, bcrypt.gensalt())
        
        user["_id"]=getId()
        user["date"]=getTime()
        user["password"]=temp_hash.decode('utf-8')
        user["meal_id"]=[]
        col.insert(user)
        return 'cool'
    
    
class UserLogin(Resource):
    def post(self):
        body = request.get_json(force=True)
        
        user = col.find_one({"username":body.get('username')})
        
        if user is None:
            return 'Invalid username'
        
        authorized = bcrypt.checkpw(body.get('password').encode('utf-8'),user.get('password').encode('utf-8'))
        
        if not authorized:
            return {'error': 'Email or password invalid'}, 401
        
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=str(user.get('_id')), expires_delta=expires)
        return {'token': access_token}, 200
        
 

class AdminApi(Resource):
    def get(self):
        
        meals = col.find({})
        
        
        return 'cool'

class AdminSignup(Resource):
    def post(self):
        admin = request.get_json(force=True)
        bvalue = bytes(admin.get('password'), 'utf-8')
        temp_hash = bcrypt.hashpw(bvalue, bcrypt.gensalt())
        
        admin["_id"]=getId()
        admin["date"]=getTime()
        admin["password"]=temp_hash.decode('utf-8')
        admin["role"]="admin"
        col.insert(admin)
        return 'cool'
    
    

   
class ManagerApi(Resource):
    def post(self):
        return 'cool'
    
class ManagerSignup(Resource):
    def post(self):
        manager = request.get_json(force=True)
        bvalue = bytes(manager.get('password'), 'utf-8')
        temp_hash = bcrypt.hashpw(bvalue, bcrypt.gensalt())
        
        manager["_id"]=getId()
        manager["date"]=getTime()
        manager["password"]=temp_hash.decode('utf-8')
        manager["role"]="manager"
        col.insert(manager)
        return 'cool'


        
    
class ForgotPassword(Resource):
    def post(self):
        body = request.get_json(force=True)
        
        user=col.find_one({"email":body.get('email')})
        
        if user is None:
            return 'Invvalid username'
        
        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=str(user.get('_id')), expires_delta=expires)
        
        return {'token': access_token}, 200
    
    
class ResetPassword(Resource):
    def post(self):
        body = request.get_json(force=True)
        #print(body.get('reset_token'))
        _id = decode_token(body.get('access_token'))['identity']
        
        print(col.find_one({"_id":_id}).get('username'))
        bvalue = bytes(body.get('password'), 'utf-8')
        temp_hash = bcrypt.hashpw(bvalue, bcrypt.gensalt())
        
        col.update_one({"_id":_id},{"$set":{'password':temp_hash.decode('utf-8')}})
        
        
        return 'Your password has been reset successfully!'
       