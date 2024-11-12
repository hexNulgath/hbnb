from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# Define related entity models
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

# Place model for marshalling response
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

# Output model
place_output_model = api.model('PlaceOutput', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner': fields.Nested(user_model, description='Owner of the place')
})

# Input model for validation
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner')
})

# Listing model for list responses
place_list_model = api.model('PlaceListing', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_input_model)
    @api.response(201, 'Place successfully created', model=place_output_model)
    @api.response(400, 'Invalid input data')
    @jwt_required()
    @api.response(404, 'User not found')
    def post(self):
        """Register a new place"""
        place_data = api.payload
        current_user = get_jwt_identity()
        place_owner = place_data['owner_id']
        if place_owner != current_user["id"]:
            return {'error': 'Unauthorized action'}, 403
        
        user_data = facade.get_user(place_owner)

        if not user_data:
           return {'error': 'User not foundi'}, 404

        # Add owner object to place data
        place_data['owner'] = user_data

        try:
            new_place = facade.create_place(place_data)
            if not new_place:
                return {'error': 'Failed to create place'}, 400
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An internal error occurred'}, 500

        return marshal(new_place, place_output_model), 201

    @api.response(200, 'List of places retrieved successfully', model=[place_list_model])
    def get(self):
        """Retrieve a list of all places"""
        place_list = facade.get_all_places()
        if not place_list:
            return {'error': 'No place found'}, 404
        return marshal(place_list, place_list_model), 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully', model=place_output_model)
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return marshal(place, place_model), 200

    @api.expect(place_input_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        place_data = api.payload
        current_user = get_jwt_identity()
        place = facade.get_place(place_data['id'])
        if place != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404 
        try:
            facade.update_place(place_id, place_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'An internal error occurred'}, 500

        return {'message': 'Place updated successfully'}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        review_list = facade.get_reviews_by_place(place_id)
        if not review_list:
            return {'error': 'No reviews found'}, 404
        return marshal(review_list, review_model), 200
