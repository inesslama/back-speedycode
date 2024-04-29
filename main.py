from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import model
from config import engine, SessionLocal 
from model import User,Message
from schemas import  LoginRequest, RegisterRequest ,MessageCreate 
from cryptography.fernet import Fernet
import binascii
import base64
import os
from dotenv import load_dotenv , dotenv_values 
import requests
import subprocess
import shutil
from requests.auth import HTTPBasicAuth

load_dotenv()



model.Base.metadata.create_all(bind=engine)


app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:4200",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


def generate_key():
    return Fernet.generate_key()


symmetric_key = base64.urlsafe_b64encode(bytes.fromhex(os.getenv("symmetric_key")))

def encrypt_password(password, key):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    hex_encrypted_password = binascii.hexlify(encrypted_password).decode()
    return hex_encrypted_password


def decrypt_password(encrypted_password_hex, key):
    cipher_suite = Fernet(key)
    encrypted_password = binascii.unhexlify(encrypted_password_hex)
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password



# database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#endpoints 

@app.post("/register")
async def register(register_request: RegisterRequest, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == register_request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    
    
    encrypted_password = encrypt_password(register_request.password, symmetric_key)
    
    
    new_user = User(username=register_request.username, email=register_request.email, password=encrypted_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Registration successful"}

@app.post("/login")
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_request.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    decrypted_password = decrypt_password(user.password, symmetric_key)
    if decrypted_password != login_request.password:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    return {"message": "Login successful"}

@app.post("/send_message")
async def save_message(message_create: MessageCreate, db: Session = Depends(get_db)):
    db_message = Message(msg=message_create.msg)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return {"message": "Message saved "}
 



@app.post("/push_bitbucket")
def push_bitbucket() :  
   bitbucket_username = os.getenv("bitbucket_username")
   bitbucket_password= os.getenv("bitbucket_password")
   repo_url = f"https://{bitbucket_username}:{bitbucket_password}@bitbucket.org/123-098/speedycode.git"
   directory = "bitbucket"
   email=os.getenv("email")
   commands = [
     
     "git init",
     "git add .",
     "git commit -m 'push the ms code to the bitbucket'",
      f"git remote add origin_bitbucket {repo_url}",
     "git push origin_bitbucket master"


    ]
   try:
       

       subprocess.run(["git", "config", "--global", "user.email", f"{email}"])
       subprocess.run(["git", "config", "--global", "user.name", f"{bitbucket_username}"])
      
       for i in commands :
            subprocess.run(i,shell=True,cwd=directory,check=True)
          
   except subprocess.CalledProcessError as exeception :
       raise HTTPException(status_code=500, detail="error")
   

   return{"message":"code pushed to bitbucket"}




@app.post("/jenkins_pipeline")
async def jenkins_pipeline():
    jenkins_username = os.getenv("jenkins_username")
    jenkins_token= os.getenv("jenkins_token")
    try:
        jenkins_url = "http://jenkins:8080"  
        pipeline_name = "login_backend_login"  
        auth = (f"{jenkins_username}", f"{jenkins_token}")  
        build_url = f"{jenkins_url}/job/{pipeline_name}/build"
        response = requests.post(build_url, auth=auth,timeout= 3600)   
        if response.status_code == 201:
            return {"message": "success!"}
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed pipeline")
    
    except requests.RequestException as e:
        print(f"Request to Jenkins failed: {str(e)}")
        raise HTTPException(status_code=500, detail="connection error")



@app.get('/')
async def Home():
    return "Welcome"
