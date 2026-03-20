from crewai import Task
from models import StockAnalysis

def get_tasks(researcher, analyst):
    research_task = Task(
        description='Conduct comprehensive web research on {company} ({ticker}). Search for recent news, earnings context, product launches, and general market sentiment. Make sure you gather enough context to allow an analyst to make a complete recommendation. ONLY use tools if you need to fetch information remotely.',
        expected_output='A detailed research report summarizing the recent news, key events, challenges, and general sentiment for {company}.',
        agent=researcher
    )

    analysis_task = Task(
        description='Analyze the research report provided to you for {company} ({ticker}). Evaluate the sentiment, pinpoint key events, formulate a reasoning, and decide on a final trading recommendation (Buy, Sell, or Hold).',
        expected_output='A structured JSON analysis containing the sentiment score, key events, trading recommendation, and a summary. Ensure the output perfectly matches the requested Pydantic schema.',
        agent=analyst,
        output_pydantic=StockAnalysis
    )
    
    return [research_task, analysis_task]
