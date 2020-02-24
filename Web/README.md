# WebSite
## About
Under the FlaksServer directory, there are 9 folders. The Breed_Cat, Breed_Dog, Cat_vs_Dog, Emotion_Cat and Emotion_Dog folder  contain the corresponding models and helper functions. The scripts directory contaisn the files which using the above models to predict. The static folder contains the images resources and the css and js libraries. The templates directory contains the html files. The testImages file used for temporarily store the image for prediction. The app.py file contains the server functions. 

## Run on Flask 
For runing the back-end server:

  `cd ~/Web/FlaskServer`

  `pip install -r requirements.txt`

  `export FLASK_APP=app.py`

  `flask run --host 0.0.0.0:5000`

Then you can visit the website on your localhost and the port is 5000. But run on this way, only one user can access the website simultaneously.

## Run on Gunicorn
Using Gunicorn to run the server:

  `cd ~/Web/FlaskServer`

  `pip install -r requirements.txt`

  `export FLASK_APP=app.py`

  `gunicorn -b 127.0.0.1:4000 app:app`

Then you can visit the website on your localhost and the port is 5000. On this way, the website can be visited by multiple users simultaneously.

## Run using docker 
Docker can run the server in a container which contains alll needed enviroment. With docker installed, you need to follow the bolow command: 

 `sudo docker pull codegod/my_flask_server`

 `sudo docker run --name give_container_a_name -d -p 5000:5000 codegod/my_flask_server`

Then, you can follow the above examples to run the server inside the container on Flask or Gunicorn