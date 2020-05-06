from flask import Response, request
from flask_restful import Resource
import uuid
import datetime
from pytz import timezone
format = "%Y-%m-%d %H:%M:%S %Z%z"
from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token,decode_token

from utils import Utils

from pymongo import MongoClient 
  
try: 
    conn = MongoClient("mongodb://127.0.0.1:27017/") 
    print("Connected successfully!!!") 
except:   
    print("Could not connect to MongoDB")
    




col= conn['mydb']['mycol']

col_user=conn['mydb']['users']


def getTime():
    now_utc = datetime.datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    date =now_asia.strftime(format)
    
    return date


def getId():
    
    return str(uuid.uuid4())

class MealsApi(Resource):
    #List all meals for a user
    @jwt_required
    def get(self):
        access_token=request.headers.get('Authorization')[7:]
        user_id = decode_token(access_token)['identity']
        
        find_user=col_user.find_one({"_id":user_id})
        
        meal_ids = find_user.get('meal_id')
        meals=[]
        
        for i in meal_ids:
            meals.append(col.find_one({"_id":i}))
            
        return meals;
            
        
    #Add meals    
    @jwt_required
    def post(self):
        meal = request.get_json(force=True)
        access_token=request.headers.get('Authorization')[7:]
        _id = getId()
        
        user_id = decode_token(access_token)['identity']
        print(user_id)
        find_user=col_user.find_one({"_id":user_id})
        print(find_user)
        
        
        val=find_user.get('meal_id')
        
        val.append(_id)
        print(val)
        
        col_user.update_one({"_id":user_id},{"$set":{"meal_id":val}})
        
        #Nutrionix API Integration
        try:
            if not meal.get("calorie", None):
                meal["calorie"] = int(Utils.nutritionix_calorie_count(
                    meal.get('food_name')))
        except Exception as ex:
            print('Could not reach Nutritionix to get data' + str(ex))
            meal["calorie"] = 0
        
        
        
        meal["_id"]=_id
        meal["date"]=getTime()
        
        col.insert_one(meal)
        return 'cool', 200
    

class MealApi(Resource):
    #Get meal by id
    @jwt_required
    def get(self,id):
        return col.find_one({"_id":id})
    
    #Update meal
    @jwt_required
    def put(self,id):
        meal = request.get_json(force=True)
        #foundU=col.find_one({"_id":id})
        
        if meal.get('calorie') is not None:
            col.update_one({"_id":id},{"$set":{'calorie':meal.get('calorie')}})
        
        if meal.get('description') is not None:
            col.update_one({"_id":id},{"$set":{'description':meal.get('description')}})
        
        if meal.get('food_name') is not None:
            col.update_one({"_id":id},{"$set":{'food_name':meal.get('food_name')}})
            
        if meal.get('is_in_days_limit') is not None:
            col.update_one({"_id":id},{"$set":{'is_in_days_limit':meal.get('is_in_days_limit')}})
            
        return 'Updated successfully',200
    
    #Delete meal
    @jwt_required
    def delete(self,id):
        
        access_token=request.headers.get('Authorization')[7:]
        user_id = decode_token(access_token)['identity']
        
        find_user=col_user.find_one({"_id":user_id})
        
        meal_ids = find_user.get('meal_id')
        new_ids=[]
        for ids in meal_ids:
            if id!=ids:
                new_ids.append(ids)
                
        col_user.update_one({"_id":user_id},{"$set":{'meal_id':new_ids}})
                
        col.remove({"_id":id})
        
        return 'Yeaaa, Deleted!!'
            
            
        
        
        
        
        