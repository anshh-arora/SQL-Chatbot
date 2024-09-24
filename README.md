# SQL-Chatbot

## Overview
The **SQL-Chatbot** is an innovative way to interact with your database using natural language instead of traditional SQL queries. This chatbot leverages advanced language models (LLMs) to translate your natural language queries into SQL commands, allowing seamless communication with databases without requiring any programming knowledge. It's an efficient and user-friendly approach to database interaction for users of all technical backgrounds.

---

## Project Structure

### **Files and Directories**

- **`main.py`**: This file contains the Gradio application, which serves as the user interface for interacting with the SQL-Chatbot. It manages the interaction between the user, the LLM, and the SQL database.

- **`base_prompt.txt`**: This text file provides the context and guidance for the LLaMA model, helping it understand how to convert natural language inputs into accurate SQL queries.

- **`requirements.txt`**: A list of all required Python libraries and dependencies that need to be installed to run this project.

- **`store.csv`**: The original dataset used in this project. It serves as the raw data, which is later processed and transformed.

- **`modify_data.py`**: A Python script responsible for transforming the `store.csv` dataset into a structured and cleaned format, resulting in the `store_data.csv` file.

- **`store_data.csv`**: This file contains the final, processed dataset after transformation, which is used for querying and interaction with the SQL-Chatbot.

- **Database Integration**: The project uses SQLAlchemy to quickly and efficiently import data into a MySQL database.

---

## How LLM is Used in the Project
The SQL-Chatbot utilizes **Large Language Models (LLMs)** to convert user-inputted natural language queries into SQL commands. The LLaMA model is specifically used to understand the context and structure provided in `base_prompt.txt`. When a user enters a query in English, the LLM translates it into a corresponding SQL command that interacts with the database, retrieves the necessary information, and returns results in a user-friendly format.

---

## Explore the Project on Hugging Face
You can explore this project and try out the SQL-Chatbot on Hugging Face: [Hugging Face Project Link](#)

---

## How to Clone the Repository

To get started with this project, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>



Navigate to the project directory:

cd SQL-Chatbot
Install the required packages:

pip install -r requirements.txt
Run the Gradio application:

python main.py