from app.models.baseModel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()

        # Validate text
        if text and text != "":
            self.text = text
        else:
            raise ValueError("text content is required")

        # Validate rating between 1 and 5
        if 1 <= rating <= 5:
            self.rating = rating
        else:
            raise ValueError("rating must be between 1 and 5")

        # Validate place and user
        if self.place_exists(place_id):
            self.place_id = place_id
        else:
            raise ValueError("place not found")  
              
        if self.user_exists(user_id):
            self.user_id = user_id
        else:
            raise ValueError("user not found")

    def user_exists(self, user_id):
#        """Check if the user exists in the database."""
#        from app.services.facade import HBnBFacade  # Delayed import to avoid circular dependency
#        facade = HBnBFacade()
#        user_exist = facade.get_user(user_id)
#        return user_exist and 'error' not in user_exist
        return True

    def place_exists(self, place_id):
    #   """Check if the place exists in the database."""
    #   from app.services.facade import HBnBFacade  # Delayed import to avoid circular dependency
    #   facade = HBnBFacade()
    #   place_exist = facade.get_place(place_id)
    #   return place_exist and 'error' not in place_exist
        return True