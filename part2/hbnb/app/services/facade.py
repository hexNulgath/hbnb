from app.persistence.repository import InMemoryRepository
from app.models.user import User
class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user
    
    def get_all_user(self):
        return self.user_repo.get_all()
    
    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, data):
        return self.user_repo.update_user(user_id, data)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def create_amenity(self, amenity_data):
        amenity = amenity(**amenity_data)
        self.amenity_repo_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
        

    def get_all_amenities(self):
         return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        return self.amenity_repo.update_amenity(amenity_id, amenity_data)