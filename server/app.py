
# from flask import Flask, make_response, abort, request,jsonify
# from flask_restful import Api, Resource, reqparse
# from models import db, User, Service, ProviderService
# from flask_bcrypt import Bcrypt
# import re
# from flask_cors import CORS
# from flask_migrate import Migrate
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from datetime import timedelta
# import os
# from sqlalchemy import func

# app = Flask(__name__)
# api = Api(app)
# bcrypt = Bcrypt(app)
# CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:shady42635509@localhost:5432/kazi_konnect'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['JWT_SECRET_KEY'] = os.environ.get('secret_key')
# app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
# db.init_app(app)

# password_pattern = re.compile(r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[$%@!*.!?])[A-Za-z\d$%@!*.!?]{8,}')
# email_pattern = re.compile(r'[\w-]+(\.[w-]+)*@([\w-]+\.)+[a-zA-Z]{2,}')

# migrate = Migrate(app, db)
# jwt = JWTManager(app)
# jwt.init_app(app)

# signup_parser = reqparse.RequestParser()
# signup_parser.add_argument('first_name', type=str, required=True, help='First name is required')
# signup_parser.add_argument('last_name', type=str, required=True, help='Last name is required')
# signup_parser.add_argument('email', type=str, required=True, help='Email is required')
# signup_parser.add_argument('password', type=str, required=True, help='Password is required')
# signup_parser.add_argument('selectedRole', type=int, required=True, help='Role is required')
# signup_parser.add_argument('service_name', type=str, required=False, help='service name is required')

# signup_parser.add_argument('middle_name', type=str, required=False)
# signup_parser.add_argument('national_id', type=str, required=False)
# signup_parser.add_argument('phone_number', type=str, required=False)
# signup_parser.add_argument('image', type=str, required=False)

# class Signup(Resource):
#     def post(self):
#         args = signup_parser.parse_args()
#         email = args['email']
#         password = args['password']
#         first_name = args['first_name']
#         last_name = args['last_name']
#         role_id = args['selectedRole']
#         service_name = args.get('service_name')
#         middle_name = args.get('middle_name')
#         national_id = args.get('national_id')
#         image = args.get('image')
#         phone_number = args.get('phone_number')


#         if not all([email, password, first_name, last_name, role_id]):
#             return {'error': 'Fill in all forms'}, 400

#         if not password_pattern.match(password):
#             return {'error': 'Password must meet the required criteria'}, 400
#         if len(phone_number) != 10:
#             return {'error': 'Enter a valid Phone Number'}
#         if len(national_id) != 8:
#             return {'error': 'Enter a valid National Identity Number'}
#         if not email_pattern.match(email):
#             return {'error': 'Invalid email format'}, 400

#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             return {'error': 'Email already exists'}, 400

#         new_user = User(
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password=hashed_password,
#             role_id=role_id,
#             middle_name=middle_name,
#             national_id=national_id,
#             image=image,
#             phone_number=phone_number
#         )
#         db.session.add(new_user)

#         # Add provider service if role_id is 2 and service_name is provided
#         if role_id == 2 and service_name:
#             service = Service.query.filter(func.lower(Service.service_name) == func.lower(service_name)).first()
#             if service:
#                 provider_service = ProviderService(
#                     provider_id=new_user.id,
#                     service_id=service.id
#                 )
#                 db.session.add(provider_service)

#         try:
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#             return {'error': str(e)}, 500

#         access_token = create_access_token(identity=email)
#         response = make_response({'message': 'Sign up successful', 'token': access_token, 'id': new_user.id,'role_id':new_user.role_id,'first_name':new_user.first_name,'last_name':new_user.last_name,'email':new_user.email,'password':new_user.password}, 201)
#         return response


# login_parse = reqparse.RequestParser()
# login_parse.add_argument('email', type=str, required=True, help='email is required'),
# login_parse.add_argument('password', type=str, required=True, help='Password is required')


# class Login(Resource):
#     def post(self):
#         args = login_parse.parse_args()
#         email = args['email']
#         password = args['password']
#         if email == '' or password == '':
#             response = make_response({'error': 'Fill in all forms'}, 401)
#             return response
#         existing_user = User.query.filter_by(email=email).first()
#         if not existing_user:
#             response = make_response({'error': 'Invalid email or password'}, 401)
#             return response
#         hashed_password = existing_user.password
#         if existing_user and bcrypt.check_password_hash(hashed_password, password):
#             access_token = create_access_token(identity=email)
#             role_id = existing_user.role_id
#             id = existing_user.id
#             response = make_response(
#                 {'message': 'Login successful', 'access_token': access_token, 'role_id': role_id, 'id': id}, 200)
#             return response
#         response = make_response({'error': 'Invalid email or password'}, 401)
#         return response


