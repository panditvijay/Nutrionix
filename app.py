from flask import Flask, jsonify, request
import uuid
from flask_restful import Api




from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager



app = Flask(__name__)

app.config.from_envvar('ENV_FILE_LOCATION')



@app.route('/')
def hello():
    return {'hello': 'world'}


bcrypt = Bcrypt(app)
api = Api(app)
jwt = JWTManager(app)

from resources.meals import MealsApi, MealApi
from resources.users import UserApi,UserSignup, UserLogin,AdminApi,AdminSignup,ManagerApi,ManagerSignup,ForgotPassword,ResetPassword




api.add_resource(MealsApi, '/api/meals')
api.add_resource(MealApi, '/api/meals/<id>')

api.add_resource(UserApi, '/api/users')
api.add_resource(UserSignup, '/api/users/signup')
api.add_resource(UserLogin, '/api/users/login')

api.add_resource(AdminApi, '/api/admin')
api.add_resource(AdminSignup, '/api/admin/signup')
#api.add_resource(AdminLogin, '/api/admin/login')

api.add_resource(ManagerApi, '/api/manager')
api.add_resource(ManagerSignup, '/api/manager/signup')
#api.add_resource(ManagerLogin, '/api/manager/login')

api.add_resource(ForgotPassword, '/api/auth/forgot')
api.add_resource(ResetPassword, '/api/auth/reset')
    



#app.run(debug='true')