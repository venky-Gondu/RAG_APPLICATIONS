import streamlit as st
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.tools import Tool

# Define the custom prompt
custom_prompt = hub.pull("hwchase17/react").partial(
    sistema=  """
You are a highly intelligent assistant. Your task is to analyze the user's query and respond based on the available tools.
You have access to the following tools:
{tool_names}
Question: {input}

If the user asks for general information, use the Wikipedia tool.
If the user asks for research papers, use the Arxiv tool.
If the user asks about internal documents, use the Document Retriever.

Provide a step-by-step response with detailed explanations where necessary.
Guidelence :
1. Be concise and goal oriented while responding to the user query.
2. Use the available tools in efficient manner to provide accurate information.
3. Limit the word count for Wikipedia search and document search to 1000 words.
4. Summarize the content in precise and accurate manner.
{agent_scratchpad}
"""
)

# Initialize the LLM
llm = Ollama(model="gemma2:2b")

# Load tools
tools = load_tools(["wikipedia", "arxiv"])

# Load internal documents
loader = PyPDFLoader("Attention all you need.pdf")  # Modify path as needed
documents = loader.load()

# Create embeddings and vector store
embeddings = OllamaEmbeddings(model="gemma2:2b")
vectorstore = FAISS.from_documents(documents, embeddings)

# Create a Document Retrieval QA chain
doc_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(),
)

# Wrap the Document Retriever as a tool
document_tool = Tool.from_function(
    func=doc_chain.run,
    name="Document_Retriever",
    description="Use this tool to answer questions based on internal documents."
)

# Append the document tool to the tools list
tools.append(document_tool)

# Create the agent
agent = create_react_agent(llm, tools, custom_prompt)

# Create the AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, max_iterations=4,
                                 early_stopping_method="force", verbose=True)

# Set up the Streamlit interface
st.title("🔍 Multi-Source Search Application")
st.write("This application allows you to perform searches across multiple sources: Wikipedia, Arxiv, and internal documents.")

# Input box for the user's query
user_query = st.text_input("Enter your query here:", "")

# Button to execute the query
if st.button("Search"):
    if user_query.strip() == "":
        st.warning("Please enter a query before searching.")
    else:
        st.write("🔍 Processing your query...")
        
        # Execute the query using the agent executor
        response = agent_executor.invoke({"input": user_query})

        # Display the response in the Streamlit interface
        if response:
            # Extract and display the output and the tool used
            output = response.get("output", "")
            tool_used = response.get("tool_name", "Unknown Tool")  # Adjust this to track the invoked tool
            
            # Check if the tool was used
            if 'tool_name' in response:
                tool_used = response['tool_name']  # Adjust this line if your agent response includes tool name

            st.write("### Search Result:")
            st.write(output)
            st.write(f"**Source Tool:** {tool_used}")  # Display the tool name used for the response
        else:
            st.warning("No response received from the tools.")
