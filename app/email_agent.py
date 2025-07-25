from langchain.agents import create_tool_calling_agent, AgentExecutor
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from langchain_community.llms.ollama import Ollama
from langchain.agents.types import AgentType
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from sqlalchemy.orm import Session
#from app.tools.user_tools import user_report_complaint, user_question, classify_question
from functools import partial
from langchain_core.tools import Tool,StructuredTool
from app.tools.tool_test import EmailTools
from app.db.schemas.tools import ToolInputs, QuestionInput, ClassifyInput
from app.core.config import OPENAI_API_KEY

def email_agent( query: str,user_em, db:Session):
    tools_obj = EmailTools(db)
    
    llm_used =ChatOpenAI(model="gpt-4", openai_api_key= OPENAI_API_KEY)


    wrapped_tools = [
        StructuredTool.from_function(
            func=tools_obj.user_report_complaint,
            name="user_report_complaint",
            description="Report a user complaint.",
            args_schema=ToolInputs
        ),
        StructuredTool.from_function(
            func=tools_obj.user_question,
            name="user_question",
            description="Answer a user's question via RAG and email.",
            args_schema=QuestionInput
        ),
        StructuredTool.from_function(
            func=tools_obj.classify_question,
            name="classify_question",
            description="Classify a user question into auto_answer or needs_human.",
            args_schema=ClassifyInput
        )
    ]

     #can make it so that the agent takes in different tasks as tools for different purposes
    agent_prompt = """You are an AI customer support agent with access to tools.
Use the tools to answer user questions, report complaints, or classify inquiries.
Be polite, concise, and helpful by sending an email to the user. """

    prompt = ChatPromptTemplate.from_messages([("system",agent_prompt),("user",f"Email from: {user_em}\n\n{query}"), MessagesPlaceholder(variable_name="agent_scratchpad"),])
    
    try:
        try:
            agent = create_tool_calling_agent(
            llm_used,
            wrapped_tools,
            prompt
        )

    
        except Exception as e:
            import traceback
            traceback.print_exc()    # This prints the full traceback to stderr
            return f"Error {e} occurred"

        agent_executor = AgentExecutor(agent=agent, tools=wrapped_tools, verbose=True)

        response = agent_executor.invoke({
            "query": f'Email from{user_em}\n\n query :{query} ' ,
            "user_email": user_em,
            "agent_scratchpad": []  # This field is crucial for tool-calling agents!
        })

        return response["output"]

        
    
    except Exception as e:
        import traceback
        traceback.print_exc()    # This prints the full traceback to stderr
        return f"Error {e} occurred"