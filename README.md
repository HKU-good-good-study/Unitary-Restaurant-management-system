# Unitary-Restaurant-management-system

## Setup

If virtual enviroment not yet created, use: ```python -m venv EnvironmentPathYouWish``` (Don't forget to add your virtual enviroment folder into .gitignore if it is in project directory's scope)

If virtual enviroment is created, use command: ```YourEnvironmentPath/Script/activate``` to activate your virtual environment

- install requriement using ```pip install -r requirement.txt```
- Install Node.js (latest LST version)

## How to run this app:

**Frontend**:(Sevelte)
Go to directory ```frontend```
If first time: Run command ```npm install```.
Run with command ```npm run dev``` to start frontend service.


**Backend**: (FastAPI)
Go to directory ```backend```
Run with command:   ```uvicorn main:app --reload```/```python main.py``` to start backend service.

**Database**
Run MongoDB client: Default using localhost with port 27017
