from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Path to Chroma database
CHROMA_PATH = "chroma"

# Initialize Ollama model
model = OllamaLLM(model="llama3.2:3b")  # Ensure the correct model name

PROMPT_TEMPLATE = """
context:
{context}

You are an AI named Clap AI.You are an AI chatbot for children's learning in our LMS. Respond as a teacher.
Use the provided context to answer. If the answer does not exist in the context, respond with "The question asked does not refer to the subject."

question:
{question}
"""


def query_rag(query_text: str):
    """Handles querying ChromaDB and generating responses."""
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Perform similarity search
    results = db.similarity_search_with_score(query_text, k=5)
    if not results:
        return {"response": "❌ No relevant documents found in Chroma DB!", "sources": []}

    # Format context for the prompt
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    print("🔹 Generated Prompt:", prompt)  # Debugging

    # Stream response
    response_stream = model.stream(prompt)
    sources = [doc.metadata.get("id", "Unknown") for doc, _ in results]

    return response_stream, sources

@app.route("/ask", methods=["POST"])
def ask_question():
    """Handles incoming POST requests for chatbot queries."""
    data = request.json
    user_query = data.get("question", "").strip()

    if not user_query:
        return jsonify({"error": "No question provided!"}), 400

    def generate():
        """Streams the response to the client."""
        response_stream, sources = query_rag(user_query)

        for chunk in response_stream:
            yield chunk

    return Response(generate(), content_type="text/plain;charset=utf-8")

if __name__ == "__main__":
    print("🚀 Starting Flask server on http://127.0.0.1:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=True)
