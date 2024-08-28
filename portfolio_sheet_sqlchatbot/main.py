import json
import sqlparse
import pandas as pd
import mysql.connector
import gradio as gr
from groq import Groq
import os
from dotenv import load_dotenv
import datetime
import uuid
import random

# Load environment variables
load_dotenv()

# Initialize API key and Groq client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set")
client = Groq(api_key=GROQ_API_KEY)

# Use the Llama3 70b model
MODEL = "llama3-70b-8192"

# Global variable to store context 
context = {
    "current_city": None,
    "current_topic": None,
    "clients": [],
    "last_query_info": {},
    "question_history": []
}

# List of cities
CITIES = ["Pune", "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Gurugram"]

# This function generates the SQL query and provides summarized response to the user
def chat_with_groq(prompt, response_format=None):
    try:
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format=response_format
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# This function executes the SQL query in MySQL database and then returns a dataframe
def execute_mysql_query(query):
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ansh1529",
            database="smartworks_database"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        result = cursor.fetchall()
        return pd.DataFrame(result)
    except mysql.connector.Error as e:
        return pd.DataFrame({'Error': [str(e)]})
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# The dataframe returned by SQL is now read by get_summarization function and provides response to the user
def get_summarization(user_question, df):
    global context
    prompt = f'''
    A user asked the following question about the SmartWorks database:

    {user_question}

    Here's the data retrieved to answer the question:

    {df.to_markdown(index=False)}

    Current context:
    - City: {context['current_city']}
    - Topic: {context['current_topic']}
    
    Recent question history:
    {"\n".join(f"- {q}" for q in context['question_history'])}

    Summarize this data for the user, keeping in mind:

    - Answer the user's question directly and concisely using ONLY the information provided in the data above.
    - Do not make up or infer any information that is not explicitly present in the data.
    - If the data does not contain information to answer the question, state that clearly.
    - Use the current context (city and topic) in your response if it's relevant to the user's question and supported by the data.
    - Consider the recent question history to maintain context across multiple questions.
    - If the current question seems to be a follow-up to a previous question, use the context appropriately.
    - Present relevant details in a list format if appropriate.
    - All monetary amounts are in Indian Rupees (INR).
    - Keep all the numbers accurate, and avoid scientific notation or rounding. Show exact values, especially for Peak values.
    - Avoid phrases like "based on the data" or "here is a summary." Simply provide the data.
    - Do not use italics or special fonts.
    - If the data is insufficient to answer the question completely, mention what information is missing.
    - Provide calculations if applicable, showing each step of the calculation (e.g., adding revenue from multiple clients and showing individual contributions).
    - Double-check the response before providing it to the user.
    - Respond in a clear, natural, and conversational manner.
    - If providing a list of clients, include the count of clients.
    '''
    return chat_with_groq(prompt)

# Load the base prompt from a file
def load_base_prompt():
    with open('portfolio_base_prompt.txt', 'r') as file:
        return file.read()

# Load the test prompt from a file
def load_test_prompt():
    with open('portfolio_test_prompt.txt', 'r') as file:
        return file.read()
    
# Update the context based on the user's question and query results
def update_context(user_question, sql_query, results_df):
    global context
     
    # Check for city in the current question
    new_city = next((city for city in CITIES if city.lower() in user_question.lower()), None)
    
    if new_city:
        context['current_city'] = new_city
    # Don't reset the city if it's not mentioned in the current question
    
    # Update topic based on the current question
    if "revenue" in user_question.lower():
        context['current_topic'] = "revenue"
    elif "client" in user_question.lower():
        context['current_topic'] = "clients"
    # Don't reset the topic if it's not mentioned in the current question
    
    # Update clients list if available in the results
    if 'Client Name' in results_df.columns:
        context['clients'] = results_df['Client Name'].unique().tolist()
    
    # Store the last query information
    context['last_query_info'] = {
        'sql_query': sql_query,
        'results': results_df
    }
    
    # Add the current question to the history list
    context['question_history'].append(user_question)
    
    # Limit the history to the last 5 questions
    context['question_history'] = context['question_history'][-5:]

# Save the chat history to a file
def save_history(user_id, user_name, user_input, sql_query, df, bot_response):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"user_data_{user_id}.txt"
    
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"User ID: {user_id}\n")
        f.write(f"User Name: {user_name}\n")
        f.write(f"User Question: {user_input}\n")
        f.write(f"SQL Query: {sql_query}\n")
        f.write("Results DataFrame:\n")
        f.write(df.to_string(index=False))
        f.write("\n")
        f.write(f"Bot Response: {bot_response}\n")
        f.write("-" * 80 + "\n\n")

# Handle the user's query
def handle_query(user_question, history, show_sql, user_id, user_name):
    global context
    
    base_prompt = load_base_prompt()
    test_prompt = load_test_prompt()

    previous_context = ""
    if history:
        for item in history:
            q, a = item
            previous_context += f"User: {q}\nAI: {a}\n"
    
    context_info = f"""
    Current context:
    - City: {context['current_city']}
    - Topic: {context['current_topic']}
    - Recent questions: {', '.join(context['question_history'])}
    """
    full_prompt = f"{base_prompt}\n\nExample Questions and Queries:\n{test_prompt}\n\nUser Question: {user_question}\n\nPrevious Context:\n{previous_context}\n\nCurrent Context:\n{context_info}\n\nGenerate a response in JSON format with 'sql' and 'response' keys. If no SQL query is needed, leave the 'sql' key empty."
    
    llm_response = chat_with_groq(full_prompt, {"type": "json_object"})
    
    try:
        result_json = json.loads(llm_response)
        if 'sql' in result_json and result_json['sql']:
            sql_query = result_json['sql']
            results_df = execute_mysql_query(sql_query)
            
            update_context(user_question, sql_query, results_df)
            
            formatted_sql_query = sqlparse.format(sql_query, reindent=True, keyword_case='upper')
            summarization = get_summarization(user_question, results_df)
            
            response = f"SQL Query:\n```sql\n{formatted_sql_query}\n```\n\n{summarization}" if show_sql else summarization
        else:
            sql_query = ""
            results_df = pd.DataFrame()
            response = result_json.get('response', "I couldn't generate a relevant SQL query for this question. Can you please rephrase or ask something related to the SmartWorks database?")
                
        new_history = history + [(user_question, response)]
        save_history(user_name, user_id, user_question, sql_query, results_df, response)
        return new_history, ""

    except json.JSONDecodeError:
        response = "I encountered an error while processing your request. Could you please rephrase your question or try again?"
        new_history = history + [(user_question, response)]
        save_history(user_id, user_name, user_question, "", pd.DataFrame(), response)
        return new_history, ""

# Create the Gradio interface
def gradio_interface():
    with gr.Blocks(css="""
        #container { max-width: 1200px; margin: auto; }
        #sidebar { padding-right: 20px; }
        #main-content { padding-left: 20px; }
        .gr-form { gap: 5px; }
        .gr-box { margin-bottom: 10px; }
    """) as demo:
        user_id = gr.State(lambda: str(uuid.uuid4()))
        
        with gr.Row(elem_id="container"):
            # Left sidebar
            with gr.Column(scale=1, elem_id="sidebar"):
                gr.Markdown(" ")
                gr.Markdown("# SmartWorks ")
                gr.Markdown("Portfolio sheet Assistant")
                user_name = gr.Textbox(label="Enter your name", placeholder="Your Name")
                
                gr.Markdown(" #### A new way to interact with your database! The SmartWorks Database Assistant lets you query and explore data effortlessly using natural language.")
                gr.Image("Dancing Chatbot.gif",height=340)
                download = gr.Button("Download Chat History")
                
            # Main chatbot interface
            with gr.Column(scale=2, elem_id="main-content"):
                chatbot = gr.Chatbot(height=500,min_width=500)
                msg = gr.Textbox(placeholder="ask me anything...")
                show_sql = gr.Checkbox(label="Show SQL Query", value=False)

                with gr.Row():
                    clear = gr.Button("Clear")
                    regenerate = gr.Button("Regenerate")
        
        # Generate welcome message
        def welcome_message(name):
            if name:
                return [(None, f"Hello {name}! I'm your SmartWorks Database Assistant. How can I help you today?")]
            return []

        # Regenerate the last response
        def regenerate_response(user_id, user_name, history, show_sql):
            if history:
                last_user_message = history[-1][0]
                new_history = history[:-1]  # Remove the last interaction
                return handle_query(last_user_message, new_history, show_sql, user_id, user_name)[0]
            return history
        
        # Download chat history
        def download_history(user_id, user_name):
            filename = f"user_data_{user_id}.txt"
            if os.path.exists(filename):
                return filename
            return None

        # Set up event handlers
        user_name.submit(welcome_message, user_name, chatbot)
        msg.submit(handle_query, [msg, chatbot, show_sql, user_id, user_name], [chatbot, msg])
        clear.click(lambda: None, None, chatbot, queue=False)
        regenerate.click(regenerate_response, inputs=[user_id, user_name, chatbot, show_sql], outputs=[chatbot])
        download.click(download_history, inputs=[user_id, user_name], outputs=[gr.File()])
    
    return demo

# Create the Gradio interface
demo = gradio_interface()

# Launch the Gradio interface
if __name__ == "__main__":
    demo.launch(share=True)
    #demo.launch(server_name="0.0.0.0")