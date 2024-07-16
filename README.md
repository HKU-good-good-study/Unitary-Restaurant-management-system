# Unitary-Restaurant-management-system

## Way(s) to setup this app:

If virtual enviroment (**Recommand**) not yet created, use: ```python -m venv EnvironmentPathYouWish``` (Don't forget to add your virtual enviroment folder into .gitignore if it is in project directory's scope)

After virtual enviroment is created, use command: ```YourEnvironmentPath/Script/activate``` to activate your virtual environment

**Frontend**:(Sevelte)
1. Install Node.js (latest LST version)
2. Go to directory ```frontend```
3. Run command ```npm install```.

**Backend**: (FastAPI)

Install requriement using ```pip install -r requirement.txt```

## How to run this app:

**Frontend**:

Go to directory ```frontend```
Run command ```npm run dev``` to start frontend service.

**Backend**: 

Go to directory ```backend```
Run with command:   ```uvicorn main:app --reload```/```python main.py``` to start backend service.

**Database**

Run MongoDB client: Default using localhost with port 27017 (Recommand to use MongoDB compass to visualize data)