# class Dashboard(Resource):
#     @jwt_required()
#     def get(self):
#         current_user = get_jwt_identity()
#         user = User.query.filter_by(email=current_user).first()
#         if user:
#             response = make_response(
#                 {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
#                  'role_id': user.role_id, 'phone_number': user.phone_number})
#             return response
#         else:
#             response = make_response({'error': 'Error fetching user details'}, 404)
#             return response      


# @app.route('/service', methods=['GET', 'POST'])
# @jwt_required()
# def handle_service_request():
#     if request.method == 'GET':
#         try:
#             current_user = get_jwt_identity()
#             user = User.query.filter_by(email=current_user).first()
#             if not user:
#                 return {'error': 'User not found'}, 404

#             all_services = Service.query.all()
#             all_services_data = [{'id': service.id, 'name': service.service_name} for service in all_services]

#             return {'all_services': all_services_data}, 200

#         except Exception as e:
#             return {'error': 'An error occurred while processing the request'}, 500

#     elif request.method == 'POST':
#         try:
#             current_user = get_jwt_identity()
#             user = User.query.filter_by(email=current_user).first()

#             if not user:
#                 return {'error': 'User not found'}, 404

#             args = request.json
#             existing_services = args.get('existing_services', [])
#             new_service_name = args.get('service_name')

#             # Check if at least one service is provided
#             if not existing_services and not new_service_name:
#                 return {'error': 'At least one service must be provided'}, 400

#             # Initialize a list to hold service IDs
#             service_ids = []

#             # Handle existing services selected from the dropdown
#             for service_id in existing_services:
#                 service = Service.query.get(service_id)
#                 if service:
#                     provider_service = ProviderService(
#                         provider_id=user.id,
#                         service_id=service_id
#                     )
#                     db.session.add(provider_service)
#                     service_ids.append(service_id)

#             # Handle new service entered manually
#             if new_service_name:
#                 existing_service = Service.query.filter(func.lower(Service.service_name) == func.lower(new_service_name)).first()
#                 if existing_service:
#                     return {'error': f'Service "{new_service_name}" already exists, kindly check the list provided'}, 401

#                 new_service = Service(
#                     service_name=new_service_name,
#                     provider_id=user.id
#                 )
#                 db.session.add(new_service)
#                 db.session.flush()
#                 provider_service = ProviderService(
#                     provider_id=user.id,
#                     service_id=new_service.id
#                 )
#                 db.session.add(provider_service)
#                 service_ids.append(new_service.id)

#             # Commit all changes to the database
#             db.session.commit()

#             return {'message': f'Services created and associated with {user.first_name} {user.last_name}', 'service_ids': service_ids}, 201

#         except Exception as e:
#             return {'error': 'An error occurred while processing the request'}, 500



# provider_parser = reqparse.RequestParser()
# provider_parser.add_argument('service_id', type=int, required=True, help='Service Id required')

# class ServiceProvider(Resource):
#     @jwt_required()
#     def get(self):
#         args = provider_parser.parse_args() 
#         service_id = args['service_id']
#         provider_ids = ProviderService.query.filter_by(service_id=service_id).all()
        
#         if provider_ids:
#             provider_ids = [provider.provider_id for provider in provider_ids]
#             response = make_response({'provider_ids': provider_ids})
#             return response
#         else:
#             response = make_response({'error': 'No Service providers found for this service'}, 404)
#             return response

# class ProviderList(Resource):
#     @jwt_required()
#     def get(self):
#         provider_ids = request.args.get('provider_ids')

#         if provider_ids is None:
#             return {'error': 'No provider IDs provided'}, 400

#         provider_ids_list = provider_ids.split(',')
#         provider_ids_list = [int(provider_id) for provider_id in provider_ids_list]

#         users = User.query.filter(User.id.in_(provider_ids_list)).all()

#         if users:
#             # Format the user data as a list of dictionaries
#             user_details = [{'first_name': user.first_name, 'last_name': user.last_name} for user in users]
#             return jsonify(user_details)
#         else:
#             return {'error': 'No users found for the given provider IDs'}, 404


# class ProviderIds(Resource):
#     def get(self, service_id):
#         provider_ids = ProviderService.query.filter_by(service_id=service_id).all()
#         if provider_ids:
#             ids = [provider.provider_id for provider in provider_ids]
#             response = make_response({'provider_ids': ids})
#             return response
#         else:
#             response = make_response({'error': 'Provider ids do not exist'}, 404)
#             return response

