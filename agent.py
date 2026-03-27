import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from tools import get_me, login_agent, login_frontend, read_local_instructions

load_dotenv(override=True)

TOOLS = [
    read_local_instructions,
    login_agent,
    get_me,
    login_frontend,
]

#SYSTEM_PROMPT = """
#You are an AI agent that logs into a system.

#Steps:
#1. Read instructions file
#2. Login using login_agent
#3. Verify user using get_me

#IMPORTANT RULES:
#- ALWAYS read instructions first
#- ALWAYS login first
#- After get_me returns successful user data → STOP immediately
#- DO NOT repeat actions
#- DO NOT call tools again after success
#- DO NOT loop

#When login and verification are successful:
#Return FINAL ANSWER with user details and STOP.
#"""

def build_agent():
    print("Using Groq model: llama-3.1-8b-instant")

    llm = ChatGroq(                      #initialize llm
        model="llama-3.1-8b-instant",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    agent = create_agent(
        model=llm,                           #agent is creted 
        tools=TOOLS,
#        system_prompt=SYSTEM_PROMPT,
    )

    print("Agent ready!")
    return agent
