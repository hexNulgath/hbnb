import part2.hbnb.app.models.baseModel as baseModel
import part2.hbnb.app.models.user as User
import part2.hbnb.app.models.place as Place

class Review(baseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if text:
            self.text = text
        else:
            raise ValueError("text content is required")
        if rating > 0 and rating < 5:
            self.rating = rating
        else:
            raise ValueError("rating must be between 1 and 5")
        if isinstance(user, User):
            self.user = user
        else:
            raise ValueError("invalid user")
        if isinstance(place, Place):
            self.place = place
        else:
            raise ValueError("invalid place")