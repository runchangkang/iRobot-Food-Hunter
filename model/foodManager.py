# -*- coding: utf-8 -*-


from urllib import parse
from urllib import request
from PyQt5.QtCore import QThread,pyqtSignal
import json
from model.recipe import Recipe
from model.config import api_key


# The manager of the recipe, handling the fetch, parse and return tasks
class FoodManager:

    baseUrl =  "https://www.food2fork.com/api/"
    searchPath = "search?"
    getPath = "get?"
    spoofedUserAgentHeader = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"


    def __init__(self):
        self.userInputIngredient = set()
        self.params = {"key":api_key,"q" : ""}
        self.recipe = None

    # add ingredient into the manager
    def addUserIngredients(self, str):
        self.userInputIngredient.add(str.lower())

    #search by current ingredients
    def searchByExistingIngredients(self):
        if len(self.userInputIngredient) == 0 :
            return 0,"","","Please enter some ingredients first!"

        self.params["q"] = " ".join(self.userInputIngredient)
        existing = ""
        missing = ""
        url = FoodManager.baseUrl + FoodManager.searchPath + parse.urlencode(self.params)
        result = self.getDataFromUrl(url)
        if result:
            amount = result['count']
            if amount == 0:

                return 0,existing,missing,"Cannot find recipe based on your input, please double check your input."


            recipe = Recipe(result["recipes"][0])
            if recipe.validObject:
                self.recipe = recipe
                self.getRecipeIngredients(recipe)

                existing,missing = self.checkRecipeIngredientsWithUserIngredients(recipe,self.userInputIngredient )

                return 1,existing,missing,"Try this one!"
            else:

                return 0,existing,missing,"Data corrupted, please try again."
        else:

            return 0,existing,missing,"Internet error, please try again later."

    # comparing and calculating the missing ingredients
    def checkRecipeIngredientsWithUserIngredients(self,recipe,userInputIngredientSet):
        ingredients = recipe.ingredients
        existingSet = set()
        missingSet = set()
        for userIngredient in userInputIngredientSet:
            for recipeIngredient in ingredients:
                if userIngredient in recipeIngredient.lower():
                    existingSet.add(recipeIngredient)
        for recipeIngredient in ingredients:
            if recipeIngredient not in existingSet:
                missingSet.add(recipeIngredient)
        return "\n".join(existingSet), "\n".join(missingSet)

    # a helper function that connect to the internet and fetch data from the user
    # input url
    def getDataFromUrl(self,url):
        req = request.Request(
            url,
            data=None,
            headers={
                'User-Agent': FoodManager.spoofedUserAgentHeader
            }
        )
        try:
            response = request.urlopen(req)
            if response.code != 200:
                return None
            result = json.loads(response.read())
            return result
        except:
            return None

    # get the ingredient by the recipe ID
    def getRecipeIngredients(self, recipe):
        params = {"key": api_key, "rId": recipe.rid}
        url = FoodManager.baseUrl + FoodManager.getPath + parse.urlencode(params)

        result = self.getDataFromUrl(url)
        if(result):
            data = result["recipe"]
            recipe.ingredients.update(data["ingredients"])

    # clear the existing ingredients
    def clear(self):
        self.userInputIngredient = set()
        self.params = {"key": api_key, "q": ""}
        self.recipe = None

    # remove the selected ingredient
    def remove(self,item):
        if item in self.userInputIngredient:
            self.userInputIngredient.remove(item)






# The QThread class for dispatching the GUI and the fetching
# It will emit signal with data when the fetching finished
class FetchContentThread(QThread):
    result = pyqtSignal(int,str,str,str)
    def __init__(self,model):
        QThread.__init__(self)
        self.model = model

    def __del__(self):
        self.wait()
    def run(self):
        isSuccess,existing,missing,msg = self.model.searchByExistingIngredients()
        self.result.emit(isSuccess,existing,missing,msg)

