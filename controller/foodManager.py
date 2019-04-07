# -*- coding: utf-8 -*-
# author: Runchang Kang (runchangkang.com)

from urllib import parse
from urllib import request
from PyQt5.QtCore import QThread,pyqtSignal
import json
from model.recipe import Recipe
from resource.config import api_key
import resource.statusMessage as sm


# The manager of the recipe, handling the fetch, parse and return tasks
class FoodManager:

    baseUrl =  "https://www.food2fork.com/api/"
    searchPath = "search?"
    getPath = "get?"
    spoofedUserAgentHeader = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
    basicParams = {"key":api_key,"q" : "","sort" : "r"}

    def __init__(self):
        self.userInputIngredient = set()
        self.params = FoodManager.basicParams
        self.recipe = None

    # add ingredient into the manager
    def addUserIngredients(self, str):
        self.userInputIngredient.add(str.lower())

    # search by current ingredients
    # return : (success flag(int), existing ingredients(str), missing ingredients(str), system message(str))
    def searchByExistingIngredients(self):
        if self.params["key"] == "":
            return 0,"","",sm.NO_KEY
        if len(self.userInputIngredient) == 0 :
            return 0,"","",sm.NO_INPUT

        self.params["q"] = " ".join(self.userInputIngredient)
        existing = ""
        missing = ""
        url = FoodManager.baseUrl + FoodManager.searchPath + parse.urlencode(self.params)
        result = self.getDataFromUrl(url)
        if result:
            amount = result['count']
            if amount == 0:
                return 0,existing,missing,sm.NO_RESULT
            recipe = Recipe(result["recipes"][0])
            if recipe.validObject:
                self.recipe = recipe
                self.getRecipeIngredients(recipe)

                existing,missing = self.checkRecipeIngredientsWithUserIngredients(recipe,self.userInputIngredient )

                return 1,existing,missing,sm.SUCCESS
            else:

                return 0,existing,missing,sm.DATA_ERROR
        else:

            return 0,existing,missing,sm.INTERNET_ERROR

    # comparing and calculating the missing ingredients
    def checkRecipeIngredientsWithUserIngredients(self,recipe,userInputIngredientSet):
        ingredients = recipe.ingredients
        existingSet = set()
        missingList = []
        for userIngredient in userInputIngredientSet:
            for recipeIngredient in ingredients:
                if userIngredient in recipeIngredient.lower():
                    existingSet.add(recipeIngredient)
        for recipeIngredient in ingredients:
            if recipeIngredient not in existingSet and not recipeIngredient.isspace():
                missingList.append(recipeIngredient)
        return "\n".join(existingSet), "\n".join(missingList)

    # a helper function that connect to the internet and fetch data from the url
    def getDataFromUrl(self,url):
        req = request.Request(url,data=None,headers={'User-Agent': FoodManager.spoofedUserAgentHeader})
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
        self.params = FoodManager.basicParams
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

