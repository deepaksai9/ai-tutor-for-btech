store = ProgressStore(st.session_state["user_id"])

# Use Groq
from langchain_groq import ChatGroq
llm = ChatGroq(
    temperature=0.7, 
    model_name="llama3-70b-8192", 
    api_key=os.getenv("GROQ_API_KEY")
)
