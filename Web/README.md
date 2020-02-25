# WebSite
## About
Under the FlaksServer directory, there are 9 folders. The Breed_Cat, Breed_Dog, Cat_vs_Dog, Emotion_Cat and Emotion_Dog folder  contain the corresponding models and helper functions. The scripts directory contaisn the files which using the above models to predict. The static folder contains the images resources and the css and js libraries. The templates directory contains the html files. The testImages file used for temporarily store the image for prediction. The app.py file contains the server functions. Get trained models from [models](https://drive.google.com/drive/folders/19c2oPX0XAdVnRjaE3_o9EvLeQ4EyRzII?usp=sharing) 

## Run on Flask 
For runing the back-end server:

  `cd ~/Web/FlaskServer`

  `pip install -r requirements.txt`

  `export FLASK_APP=app.py`

  `flask run --host=0.0.0.0`

Then you can visit the website on your localhost and the port is 5000. But run on this way, only one user can access the website simultaneously.

## Run on Gunicorn
Using Gunicorn to run the server:

  `cd ~/Web/FlaskServer`

  `pip install -r requirements.txt`

  `gunicorn -b 0.0.0.0:5000 -t 60 app:app`

Then you can visit the website on your localhost and the port is 5000. On this way, the website can be visited by multiple users simultaneously.

## Run using docker 
Docker can run the server in a container which contains alll needed enviroment. With docker installed, you need to follow the bolow command: 

 `sudo docker pull codegod/my_flask_server:v2`

 `sudo docker run -p 5000:5000 --name petSmile -i -t codegod/my_flask_server:v2 /bin/bash`

Then, you can follow the above examples to run the server inside the container on Flask or Gunicorn without the install requirements.txt step.

## Research Cloud 
We deployed our server on the University of Melbourne research cloud. If connected The University of Melbourne's network, you can visit our website at [this link](45.113.232.117:5000)