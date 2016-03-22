# contact-list-webapp
It contains REST services in Flask (python) and Angularjs Web application. Web application using the rest service in flask.
This repo contains two folders
- **rest-service **: Flask REST services with SQLite3 DB
-  **web-app**: Simple angular js web application which used above rest service

## Prerequisites
### Prerequisites for REST service APP
- SQLite3 
- Python with these modules Flask, simplejson and flask-restful. If  you do not have them, using below commands you can install them.
```
pip install flask-restful
pip install simplejson
pip install Flask
```
### Prerequisites for REST service APP
 - NPM
 - NodeJS
  
## Staring REST services
- Start Web app in rest-service by below command
```
python simple-rest.py
```

server is start in [http://localhost:5000/](http://localhost:5000/)

### REST Service API

Adding New Contact: POST Request http://127.0.0.1:5000/<name>/<phoneNo>
eg:http://127.0.0.1:5000/jane/9456824231

List all Contacts: GET Request http://127.0.0.1:5000/
eg:http://127.0.0.1:5000/

Get One Contact: GET Request http://127.0.0.1:5000/<name>
eg:http://127.0.0.1:5000/jane

Update a Contact: PUT Request http://127.0.0.1:5000/<name>/<new-phoneNo>
eg:http://127.0.0.1:5000/jane/9456824888

## Starting Web App

Enter below command in web-app

```
npm start
```

Web App start [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

- List all contacts in SQLite3 using REST services in port 5000 
