from jose import  jwt
from datetime import datetime,timedelta

SECRET_KEY = "5da533deab4ffc924687b5a5780a4b49dc01fe02416351611616ae3cc00d265c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # minutes


def create_jwt_token(data : dict):
    to_encode = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp" : exp})
    encoded_jwt = jwt.encode(to_encode, #payload
                             key=SECRET_KEY, #secret key
                             algorithm=ALGORITHM #algorithm
                             
                             )

    return encoded_jwt