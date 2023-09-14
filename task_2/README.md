# CRUD API

## Setup

Requires Python 3.8 or Later. I also used Mysql 5.7 for this project.

I recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### To Create a virtual Environment

To create a virtual environment using `pipenv`

```
pipenv install -r requirements.txt
```

This command will create and install all the require dependecies

##### To Start the environment for Windows Users

```
pipenv shell
```

#### Running Mysql Database on Linux

`Note`: If your running the code locally, you need to input the database details in `db.py`
user = "<the database user>"
password = "<the specific users password>"
host = "localhost or the where the database is hosted"
database = "<the database name>"

```

```

To `start` your server use

```
 sudo service mysql start
```

After starting you can then create the database you will need for this project by entering this commands

```
mysql -u<your mysql user name> -p<your mysql password for this specific user>
```

## Endpoints

### POST '/api'

- Create a user from the request data.
- Request:
  ```
  {
      "name": "the name of the user to be created",
      "email": "A unqiue email"
  }
  ```
- Response:
  For successfully response
  ```
  Status code: 201
  {
  "email": email,
  "message": "user created"
  }
  ```
  If the user already exists
  ```
  Status code: 400
  {
  "error": "email <email provided> already registered",
  }
  ```
  If no json data is provided in the request
  ```
  Status code: 400
  {
  "error": "you must provide a name and an email"
  }
  ```

### GET '/api/<user_id>'

- Gets the specific details for the user that own the `id`
- Request: Proide the user_id in the query parameter e.g
  ` \api\1 or api\2`
- Response JSON object of id, email and name of the specific user
  For successfully response
  ```
  Status code: 200
  {
    "id": user_id,
    "email": email,
    "name": name
  }
  ```
  If no user found
  ```
  Status code: 404
  {
    "message": "user not found"
  }
  ```

### GET '/api/<user_id>'

- update specific details for the user that own the `id`
- request: The details to change
- Response: 200 if the user is successfully updated from the database.
- Response: 404 if the user did not exist in the database

### DELETE 'api/<user_id>'

- Deletes selected question by id
- Response: 200 if the user is successfully deleted from the database.
- Response: 404 if the user did not exist in the database
- Response: "user was successfully deleted"
