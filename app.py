import fastapi 
import fastapi.security as security
import sqlalchemy.orm as orm
import schemas
import services
import jwt

app=fastapi.FastAPI()

@app.post("/api/v1/users")
async def register_user(
    user:schemas.UserRequest,db:orm.Session=fastapi.Depends(services.get_db())
       
):
    # check if user with email exists
    db_user=await services.getUserByEmail(email=user.email,db=db)
    if db_user:
        raise fastapi.HTTPException(status_code=400,detail="User with this email already exists")
    # create user and return token
    