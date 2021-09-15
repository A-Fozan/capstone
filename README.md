# Potion Market API

## Capstone Project for Udacity's Full Stack Developer Nanodegree
Heroku Link: https://potion-market-capstone-fsnd.herokuapp.com/

While running locally:  http://127.0.0.1:5000/

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).


#### Virtual Enviornment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

## Running the server

To run the server, execute:

```bash
export DATABASE_URL2=<database-connection-url>
export FLASK_APP=app.py
bash setup.sh
flask run --reload
```

Setting the `FLASK_APP` variable to `app.py` directs flask to use the `app.py` file to find the application. 

Using the `--reload` flag will detect file changes and restart the server automatically.

## API Reference

## Getting Started
This application can be run locally. 

but also there is a hosted version at `https://potion-market-capstone-fsnd.herokuapp.com/`.

Authentication: This application requires authentication to perform various actions. some endpoints require
permissions, while some do not, the authentication are passed via the `Bearer` JWT token.

The application has two different types of roles:
- wizard
  - this role has the following permistions:
  `add:bottle, update:bottl`, this role can add as well as update a bottle

- market owner
  - this role has the same permistions as the `wizard` plus these aditioan ones:
  `add:potion, add:wizard, delete:potion, delete:wizard	` 

not to forget to mention that some endpoints do not require any permistions.

required permistions will be mentioned in the endpoint section infront of each endpoint.


## Error Handling
Errors are returned as JSON objects in the following format:
```
{

    "success": False,
    "error": <error code>,
    "message": <error message>

}
```

The API will return the following errors based on how the request fails:
 - 401: Unauthorized
 - 403: Forbidden
 - 404: resource not found
 - 422: Unprocessable

## Endpoints

#### GET /wizards
 - Information
   - gets the list of all the wizards
   - no permission required 
 
 - Sample Request

   `https://potion-market-capstone-fsnd.herokuapp.com/wizards`
    
 - Sample Response

```
{
    "success":True,
    "wizards": [
        {
            "id": 1,
            "name": "Gandalf",
            "info": "he will not let you pass"
        },
        {
            "id": 2,
            "name": "the necromancer",
            "info": "say hi to his skeleton"
        },
        {
            "id": 3,
            "name": "Sauron"
            "info": "he really wants his ring back"
        }
    ]
}
```

#### GET /potions
 - Information
   - gets the list of all the potions
   - no permission required 
 
 - Sample Request

   `https://potion-market-capstone-fsnd.herokuapp.com/potions`
    
 - Sample Response

```
{
    "success":True,
    "potions": [
        {
            "id": 1,
            "name": "the invisibility potion",
            "effect": "its in the name"
        },
        {
            "id": 2,
            "name": "water breathing potion",
            "effect": "drink it and you will breath under water...or turn into a fish..."
        },
        {
            "id": 3,
            "name": "Potion Of Flying"
            "effect": "you can fly now!"
        }
    ]
}
```




#### GET /wizard_potions/[int:id]
 - Information
   - gets all the potion bottles that the wizard with the given id
   - no permission required 
 
 - Sample Request
   - `https://potion-market-capstone-fsnd.herokuapp.com/wizard_potions/1`

- Sample Response

```
{
    "success":True,
    "id":1,
    "list": [
        {
            "w_id": 1,
            "p_id": 1,
            "name": "the invisibility potion",
            "effect": "its in the name"
            "quantity": 6,
            "price": 20
        },
        {
            "w_id": 1,
            "p_id": 3,
            "name": "Potion Of Flying",
            "effect": "you can fly now!",
            "quantity": 3,
            "price": 12
        }
    ]
}
```

#### POST /wizard/add
 - Information
   - adds a new wizard
   - requires the `add:wizard` permission
 
 - Request Body 
   - name: string
   - info: string
 
 - Sample Request
   
   `https://potion-market-capstone-fsnd.herokuapp.com/wizard/add`
- Sample Request Body
     ```
       {
            "name": "Gandalf",
            "info": "he will not let you pass"
       }
     ```
- Sample Response


```
{
    ""success":True,
      "added":1
}
```

#### POST /potion/add
 - Information
   - adds a new potion
   - requires the `add:potion` permission
 
 - Request Body 
   - name: string
   - effect: string
 
 - Sample Request

   `https://potion-market-capstone-fsnd.herokuapp.com/potion/add`
- Sample Request Body
     ```
       {
            "name": "the invisibility potion",
            "effect": "its in the name"
       }
     ```
- Sample Response


```
{
    ""success":True,
      "added":1
}
```
#### POST /bottle/add
 - Information
   - adds a new bottle to a wizard
   - requires the `add:bottle` permission
 
 - Request Body 
   - w_id: string, (wizard id)
   - p_id: string, (potion id)
   - quantity: string   
   - price: string
 
 - Sample Request

   `https://potion-market-capstone-fsnd.herokuapp.com/bottle/add`
- Sample Request Body
     ```
       {
            "w_id": 1,
            "p_id": 2,
            "quantity": 6,
            "price": 23
       }
     ```
- Sample Response

```
{
    ""success":True,
      "added"::{
        "w_id":1,
        "p_id":2
      }
}
```
#### DELETE /wizard/delete/[int:id]
 - Information
   - deletes a wizard given its id
   - requires the `delete:wizard` permission
 
 - Sample Request

   `https://potion-market-capstone-fsnd.herokuapp.com/wizard/delete/1`

- Sample Response

```
{
    "success":True,
    "deleted_wizard_id":1
}
```
#### DELETE /potion/delete/[int:id]
 - Information
   - deletes a potion given its id
   - requires the `delete:potion` permission
 
 - Sample Request

   `https://potion-market-capstone-fsnd.herokuapp.com/potion/delete/1`

- Sample Response

```
{
    "success":True,
    "deleted_potion_id":1
}
```
#### PATCH /bottle/update
 - Information
   - updates `quantity`and or `price` of a bottel
   - requires the `update:bottle` permission

- Request Body 
   - w_id: string, (wizard id)
   - p_id: string, (potion id)
   - quantity: string , optional
   - price: string , optional
 
 - Sample Request

   `https://potion-market-capstone-fsnd.herokuapp.com/bottle/update`

- Sample Request Body
     ```
       {
            "w_id": 1,
            "p_id": 2,
            "quantity": 10,
            "price": 14
       }
     ```
- Sample Response

```
{
    ""success":True,
      "updated"::{
        "w_id":1,
        "p_id":2
      }
}
```
  

## Testing
For testing, run the following commands:
```
dropdb capstone_test
createdb capstone_test
python test_app.py
```
