from dotenv import load_dotenv
#load_dotenv()
from app.email_agent import email_agent
#from app.tools.tool_test import user_report_complaint, user_question, classify_question
from app.db.schemas.responses import APIResponse, StatusEnum
from app.db.schemas.emailrequest import EmailRequest
from app.email_parser import parse_email
from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.Complaints import Base
from app.db.session import engine
from email.utils import parseaddr






app = FastAPI()
def user_email_response(email_content: str, user_ema,db: Session):
    
    response = email_agent( email_content,user_ema,db)
  

    return response

@app.post("/email_handle/")
async def email_handle(file: UploadFile, db:Session = Depends(get_db)):
    try:
        raw_email = await file.read()
        user_email, subject, body = parse_email(raw_email)
        name , email = parseaddr(user_email)

        user_input = f"Email from: {email}\nSubject: {subject}\n\n{body}"
        response = user_email_response(user_input,email,db)
        return APIResponse(status = StatusEnum.SUCCESS, data = response)
    
    except Exception as e:
         return APIResponse(
            status=StatusEnum.FAIL,
            message="Failed to process email",
            data={"error": str(e)},
        )