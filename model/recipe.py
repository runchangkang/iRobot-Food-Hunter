
# The bean class for the recipe object, for maintaining future extensibility
class Recipe:
    def __init__(self,json):
        self.json = json
        self.image = None
        self.ingredients = set()
        try:
            self.rid = json["recipe_id"]
            self.title = json["title"]
            self.image_url = json["image_url"]
            self.validObject = True
        except ValueError:
            self.validObject = False




