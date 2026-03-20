from pydantic import BaseModel, Field
from typing import List, Optional

class NewsArticle(BaseModel):
    headline: str = Field(..., description="The headline of the news article")
    date: str = Field(..., description="The date the article was published")
    summary: str = Field(..., description="A short summary of the article's contents")
    sentiment_score: float = Field(..., description="A sentiment score from -1.0 (very negative) to 1.0 (very positive)")
    market_catalyst: bool = Field(..., description="True if the news acts as a potential market catalyst, otherwise False")

class NewsAnalysisOutput(BaseModel):
    articles: List[NewsArticle] = Field(..., description="A list of analyzed news articles")

class QuantAnalysisOutput(BaseModel):
    ticker: str = Field(..., description="The stock ticker symbol being evaluated")
    action: str = Field(..., description="The recommended action: 'buy', 'sell', or 'hold'")
    confidence: float = Field(..., description="Confidence score of the recommendation from 0.0 to 1.0")
    strength: str = Field(..., description="The strength of the signal: 'weak', 'moderate', 'strong'")
    stop_loss: float = Field(..., description="The calculated stop loss price ensuring a 1:3 risk/reward ratio")
    take_profit: float = Field(..., description="The calculated take profit price ensuring a 1:3 risk/reward ratio")
