#from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
else:
    st.warning("LANGCHAIN_API_KEY is not set in the environment")  # Use st.warning instead of print for Streamlit

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's queries."),
        ("user", "Question: {question}")
    ]
)

# Streamlit framework
st.title('Langchain Demo with Gamma2 Model')
input_text = st.text_input("Search the topic you want")

# Ollama LLaMA2 LLM model loading
llm = Ollama(model="gemma2:2b")
output_parser = StrOutputParser()

# Create the chain (step-by-step instead of using the pipe operator for better readability)
# Create the chain (step-by-step instead of using the pipe operator for better readability)
def run_llm_chain(input_text):
    chain_input = {"question": input_text}
    prompt_output = prompt.format(**chain_input)  # Unpack the dictionary here
    llm_output = llm(prompt_output)  # Pass prompt to LLM
    parsed_output = output_parser.parse(llm_output)  # Parse the output
    return parsed_output


# Trigger the LLM and display the result if input is provided
if input_text:
    result = run_llm_chain(input_text)
    st.write(result)
