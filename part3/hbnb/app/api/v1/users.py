from urllib import request
from flask_restx import Namespace, Resource, fields, marshal
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_output_model = api.model('UserOutput', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', model=user_output_model)
    @api.response(409, 'Email already registered', model=error_model)
    @api.response(400, 'Invalid input data', model=error_model)
    def post(self):
        """Register a new user"""
        try:
            user_data = api.payload
            # Check for email uniqueness
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return marshal({'error': 'Email already registered'}, error_model), 409
            new_user = facade.create_user(user_data)
            if not new_user:
                return marshal({'error': 'Invalid input data'}, error_model), 400
            return marshal(new_user, user_output_model), 201
        except ValueError as ve:
            # Handling specific validation errors
            return marshal({'error': str(ve)}, error_model), 400
        except Exception as e:
            # Catch unexpected exceptions to prevent 500 errors
            return marshal({'error': 'An internal error occurred'}, error_model), 500
    
    
    @api.response(200, 'User details retrieved successfully', model=[user_output_model])
    @api.response(404, 'No users found', model=error_model)
    def get(self):
        """Get all users"""
        user_list = facade.get_all_users()
        if not user_list:
            return marshal({'error': 'No users found'}, error_model), 404

        return marshal(user_list, user_output_model), 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully', model=user_output_model)
    @api.response(404, 'User not found', model=error_model)
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if user is None:
            return marshal({'error': 'User not found'}, error_model), 404

        return marshal(user, user_output_model), 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully', model=user_output_model)
    @api.response(404, 'User not found', model=error_model)
    @api.response(400, 'Invalid input data', model=error_model)
    @jwt_required()
    def put(self, user_id):
        """Update a user by ID"""
        user_data = api.payload
        current_user_id = get_jwt_identity()
        user = facade.get_user(user_id)
        
        # Authorization check
        if not user or user.id != current_user_id:
            return marshal({'error': 'Unauthorized action'}, error_model), 403
        
        # Restrict email and password modifications
        if 'email' in user_data and user_data['email'] != user.email:
            return marshal({'error': 'You cannot modify the email.'}, error_model), 400
        if 'password' in user_data and not user.verify_password(user_data['password']):
            return marshal({'error': 'Incorrect password.'}, error_model), 400
        
        # Perform update
        facade.update_user(user_id, user_data)
        updated_user = facade.get_user(user_id)

        return marshal(updated_user, user_output_model), 200
    
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created', model=user_output_model)
    @api.response(409, 'Email already registered', model=error_model)
    @api.response(400, 'Invalid input data', model=error_model)
    @api.route('/users/')
    class AdminUserCreate(Resource):
        @jwt_required()
        def post(self):
            """Create user using admin jws"""
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403

            user_data = request.json
            email = user_data.get('email')

            # Check if email is already in use
            if facade.get_user_by_email(email):
                return {'error': 'Email already registered'}, 400

            # Logic to create a new user
            new_user = facade.create_user(user_data)
            return marshal(new_user, user_output_model), 201


    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully', model=user_output_model)
    @api.response(404, 'User not found', model=error_model)
    @api.response(400, 'Invalid input data', model=error_model)
    @api.route('/users/<user_id>')
    class AdminUserModify(Resource):
        @jwt_required()
        def put(self, user_id):
            """Update user using admin jws"""
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                return {'error': 'Admin privileges required'}, 403

            data = request.json
            email = data.get('email')

            # Ensure email uniqueness
            if email:
                existing_user = facade.get_user_by_email(email)
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already in use'}, 400

            # Logic to update user details
            facade.update_user(user_id, data)
            updated_user = facade.get_user(user_id)

            return marshal(updated_user, user_output_model), 200