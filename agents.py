import os
from crewai import Agent
from tools import TavilySearchTool
from langchain_openai import ChatOpenAI

def get_agents():
    # Use gpt-4o as it provides great reasoning and structure
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    researcher = Agent(
        role='Financial Researcher',
        goal='Gather recent news, earnings context, and general market sentiment for {company} ({ticker}).',
        backstory='You are an expert financial researcher responsible for fetching the most up-to-date and accurate news about assigned companies.',
        tools=[TavilySearchTool()],
        llm=llm,
        verbose=True
    )

    analyst = Agent(
        role='Financial Analyst',
        goal='Analyze the collected research and synthesize a robust trading recommendation for {company} ({ticker}).',
        backstory='You are a seasoned Wall Street analyst known for your deep insights, logical reasoning, and accurate trading recommendations.',
        llm=llm,
        verbose=True
    )
    
    return researcher, analyst
