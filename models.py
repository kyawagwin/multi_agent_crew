from pydantic import BaseModel, Field
from typing import List, Optional

class SentimentScore(BaseModel):
    score: int = Field(description="The sentiment score of the stock between 1 to 10 (1 = extremely bearish, 10 = extremely bullish)")
    reasoning: str = Field(description="The reasoning behind the sentiment score based on collected news and analysis")

class StockAnalysis(BaseModel):
    stock_ticker: str = Field(description="The ticker symbol of the stock analyzed")
    company_name: str = Field(description="The full name of the company")
    current_price: Optional[float] = Field(description="The current stock price (if available during the run)", default=None)
    sentiment: SentimentScore = Field(description="Extracted sentiment analysis from news and social data")
    key_events: List[str] = Field(description="A concise list of recent key events and news highlights")
    recommendation: str = Field(description="The final trading recommendation: 'Buy', 'Sell', or 'Hold'")
    analysis_summary: str = Field(description="A brief paragraph summarizing the reasoning behind the recommendation and analysis")
