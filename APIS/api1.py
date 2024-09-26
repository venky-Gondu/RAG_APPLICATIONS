from fastapi import FastAPI
from fastapi.responses import JSONResponse

from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama  # Import the correct class from the module
from langserve import add_routes
import uvicorn
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
else:
    print("Error loading the Langchain API Key")

# Initialize FastAPI app
api1 = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API Server"
)

# Correctly instantiate the Ollama model
llm = Ollama(model="gemma2:2b")  # Ensure model string is correct

# Create the prompt template
prompt2 = ChatPromptTemplate.from_template("{topic}")

# Add routes to the FastAPI app
add_routes(
    api1,
    prompt2 | llm,  # Ensure the prompt and llm are correctly piped
)

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(api1, host="localhost", port=8000)
