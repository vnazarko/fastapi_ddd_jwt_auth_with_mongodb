This is a FastAPI application with JWT authorization, written using DDD architecture. The MongoDB database with asynchronous Motor driver is used here. [Poetry](https://python-poetry.org/docs/) is used to manage dependencies.
Preparing to launch the application:
 - ```shell
   # Creating a virtual environment
   poetry config virtualenvs.in-project true
   # Activation a virtual environment
   poetry shell 
   # Installing dependencies
   poetry install 
   ```
 - Create a `certs` folder in the root of the project and run the following commands in it:
    ```shell
    # Genetate an RSA private key, of size 2048
    openssl genrsa -out jwt-private.pem 2048
    # Extract the public key from the key pair, which can be used in a certificate
    openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
    ```
 - Now create it .the env file, it should look something like this:
   ```
   DB_URL='mongodb://user_db:password_db@localhost:27017'
   USERS_COLLECTION='users'
   # Settings for MongoDB
   MONGO_INITDB_ROOT_USERNAME=user_db
   MONGO_INITDB_ROOT_PASSWORD=password_db
   ```
Now everything is ready, now you need to enter the following command in the root of the project:
```shell
uvicorn src.main:app --reload
```
In order to create secure routes, you need to add the following to the function parameters:
```python 
user: User = Depends(auth_service.get_user_from_access)
# your function will need to look like this
async def test(user: User = Depends(auth_service.get_user_from_access)):
```