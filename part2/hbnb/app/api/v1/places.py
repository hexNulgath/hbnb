from flask_restx import Namespace, Resource, fields, marshal
from app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

facade = HBnBFacade()

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

# Define an output model for marshalling responses
place_output_model = api.model('PlaceOutput', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created', model=place_output_model)
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        # Try to create the place
        try:
            new_place = facade.create_place(place_data)
            if not new_place:
                return {'error': 'Failed to create place'}, 400
        except Exception as e:
            return {'error': str(e)}, 400

        # If successful, return the new place
        return marshal(new_place, place_output_model), 201
    
    @api.response(200, 'List of places retrieved successfully', model=[place_output_model])
    def get(self):
        """Retrieve a list of all places"""
        place_list = facade.get_all_places()
        if not place_list:
            return {'error': 'No place found'}, 404
        
        return marshal(place_list, place_output_model), 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', model=place_output_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return marshal(place, place_output_model), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        facade.update_place(place_id, place_data)
        return {'message': 'Place updated successfully'}, 200
