import os
import argparse
import json
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
from crewai import Crew, Process
from agents import get_agents
from tasks import get_tasks

# Load environment variables from .env
load_dotenv()

def send_to_webhook(data: dict):
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        print("WEBHOOK_URL not configured, skipping webhook push.")
        return
    
    try:
        response = requests.post(
            webhook_url,
            json=data,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        print("Successfully sent data to webhook.")
    except Exception as e:
        print(f"Failed to send webhook: {e}")

def save_to_mongodb(data: dict):
    mongodb_uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DB_NAME", "trading_db")
    collection_name = os.getenv("MONGODB_COLLECTION", "stock_analysis")
    
    if not mongodb_uri:
        print("MONGODB_URI not configured, skipping database insertion.")
        return
        
    try:
        client = MongoClient(mongodb_uri)
        db = client[db_name]
        collection = db[collection_name]
        
        result = collection.insert_one(data)
        print(f"Successfully saved to MongoDB. ID: {result.inserted_id}")
    except Exception as e:
        print(f"Failed to save to MongoDB: {e}")

def main():
    parser = argparse.ArgumentParser(description="Run the Multi-Agent Trading Analysis Crew")
    parser.add_argument("--ticker", type=str, required=True, help="The stock ticker symbol (e.g., AAPL, TSLA)")
    parser.add_argument("--company", type=str, help="The company name (e.g., 'Apple Inc.'). Defaults to ticker if not provided.")
    args = parser.parse_args()

    ticker = args.ticker
    company = args.company if args.company else ticker

    print(f"Starting Multi-Agent Stock Analysis for {company} ({ticker})...")

    # 1. Initialize Agents
    researcher, analyst = get_agents()

    # 2. Initialize Tasks
    tasks = get_tasks(researcher, analyst)

    # 3. Form the Crew
    crew = Crew(
        agents=[researcher, analyst],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    # 4. Kickoff the Crew
    print("Kicking off the tasks...")
    inputs = {
        'company': company,
        'ticker': ticker
    }
    
    try:
        result = crew.kickoff(inputs=inputs)
        
        # 5. Extract Pydantic Output or raw JSON
        if hasattr(result, 'pydantic') and result.pydantic:
            output_dict = result.pydantic.model_dump()
        else:
            try:
                output_dict = json.loads(result.raw)
            except json.JSONDecodeError:
                print("Could not parse raw output as JSON. Saving raw string.")
                output_dict = {"raw_output": result.raw}
            
        print("\n--- Final Analysis Result ---")
        print(json.dumps(output_dict, indent=2))
        
        # 6. Save to DB and Send Webhook
        save_to_mongodb(output_dict)
        send_to_webhook(output_dict)
        
    except Exception as e:
        print(f"An error occurred during workflow execution: {e}")

if __name__ == "__main__":
    main()
