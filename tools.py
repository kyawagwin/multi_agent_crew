import os
from crewai.tools import BaseTool
from pydantic import Field
from tavily import TavilyClient

class TavilySearchTool(BaseTool):
    name: str = "Tavily Search"
    description: str = "Search the web for recent news, articles, and financial information about a stock's ticker and company name."
    
    def _run(self, query: str) -> str:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY environment variable is not set."
            
        client = TavilyClient(api_key=api_key)
        try:
            response = client.search(query=query, search_depth="advanced", max_results=5)
            results = response.get("results", [])
            if not results:
                return "No useful search results found."
                
            output = ""
            for res in results:
                title = res.get('title', 'No Title')
                url = res.get('url', 'No URL')
                content = res.get('content', 'No Content')
                output += f"Title: {title}\nURL: {url}\nContent: {content}\n\n---\n\n"
            return output
        except Exception as e:
            return f"Error during search: {str(e)}"
