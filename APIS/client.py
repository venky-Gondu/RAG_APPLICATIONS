import requests
import streamlit as st

# Function to send a request to the FastAPI server
def get_ollama_response(input_text):
    # Make a POST request to the FastAPI server's endpoint
    response = requests.post(
        "http://localhost:8000/invoke",  # Ensure this matches the FastAPI endpoint
        json={'input': {'topic': input_text}}  # Pass 'topic' in the expected format
    )

    # Check if the response is successful and return the output
    if response.status_code == 200:
        return response.json().get('output', 'No output found')  # Handle response safely
    else:
        return f"Error: {response.status_code}, {response.text}"

# Streamlit app interface
st.title('Langchain Demo with OpenLLM API')

# Text input for the user to enter a topic
input_text1 = st.text_input("Enter a topic")

# Button to trigger the API call
if st.button('Get Response'):
    # If input is provided, call the API and display the result
    if input_text1:
        result = get_ollama_response(input_text1)
        st.write(result)
    else:
        st.write("Please enter a topic to continue.")
