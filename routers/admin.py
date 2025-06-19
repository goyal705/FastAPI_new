from fastapi import Depends,Response,status,HTTPException,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import desc
from database import *
from schemas import *
from models import *
from .token import *
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Admin"],
    prefix='/admin'
)

@router.get("/request-user-create")
def get_all_user_create_request(request: Request,user_status:Optional[str] = None, _=Depends(verify_access_token),db: Session = Depends(get_db)):
    role = request.state.user_data.get("role")
    if role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admins allowed for this operation"
        )
    if user_status == "Pending":
        all_objects = db.query(AdminRecords).filter(AdminRecords.approved == False,AdminRecords.is_active == True).all()
    elif user_status == "Approved":
        all_objects = db.query(AdminRecords).filter(AdminRecords.approved == True,AdminRecords.is_active == True).all()
    else:
        all_objects = db.query(AdminRecords).filter(AdminRecords.is_active == True).all()
    return {"status":True,"data":all_objects}

@router.post("/approve-reject-user")
def approve_reject_user(response:Response,request: Request,body:AdminApproveRejectRequest, _=Depends(verify_access_token),db: Session = Depends(get_db)):
    role = request.state.user_data.get("role")
    if role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admins allowed for this operation"
        )
    
    user = db.query(AdminRecords).filter(AdminRecords.username == body.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found"
        )
        
    action = body.action
    if action and (action == "Approve" or action.lower() == "approve"):
        if user.approved:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Request already approved"
        )   
        user_entry = Users(
            name = user.name,
            username = user.username,
            mobile = user.mobile,
            email = user.email,
            password = user.password,
            role = user.role,
            is_active = True
        )
        user.approved = True
        user.is_active = False
        db.add(user_entry)
        db.commit()
        db.refresh(user_entry)
        response.status_code = status.HTTP_201_CREATED
        return {"status":True,"message":"User Profile Activated"}
        
    elif action and (action == "Reject" or action.lower() == "reject"):
        if user.approved:
            raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Request already approved"
        )
        user.approved = False
        user.is_active = False
        db.commit()
        response.status_code = status.HTTP_200_OK
        return {"status":True,"message":"User Profile Created Request Rejected"}
    
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Action Not Allowded"
        )

    
    