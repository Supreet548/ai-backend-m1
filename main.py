from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return{"message":"welcome to my backend"}

@app.get("/hello")
def hello():
    return{"message":"Hello, AI Engineer!"}

@app.get("/about")
def about():
    return{"name":"Supreet Kumar", "goal":"AI Engineer"}