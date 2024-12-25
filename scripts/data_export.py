import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from dotenv import load_dotenv
import os



# Load environment variables
load_dotenv()



# Define the export function for PostgreSQL
from sqlalchemy import text

def export_to_postgresql(scores):
    # Retrieve database configuration from environment variables
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    # Create a database connection string
    connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    engine = create_engine(connection_string)

    # Create table if it doesn't exist
    with engine.connect() as connection:
        try:
            connection.execute(text("""
            CREATE TABLE IF NOT EXISTS user_scores (
                MSISDN VARCHAR(20),
                Engagement_Score FLOAT,
                Experience_Score FLOAT,
                Satisfaction_Score FLOAT,
                Cluster INT
            )
            """))
        except SQLAlchemyError as e:
            print(f"Error creating table: {e}")
            return
    
    # Insert data into the table
    try:
        scores.to_sql('user_scores', engine, if_exists='append', index=False)
        print("Data exported to PostgreSQL database.")
    except SQLAlchemyError as e:
        print(f"Error inserting data: {e}")