# api.add_resource(ProviderList, '/provider-details')
# api.add_resource(ProviderIds,'/provider-ids/<int:service_id>')

# api.add_resource(ServiceProvider,'/service-provider')
# api.add_resource(Signup, '/signup')
# api.add_resource(Login, '/login')
# api.add_resource(Dashboard, '/dashboard')



# if __name__ == '__main__':
#     app.run(debug=True, port=4000)






from flask import Flask, make_response, abort, request,jsonify
from flask_restful import Api, Resource, reqparse
from models import db, User, Service, ProviderService
from flask_bcrypt import Bcrypt
import re
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os
from sqlalchemy import func

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:shady42635509@localhost:5432/kazikonnect'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('secret_key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
db.init_app(app)

password_pattern = re.compile(r'(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[$%@!*.!?])[A-Za-z\d$%@!*.!?]{8,}')
email_pattern = re.compile(r'[\w-]+(\.[w-]+)*@([\w-]+\.)+[a-zA-Z]{2,}')

migrate = Migrate(app, db)
jwt = JWTManager(app)
jwt.init_app(app)

signup_parser = reqparse.RequestParser()
signup_parser.add_argument('first_name', type=str, required=True, help='First name is required')
signup_parser.add_argument('last_name', type=str, required=True, help='Last name is required')
signup_parser.add_argument('email', type=str, required=True, help='Email is required')
signup_parser.add_argument('password', type=str, required=True, help='Password is required')
signup_parser.add_argument('selectedRole', type=int, required=True, help='Role is required')
signup_parser.add_argument('service_name', type=str, required=False, help='service name is required')

signup_parser.add_argument('middle_name', type=str, required=False)
signup_parser.add_argument('national_id', type=str, required=False)
signup_parser.add_argument('phone_number', type=str, required=False)
signup_parser.add_argument('uuid', type=str, required=False, help='uuid is required')
signup_parser.add_argument('uids', type=str, required=False, help='uuid is required')
signup_parser.add_argument('image', type=str, required=False)

class Signup(Resource):
    def post(self):
        args = signup_parser.parse_args()
        email = args['email']
        password = args['password']
        first_name = args['first_name']
        last_name = args['last_name']
        role_id = args['selectedRole']
        service_name = args.get('service_name')
        middle_name = args['middle_name']
        national_id = args['national_id']
        image = args['image']
        phone_number = args['phone_number']
        uuid = args['uuid']
        uids = args['uids']


        if not all([email, password, first_name, last_name, role_id]):
            return {'error': 'Fill in all forms'}, 400

        if not password_pattern.match(password):
            return {'error': 'Password must meet the required criteria'}, 400
        if phone_number and len(phone_number) != 10:
            return {'error': 'Enter a valid Phone Number'}
        if national_id and len(national_id) != 8:
            return {'error': 'Enter a valid National Identity Number'}
        if not email_pattern.match(email):
            return {'error': 'Invalid email format'}, 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'error': 'Email already exists'}, 400
        db.session.commit()
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            role_id=role_id,
            image=image,
            uuid = uuid
        )
        db.session.add(new_user)
        db.session.commit()
        e_user = User.query.filter(User.uuid == uids).first()
        print("UUID from frontend:", uids)
        print("User found in database:", e_user)
        if e_user:
            print("Updating user information...")
            e_user.middle_name = middle_name
            e_user.national_id = national_id
            e_user.phone_number = phone_number
            db.session.commit()
        else:
            print("User not found with UUID:", uids)

        # Add provider service if role_id is 2 and service_name is provided
        if role_id == 2 and service_name:
            service = Service.query.filter(func.lower(Service.service_name) == func.lower(service_name)).first()
            if service:
                provider_service = ProviderService(
                    provider_id=new_user.id,
                    service_id=service.id
                )
                db.session.add(provider_service)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500
        

        access_token = create_access_token(identity=email)
        response = make_response({'message': 'Sign up successful', 'token': access_token, 'id': new_user.id,'role_id':new_user.role_id,'first_name':new_user.first_name,'last_name':new_user.last_name,'email':new_user.email,'password':new_user.password}, 201)
        return response


login_parse = reqparse.RequestParser()
login_parse.add_argument('email', type=str, required=True, help='email is required'),
login_parse.add_argument('password', type=str, required=True, help='Password is required')


