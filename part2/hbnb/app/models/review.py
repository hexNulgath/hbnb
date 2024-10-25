from app.models.baseModel import BaseModel
import app.services.facade as facade

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        # Validate text
        if text and text is not "":
            self.text = text
        else:
            raise ValueError("text content is required")

        # Validate rating between 1 and 5
        if 1 <= rating <= 5:
            self.rating = rating
        else:
            raise ValueError("rating must be between 1 and 5")

        if self.place_exists(place_id):
            self.place_id = place_id
        else:
            raise ValueError("place not found")  
              
        if self.user_exists(user_id):
            self.user_id = user_id
        else:
            raise ValueError("user not found")


    @staticmethod
    def user_exists(user):
        """Check if the user exists in the database."""
        user_exist = facade.HBnBFacade.get_user(user)
        if user_exist:
            return True
        return False

    @staticmethod
    def place_exists(place):
        """Check if the place exists in the database."""
        place_exist = HBnBFacade.get_place(place)
        if place_exist:
            return True
        return False
