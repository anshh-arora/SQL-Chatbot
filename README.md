# SQL-Chatbot

SQL-Chatbot introduces a revolutionary approach to interacting with databases by utilizing **Natural Language Processing (NLP)** to translate user queries into SQL commands. With this project, users no longer need to write SQL commands manually; instead, they can communicate with the database in plain English. This not only streamlines the database querying process but also opens up the world of data management to users with limited or no programming knowledge. SQL-Chatbot uses cutting-edge **LLaMA models** to comprehend and generate accurate SQL queries based on natural language input.

![SQL-Chatbot Demo](Dancing%20Chatbot.gif)

## Why SQL-Chatbot?

SQL-Chatbot transforms the way users interact with databases by:

- **Simplifying database queries**: Users can bypass learning SQL syntax and instead ask questions or request data in English.
- **Improving accessibility**: Users of all technical levels, from beginners to advanced professionals, can benefit from SQL-Chatbot without needing to master complex SQL commands.
- **Efficient database operations**: SQL-Chatbot handles the entire process, from understanding user queries to executing the corresponding SQL commands, making database interaction smoother and faster.

## How It Works

The SQL-Chatbot leverages **Large Language Models (LLMs)** to convert user input into valid SQL queries. The project is powered by the **LLaMA model**, which takes the user's natural language query and, using the instructions provided in `base_prompt.txt`, translates it into a corresponding SQL query. Once generated, the SQL query interacts with the database, retrieves the requested data, and presents it back to the user in an understandable format.

## Project Structure

- `.env`: Contains sensitive environment variables such as API keys.
- `main.py`: Core script containing the Gradio application for user interaction.
- `base_prompt.txt`: Provides foundational context to the LLaMA model.
- `store_data.csv`: Primary dataset for the SQL-Chatbot's queries.
- `data_to_sql.py`: Script for transferring data from CSV to SQL database.
- `modify_data.py`: Applies data transformations before storage.
- `previous_interactions.txt`: Logs user interactions for context maintenance.
- `requirements.txt`: List of Python dependencies.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd SQL-Chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in a `.env` file.

4. Run the Gradio application:
   ```bash
   python main.py
   ```

## Database Integration

SQL-Chatbot uses SQLAlchemy for database interaction. The `data_to_sql.py` script automates loading `store_data.csv` into a MySQL or PostgreSQL database.

## How to Use SQL-Chatbot

1. Enter a natural language query in the Gradio interface.
2. The LLaMA model converts the query to SQL.
3. The SQL query is executed on the database.
4. Results are displayed in a human-readable format.

## Future Enhancements

- Multi-database support
- Improved NLP capabilities
- Query optimization

## How to Contribute

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a clear explanation of your changes.

## License

[Insert your chosen license here]

## Contact

[Your contact information or project maintainer's contact]