class Login(Resource):
    def post(self):
        args = login_parse.parse_args()
        email = args['email']
        password = args['password']
        if email == '' or password == '':
            response = make_response({'error': 'Fill in all forms'}, 401)
            return response
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            response = make_response({'error': 'Invalid email or password'}, 401)
            return response
        hashed_password = existing_user.password
        if existing_user and bcrypt.check_password_hash(hashed_password, password):
            access_token = create_access_token(identity=email)
            role_id = existing_user.role_id
            id = existing_user.id
            response = make_response(
                {'message': 'Login successful', 'access_token': access_token, 'role_id': role_id, 'id': id}, 200)
            return response
        response = make_response({'error': 'Invalid email or password'}, 401)
        return response


class Dashboard(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()
        if user:
            response = make_response(
                {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                 'role_id': user.role_id, 'phone_number': user.phone_number})
            return response
        else:
            response = make_response({'error': 'Error fetching user details'}, 404)
            return response      


@app.route('/service', methods=['GET', 'POST'])
@jwt_required()
def handle_service_request():
    if request.method == 'GET':
        try:
            all_services = Service.query.all()
            all_services_data = [{'id': service.id, 'name': service.service_name} for service in all_services]

            return {'all_services': all_services_data}, 200

        except Exception as e:
            return {'error': 'An error occurred while processing the request'}, 500

    elif request.method == 'POST':
        
        try:
            current_user = get_jwt_identity()
            user = User.query.filter_by(email=current_user).first()
            args = request.json
            existing_services = args.get('existing_services', [])
            new_service_name = args.get('service_name')

            # Check if at least one service is provided
            if not existing_services and not new_service_name:
                return {'error': 'At least one service must be provided'}, 400

            # Initialize a list to hold service IDs
            service_ids = []

            # Handle existing services selected from the dropdown
            for service_id in existing_services:
                service = Service.query.get(service_id)
                if service:
                    provider_service = ProviderService(
                        provider_id=user.id,
                        service_id=service_id
                    )
                    db.session.add(provider_service)
                    service_ids.append(service_id)

            # Handle new service entered manually
            if new_service_name:
                existing_service = Service.query.filter(func.lower(Service.service_name) == func.lower(new_service_name)).first()
                if existing_service:
                    return {'error': f'Service "{new_service_name}" already exists, kindly check the list provided'}, 401

                new_service = Service(
                    service_name=new_service_name,
                    provider_id=user.id
                )
                db.session.add(new_service)
                db.session.flush()
                provider_service = ProviderService(
                    provider_id=user.id,
                    service_id=new_service.id
                )
                db.session.add(provider_service)
                service_ids.append(new_service.id)

            # Commit all changes to the database
            db.session.commit()

            return {'message': f'Services created and associated with {user.first_name} {user.last_name}', 'service_ids': service_ids}, 201

        except Exception as e:
            return {'error': 'An error occurred while processing the request'}, 500



provider_parser = reqparse.RequestParser()
provider_parser.add_argument('service_id', type=int, required=True, help='Service Id required')

class ServiceProvider(Resource):
    @jwt_required()
    def get(self):
        args = provider_parser.parse_args() 
        service_id = args['service_id']
        provider_ids = ProviderService.query.filter_by(service_id=service_id).all()
        
        if provider_ids:
            provider_ids = [provider.provider_id for provider in provider_ids]
            response = make_response({'provider_ids': provider_ids})
            return response
        else:
            response = make_response({'error': 'No Service providers found for this service'}, 404)
            return response

class ProviderList(Resource):
    @jwt_required()
    def get(self):
        provider_ids = request.args.get('provider_ids')

        if provider_ids is None:
            return {'error': 'No provider IDs provided'}, 400

        provider_ids_list = provider_ids.split(',')
        provider_ids_list = [int(provider_id) for provider_id in provider_ids_list]

        users = User.query.filter(User.id.in_(provider_ids_list)).all()

        if users:
            # Format the user data as a list of dictionaries
            user_details = [{'first_name': user.first_name, 'last_name': user.last_name} for user in users]
            return jsonify(user_details)
        else:
            return {'error': 'No users found for the given provider IDs'}, 404


class ProviderIds(Resource):
    def get(self, service_id):
        provider_ids = ProviderService.query.filter_by(service_id=service_id).all()
        if provider_ids:
            ids = [provider.provider_id for provider in provider_ids]
            response = make_response({'provider_ids': ids})
            return response
        else:
            response = make_response({'error': 'Provider ids do not exist'}, 404)
            return response

api.add_resource(ProviderList, '/provider-details')
api.add_resource(ProviderIds,'/provider-ids/<int:service_id>')

api.add_resource(ServiceProvider,'/service-provider')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(Dashboard, '/dashboard')



if __name__ == '__main__':
    app.run(debug=True, port=4000)
