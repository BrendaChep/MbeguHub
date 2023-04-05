from fastapi import APIRouter,status,Depends, Request, Body, Form, File, UploadFile
from database import Session, engine
from schemas import SignUpModel,LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")

auth_router = APIRouter(
    prefix = '/auth',
    tags=['auth']
) 

session = Session(bind=engine)

@auth_router.get('/',response_class=HTMLResponse)
async def hello(request: Request):    
    return templates.TemplateResponse("another.html", {"request": request}) 

@auth_router.post('/signup',response_model=SignUpModel,status_code=status.HTTP_201_CREATED)
async def signup(email: str = Form(...),firstname: str = Form(...),lastname: str = Form(...),phone_number: str = Form(...),password: str = Form(...),confirmpassword: str = Form(...)):

    """
    Creates a user. This requires the following
    ```
            'email':'johndoe@gmail.com',
            'firstname':'john',
            'lastname':'doe',
            'password':'password',
            'confirmpassword':'password',
    ```    
    """

    db_email = session.query(User).filter(User.email==email).first()

    if db_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User with the email already exists')    
    try:
        new_user = User(
            email = email,
            firstname = firstname,
            lastname = lastname,
            phone_number = phone_number,
            password = generate_password_hash(password)
        )

        session.add(new_user)
        session.commit()
        print(new_user)

        return new_user
    except:
        session.rollback()
        raise
    finally:
        # always close the session
        session.close()
        
#login route
@auth_router.post('/login', response_model = LoginModel,status_code=status.HTTP_200_OK,response_class=HTMLResponse)
async def login(request: Request,email: str = Form(...), password: str = Form(...), Authorize: AuthJWT = Depends()):

    """
    Login a user. This requires the following
    ```
    email:string
    password:string
    ```  
    and returns a token pair of 'access' and 'refresh'  
    """
    db_user=session.query(User).filter(User.email==email).first()
    if db_user and check_password_hash(db_user.password, password):
        access_token=Authorize.create_access_token(subject=db_user.email)
        refresh_token=Authorize.create_refresh_token(subject=db_user.email)

        response = templates.TemplateResponse("signin.html", {"request": request})
        response.set_cookie(key="access_token", value=access_token)
        return response

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Email or Password')


