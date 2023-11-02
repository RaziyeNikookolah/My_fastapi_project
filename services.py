import database 
import models
import sqlalchemy.orm as orm
import schemas
import email_validator
import fastapi
import passlib.hash as hash

def create_db():
    return database.Base.metadata.create_all(bind=database.engine)

def get_db():
    db=database.SessionLocal()
    try :
        yield db
    finally:
        db.close()



async def getUserByEmail(email:str,db:orm.Session):
    return db.query(models.UserModel).filter(models.UserModel.email==email).first()

async def create_user(user:schemas.UserRequest,db:orm.Session):
    
    try:
        isvalid=email_validator.validate_email(email=user.email)
        email=isvalid.email
        
    except email_validator.EmailNotValidError:
        
        raise fastapi.HTTPException(status_code=400,detail="Provide valid Email")
    
    #create the user model to be saved
    user_obj=models.UserModel(
        email=email,
        name=user.name,
        phone=user.phone,
        #convert normal password to hash form
        password_hash=hash.bcrypt.hash(user.password)       
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj



