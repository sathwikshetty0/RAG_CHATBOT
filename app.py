# from flask import Flask, request, jsonify, Response
# from flask_cors import CORS
# from langchain_chroma import Chroma
# from langchain.prompts import ChatPromptTemplate
# from langchain_ollama import OllamaLLM
# from get_embedding_function import get_embedding_function

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# # Path to Chroma database
# CHROMA_PATH = "chroma"

# # Initialize Ollama model
# model = OllamaLLM(model="llama3.2:3b")  # Ensure the correct model name
# # Define prompt template
# # PROMPT_TEMPLATE = """
# # context:
# # {context}

# # You are an AI named Clap AI.
# # You are an AI chatbot for children's learning in our LMS. Respond as a teacher.
# # Use the provided context to answer. If the answer does not exist in the context, respond with "The question asked does not refer to the subject."

# # question:
# # {question}
# # """

# PROMPT_TEMPLATE = """
# context:
# {context}

# You are an expert from Dexes Company, providing guidance on how and what to teach teachers. Use the provided context to give clear and informative instructions.
# If thw question is greating then introduce yourself for questions like hii, hello.
# If the question does not match the context, respond with "The question asked is out of subject."

# question:
# {question}
# """

# def query_rag(query_text: str):
#     """Handles querying ChromaDB and generating responses."""
#     embedding_function = get_embedding_function()
#     db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

#     # Perform similarity search
#     results = db.similarity_search_with_score(query_text, k=5)
#     if not results:
#         return {"response": "❌ No relevant documents found in Chroma DB!", "sources": []}

#     # Format context for the prompt
#     context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])
#     prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
#     prompt = prompt_template.format(context=context_text, question=query_text)

#     print("🔹 Generated Prompt:", prompt)  # Debugging

#     # Stream response
#     response_stream = model.stream(prompt)
#     sources = [doc.metadata.get("id", "Unknown") for doc, _ in results]

#     return response_stream, sources

# @app.route("/ask", methods=["POST"])
# def ask_question():
#     """Handles incoming POST requests for chatbot queries."""
#     data = request.json
#     user_query = data.get("question", "").strip()

#     if not user_query:
#         return jsonify({"error": "No question provided!"}), 400

#     def generate():
#         """Streams the response to the client."""
#         response_stream, sources = query_rag(user_query)

#         for chunk in response_stream:
#             yield chunk

#     return Response(generate(), content_type="text/plain;charset=utf-8")

# if __name__ == "__main__":
#     print("🚀 Starting Flask server on http://127.0.0.1:5000 ...")
#     app.run(host="0.0.0.0", port=5000, debug=True)



from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from get_embedding_function import get_embedding_function
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL')

# Path to Chroma database
CHROMA_PATH = "chroma"

# Initialize Ollama model
model = OllamaLLM(model="llama3.2:3b")

PROMPT_TEMPLATE = """
context:
{context}

You are an expert from Dexes Company, providing guidance on how and what to teach teachers. Use the provided context to give clear and informative instructions. And you need to be Specific. 
If the question is greating then introduce yourself for questions like hii, hello and not more dont tell the names.
If the question does not match the context, respond with:
"The question asked is out of subject. You can click 'Contact Support' to get help from a human."


question:
{question}
"""

def send_support_email(subject, message, from_email):
    """
    Sends support email using configured SMTP server
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = SUPPORT_EMAIL
        msg['Subject'] = f"Support Request: {subject}"

        # Create email body
        body = f"""
        New support request from teacher:
        
        From: {from_email}
        Subject: {subject}
        
        Message:
        {message}
        """
        
        msg.attach(MIMEText(body, 'plain'))

        # Create SMTP connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

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

@app.route("/send_support_email", methods=["POST"])
def handle_support_email():
    """Handles support email requests from the chatbot."""
    data = request.json
    
    required_fields = ['email', 'subject', 'message']
    if not all(field in data for field in required_fields):
        return jsonify({
            "error": "Missing required fields. Please provide email, subject, and message."
        }), 400

    # Validate email format (basic check)
    if '@' not in data['email'] or '.' not in data['email']:
        return jsonify({
            "error": "Invalid email format."
        }), 400

    # Send support email
    success = send_support_email(
        subject=data['subject'],
        message=data['message'],
        from_email=data['email']
    )

    if success:
        return jsonify({
            "message": "Support request sent successfully!"
        })
    else:
        return jsonify({
            "error": "Failed to send support request. Please try again later."
        }), 500

if __name__ == "__main__":
    # Verify email configuration
    if not all([SMTP_USERNAME, SMTP_PASSWORD, SUPPORT_EMAIL]):
        print("⚠️ Warning: Email configuration is incomplete. Support email feature will not work.")
        print("Please set SMTP_USERNAME, SMTP_PASSWORD, and SUPPORT_EMAIL in your .env file")
    
    print("🚀 Starting Flask server on http://127.0.0.1:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=True)
