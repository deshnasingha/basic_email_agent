from langchain_core.tools import tool,InjectedToolArg
from sqlalchemy.orm import Session
from app.db.models.Complaints import Complaint
from app.db.models.User import User
from app.db.schemas.responses import APIResponse, StatusEnum # Assuming you have a custom response class
from datetime import datetime
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
# from langchain.chains import LLMChain
from langchain_core.output_parsers import StrOutputParser
from app.rag.rag_chain import rag_chain
from app.email_send import send
from langchain_community.llms.ollama import Ollama
import re
from app.core.config import OPENAI_API_KEY


# llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
llm_used = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY)

# Prepare a prompt template for classification
prompt_template = PromptTemplate(
    input_variables=["question"],
    template=(
        "You are a customer support classifier. "
        "Classify the following user question as either 'auto_answer' if it can be "
        "answered automatically, or 'needs_human' if it requires a human to respond.\n\n"
        "Question: {question}\n\n"
        "Answer with exactly one of these two options: auto_answer or needs_human."
    )
)

# Create the LLM chain for classification
llm_chain = prompt_template|llm_used | StrOutputParser()

def extract_email(text: str) -> str | None:
    # Regex for basic email extraction
    match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    if match:
        return match.group(0)
    return None

class EmailTools:
    def __init__(self, db: Session):
        self.db = db

    def user_report_complaint(self,complaint: str,user_email: str ):
        """This function takes the complaint text and records the users complaint in the database."""
    
        # adds the complaint to the complaint db
        #db = kwargs["db"]
        user = self.db.query(User).filter(User.email == user_email).first()
        if not user:
            return APIResponse(
            status= StatusEnum.FAIL,
            message="User not found"
        )
        user_id = user.id
        new_complaint = Complaint(
        id = 3,
        user_id=user_id,
        content=complaint,
        status='open',
        )
    
        self.db.add(new_complaint)
        self.db.commit()
        self.db.refresh(new_complaint)
        return APIResponse(
        status= StatusEnum.SUCCESS,
        message="Complaint reported successfully",
        data={
            "complaint_id": new_complaint.id,
            "user_id": user_id,
            "status": new_complaint.status
            }
        )
    
    def classify_question(question: str, user_email:str) -> str:
        """This function classifies the question provided by the user 
        into a auto answerable or human answeable question. Seeing if the user is asking about refund or not."""
        classification = llm_chain.invoke({"question":question}).strip().lower()
        if not classification:
            return "needs_human"
        if classification not in ("auto_answer", "needs_human"):
            classification = "needs_human"
        return classification
    

    def user_question(self,question: str,user_email:str, ):
        """This function can be used to handle user questions
        For now, it send a email response to the user with the answer based on the company data."""
        # db = kwargs["db"]
        #user_email = extract_email(question)
        user = self.db.query(User).filter(User.email == user_email).first()
        if not user:
            return APIResponse(
            status= StatusEnum.FAIL,
            message="User not found"
        )
        user_id = user.id
        answer = rag_chain(question, file_path= "C:/WorkSpace/n3one/base_agent/documents/text_doc.txt")
        
        prompt_content = PromptTemplate(
        input_variables=["question",  "answer","user_id"],
        template=(
        "You are a customer support assistamt. "
        "Write a polite email to the customer with customer id : {user_id}, answering their question given below."
        "\n\n"
        "Question: {question}\n\n"
        "Answer : {answer}"
            )
    )
        prompt_subject = PromptTemplate(
        input_variables=["question"],
        template=(
        "You are a customer support assistamt. "
        "Write a subject for an email, that answers user's question."
        "\n\n"
        "Question: {question}\n\n"
        )
    )
        try:
            llm_chain_ =prompt_subject | llm_used| StrOutputParser()
            llm_chain = prompt_content|llm_used|StrOutputParser()
            subject = llm_chain_.invoke({"question": question})
            content = llm_chain.invoke({"question": question, "answer": answer, "user_id": user_id})
            #response = send(user.email, subject,content)
            #if response.status_code != 200:
                #return response
    
            return APIResponse(
                status= StatusEnum.SUCCESS,
                message="Your question has been received",
                data={
                "question": question,
                "user_id": user_id,
                "answer": content
                }
        )   
    
        except Exception as e:
            return APIResponse(status = StatusEnum.FAIL,
                           message = f"error showed up in tools {e}")
    



