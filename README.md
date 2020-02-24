# Pet Smile 
This is a project that using deep learning to predict dog and cat's emotion. There is four parts in this project, which are deep learning models, website, Andorid and IOS application. 

## Model
The model directory contains the [trained models](https://drive.google.com/drive/folders/19c2oPX0XAdVnRjaE3_o9EvLeQ4EyRzII?usp=sharing), emotion training files and data preprocess files of this project. 

## Web
The web directory contains the website's front-end and back-end. For runing the back-end server 

  `cd ~/Web/FlaskServer`

  `pip install -r requirements.txt`

  `export FLASK_APP=app.py`

  `flask run --host=0.0.0.0:5000`

Then you can visit the website on your localhost and the port is 5000.

## Andorid
The Andorid directory contains the source code of  the Andorid application. The main function of this application is to predict pet’s emotion. In addition, there are also some auxiliary functions to enhance the usability such as histroy, predicting pet's type and breed. 

## IOS
The IOS directory contains the source code of the IOS applicaiton. The IOS application has the exact same functions with Android application. 