import os
from typing import TypedDict , Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph ,START , END
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.messages import AIMessage
from dotenv import load_dotenv


load_dotenv()

embeddings =  HuggingFaceEmbeddings(model_name = "BAAI/bge-small-en-v1.5",
                                    encode_kwargs={"normalize_embeddings": True},)

def build_retriver(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=250
    )

    chunks = splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 10,
            "fetch_k": 20,
            "lambda_mult": 0.7
        }
    )

    return retriever
academic_retriever = build_retriver("handbook.pdf")
fee_retriever = build_retriver("fee.pdf")

llm = ChatGroq(model = "llama-3.3-70b-versatile",temperature=0.5)

class State(TypedDict):
    programme:str
    messages:Annotated[list,add_messages]
    query_type:str
    retrieved_context:str


# nodes generation

def classifier_node(state:State)->dict:
    """
    look at the latest user message  and decide which path to take
    """
    last_message = state['messages'][-1].content

    prompt = f"""
You are a query classifier.

Classify the question into ONE category.

academic
- attendance
- syllabus
- semester
- subject
- credits
- examination
- grading
- internship
- regulations
- promotion
- handbook information

fee
- fees
- scholarship
- refund
- payment
- hostel fees

general
Everything else.

Examples

What is Tree in DSA? -> general
Explain Optical Fiber -> general
Who is APJ Abdul Kalam? -> general
Attendance policy -> academic
Semester 4 syllabus -> academic
Fee of BTech AI -> fee

Question:

{last_message}

Return only one word.
"""

    response = llm.invoke(prompt)
    category = response.content.strip().lower()

    if "academic" in category:
        category = "academic"
    elif "fee" in category:
        category = "fee"
    else:
        category = "general"
    
    return {"query_type":category}

def academic_rag_node(state: State) -> dict:

    original_query = state["messages"][-1].content

    rewrite_prompt = f"""
You are an AI assistant that rewrites student questions for semantic document retrieval.

Rewrite the question to make it more specific while preserving its meaning.

Question:
{original_query}

Return only the rewritten question.
"""

    rewritten_query = llm.invoke(rewrite_prompt).content.strip()

    docs = academic_retriever.invoke(rewritten_query)

    context = "\n\n".join(doc.page_content for doc in docs)

    return {
        "retrieved_context": context
    }

def fee_rag_node(state: State) -> dict:

    original_query = state["messages"][-1].content

    rewrite_prompt = f"""
Rewrite this question so it is easier to retrieve information from a fee document.

Question:
{original_query}

Return only the rewritten question.
"""

    rewritten_query = llm.invoke(rewrite_prompt).content.strip()

    docs = fee_retriever.invoke(rewritten_query)

    context = "\n\n".join(doc.page_content for doc in docs)

    return {
        "retrieved_context": context
    }

def general_node(state: State) -> dict:
    """Answers directly using the LLM's own knowledge, no retrieval needed."""
    return {"retrieved_context": "NO_RETRIEVAL_NEEDED"}



def response_node(state: State):

    query = state["messages"][-1].content
    context = state["retrieved_context"]

    if context == "NO_RETRIEVAL_NEEDED":

        prompt = f"""
You are a knowledgeable AI assistant.

Answer the question naturally.

Question:
{query}
"""

    elif context.strip() == "":

        prompt = f"""
You are a knowledgeable AI assistant.

The college documents do not contain the required information.

Answer using your general knowledge.

Question:
{query}
"""

    else:

        prompt = f"""
You are an AI Assistant for AKTU students.

Answer using the context below.

If the context contains the answer,
use it.

If the context is incomplete,
complete the answer using your own
general knowledge.

If the question specifically asks about
AKTU rules, syllabus, regulations,
credits or fee and the context does not
contain the answer, then say

"I couldn't find this information in the college documents."

Context

{context}

Question

{query}
"""

    response = llm.invoke(prompt)

    return {
        "messages": [
            AIMessage(content=response.content)
        ]
    }
#step 4 - router function 

def route_query(state:State):
    if state['query_type'] == 'academic':
        return "academic_rag"
    elif state['query_type'] == "fee":
        return "fee_rag"
    else:
        return "general"


#step 5 - Building the graph 

graph = StateGraph(State)

graph.add_node("classifier",classifier_node)
graph.add_node("academic_rag",academic_rag_node)
graph.add_node("fee_rag",fee_rag_node)
graph.add_node("general",general_node)
graph.add_node("response",response_node)

#edges 

graph.add_edge(START,"classifier")

graph.add_conditional_edges(
    "classifier",
    route_query,
    {
        "academic_rag": "academic_rag",
        "fee_rag": "fee_rag",
        "general": "general"
    }
)

graph.add_edge("academic_rag","response")
graph.add_edge("fee_rag","response")
graph.add_edge("general","response")

graph.add_edge("response",END)

app = graph.compile()
#step 6 - Run the code 
if __name__ == "__main__":

    print("welcome to the College assistant \n")

    print("1. BCA")
    print("2. BBA")
    print("3. B.Tech.")

    choice = input("Enter choice: ")

    programme_map = {
        "1": "BCA",
        "2": "BBA",
        "3": "B.Tech.(H)"
    }

    student_programme = programme_map.get(choice, "B.Tech.(H)")

    while True:

        query = input("You: ")

        if query.lower() == "exit":
            break

        result = app.invoke(
            {
                "programme": student_programme,
                "messages": [("human", query)]
            }
        )

        print(result["messages"][-1].content)