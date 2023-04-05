from pydantic import BaseModel, validator,constr
from typing import Optional
from fastapi_jwt_auth import AuthJWT

class SignUpModel(BaseModel):
    id:Optional[str]
    email:str
    firstname:str
    lastname:str
    phone_number:constr(min_length=10, max_length=10) = None
    profilepicture:str = None
    password:str
    confirmpassword:str
    is_seller:Optional[bool] = False
    is_buyer:Optional[bool] = True
    is_staff:Optional[bool] = False
    
    @validator('confirmpassword')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

    class Config: 
        orm_mode=True
        schema_extra={
            'example':{
            'email':'johndoe@gmail.com',
            'firstname':'john',
            'lastname':'doe',
            'phone_number': '0702567895',
            'profilepicture':'profilepicture.jpg',
            'password':'password',
            'confirmpassword':'password',
            'is_seller':False,
            'is_buyer':True,
            'is_staff':False,

            }
        }
class Settings(BaseModel):
    authjwt_secret_key:str='dac6225e7545f69ca1cedebfe7cec4cadceb58f3fe32197a724b957bdfe0d123'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
class LoginModel(BaseModel):
    email:str
    password:str
    
    class Config:
        orm_mode=True
        schema_extra={
            'example':{
  "email": "diana@gmail.com",
  "password": "diana"
}
        }
        
                    