from fastapi import Depends,Response,status,HTTPException,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import desc
from database import *
from schemas import *
from models import *
from .token import *
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Users"],
    prefix='/user'
)
    
@router.post("/create_user",status_code=status.HTTP_201_CREATED)
def create_user(request:User, response: Response ,db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(
        (Users.username == request.username) |
        (Users.email == request.email) |
        (Users.mobile == request.mobile)
    ).first()
    
    if existing_user:
        if existing_user.username == request.username:
            detail = "User with same username already exists"
        elif existing_user.email == request.email:
            detail = "User with same email already exists"
        elif existing_user.mobile == request.mobile:
            detail = "User with same mobile number already exists"
        else:
            detail = "Duplicate user"

        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": False, "message": detail}
    
    new_user = Users(
        name=request.name,
        username=request.username,
        mobile=request.mobile,
        email=request.email,
        role=request.role
    )
    
    new_user.set_password(request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Username"
        )

    if not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password matching failed"
        )

    access_token = create_access_token(data={"user_id": user.user_id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
    
@router.get("/user-detail",response_model=UserOut)
def get_user_details(response:Response,request: Request, _=Depends(verify_access_token), db: Session = Depends(get_db)):
    user_id = request.state.user_data.get("user_id")
    user = db.query(Users).filter(
        Users.user_id == user_id
    ).first()
    
    if not user:
        response.status_code = 404
        return {"status":False,"message":"User details not found"}
    
    return user

@router.post("/send-otp")
def send_otp(response:Response ,mobile_no:int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.mobile == mobile_no).first()
    if not user:
        response.status_code = 404
        return {
            "status":False,
            "message":"Mobile not associated with any user"
            }
    
    old_otp = (
            db.query(OtpRecords)
            .filter(OtpRecords.user_id == user.user_id)
            .order_by(desc(OtpRecords.created_at))
            .first()
    )
    current_time = datetime.now(timezone.utc)
    if old_otp and (current_time - old_otp.created_at) < timedelta(minutes=1):
        return {
            "status": True,
            "otp": old_otp.otp,
            "message": "OTP already generated within the last minute"
        }
    
    static_otp = 123456
    
    otp_entry = OtpRecords(
        user_id=user.user_id,
        mobile_no=user.mobile,
        otp=static_otp,
    )
    db.add(otp_entry)
    db.commit()
    db.refresh(otp_entry)
    
    response.status_code = status.HTTP_201_CREATED
    return {
        "status":True,
        "otp":static_otp,
        "message":"Otp generated sucessfully"
    }
    
@router.post("/verify-otp")
def verify_otp(response:Response ,mobile_no:int,otp:int, db: Session = Depends(get_db)):
    otp_entry = (
            db.query(OtpRecords)
            .filter(OtpRecords.mobile_no == mobile_no,OtpRecords.otp == otp)
            .order_by(desc(OtpRecords.created_at))
            .first()
    )
    
    if not otp_entry:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status":False,
            "message":"No otp generated for the user or user not found"
        }
    
    if (otp_entry.expire_at - otp_entry.created_at) > timedelta(15):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "status":False,
            "message":"Otp expired please generate again"
        }
        
    access_token = create_access_token(data={"user_id": otp_entry.user_id})
    return {
        "status":True,
        "access_token": access_token,
        "token_type": "bearer"
    }
    
    