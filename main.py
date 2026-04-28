from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return{"message":"Welcome to my backend"}

@app.get("/hello")
def hello():
    return{"message":"Hello, AI Engineer!"}

@app.get("/about")
def about():
    return{"name":"Supreet Kumar", "goal":"AI Engineer"}


@app.get("/name")
def name():
    return{"name":"Supreet Kumar"}

@app.get("/city")
def city():
    return{"city":"Bengaluru"}

@app.get("/aim")
def aim():
    return {"aim":"Become an AI Engineer"}