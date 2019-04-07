# iRobot-Food-Hunter

#### Introduction
This is the take home assignment for the iRobot Cloud Software Team Software Engineer position.

Food Hunter is a tiny Python application that allows user type in food ingredients and search the most popular recipe from food2fork.com API.

The application will inform the user with the ingredients that still missing. 

#### How to run?
##### Please make sure the python version is 3.6

to check version, please open terminal type `$ python --version`

##### Please also download the PyQt5 library 

`$ pip install pyqt5`

##### Please enter your food2fork.com API Key
locate the /resource/config.py

enter your api key after the api_key variable

in config.py

    api_key = "YOUR_API_KEY" 
    

##### Run the program by
    $ python main.py
    
    
#### How to use?
Type in ingredient name in the textField and press **Add**

After typed in enough ingredients, press **Search**

To clear all previous ingredients, press **Clear All**

To remove the ingredient, select it in the list table and press **"-"**

