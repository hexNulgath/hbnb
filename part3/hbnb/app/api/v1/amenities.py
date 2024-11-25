from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from app.models.amenity import Amenity

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Define the output model for documentation and response marshalling
amenity_output_model = api.model('AmenityOutput', {
    'id': fields.String(description='The amenity ID'),
    'name': fields.String(description='The amenity name'),
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created', model=amenity_output_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return marshal({'id': new_amenity.id, 'name': new_amenity.name}, amenity_output_model), 201

    @api.response(200, 'List of amenities retrieved successfully', model=[amenity_output_model])
    def get(self):
        """Retrieve a list of all amenities"""
        amenity_list = facade.get_all_amenities()
        if not amenity_list:
            return {'error': 'No amenities found'}, 404
        return marshal(amenity_list, amenity_output_model), 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully', model=amenity_output_model)
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return marshal({'id': amenity.id, 'name': amenity.name}, amenity_output_model), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity by ID"""
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        facade.update_amenity(amenity_id, amenity_data)
        return {'message': 'Amenity updated successfully'}, 200

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created', model=amenity_output_model)
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to create a new amenity
        amenity_data = api.payload

        new_amenity = facade.create_amenity(amenity_data)
        return marshal({'id': new_amenity.id, 'name': new_amenity.name}, amenity_output_model), 201

@api.expect(amenity_model)
@api.response(200, 'Amenity updated successfully')
@api.response(404, 'Amenity not found')
@api.response(400, 'Invalid input data')
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        # Logic to update an amenity
        amenity_data = api.payload
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        facade.update_amenity(amenity_id, amenity_data)
        return {'message': 'Amenity updated successfully'}, 200
