from flask_restx import Namespace, Resource, fields, marshal
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_input_model = api.model('Input_review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

update_review_model = api.model('Update_review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
})

# Define the review model for output
review_model = api.model('Review', {
    'id': fields.String(required=True, description='ID of the review'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_output_model = api.model('Review_output', {
    'id': fields.String(required=True, description='ID of the review'),
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

facade = HBnBFacade()

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_input_model)
    @api.response(201, 'Review successfully created', model=review_output_model)
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'An internal error occurred while creating the review'}, 500
        return marshal(new_review, review_output_model), 201

    @api.response(200, 'List of reviews retrieved successfully', model=[review_output_model])
    def get(self):
        """Retrieve a list of all reviews"""
        review_list = facade.get_all_reviews()
        if not review_list:
            return {'error': 'No reviews found'}, 404
        return marshal(review_list, review_output_model), 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully', model=review_model)
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review is None:
            return {'error': 'Review not found'}, 404
        return marshal(review, review_model), 200

    @api.expect(update_review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        try:
            facade.update_review(review_id, review_data)
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'An internal error occurred while updating the review'}, 500
        return {'message': 'Review updated successfully'}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid review ID')
    def delete(self, review_id):
        """Delete a review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        try:
            facade.delete_review(review_id)
        except Exception:
            return {'error': 'An internal error occurred while deleting the review'}, 500
        return {'message': 'Review deleted successfully'}, 200
