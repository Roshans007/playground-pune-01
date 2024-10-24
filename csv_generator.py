import pandas as pd
import sqlite3
import random
import csv

# Database connection setup (Using SQLite for this example)
def create_db_connection(db_file):
    """ Create a database connection to an SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Fetch distinct values from a specific column in the database
def fetch_random_db_values(conn, db_column, table_name, num_values):
    query = f"SELECT DISTINCT {db_column} FROM {table_name} LIMIT {num_values}"
    cur = conn.cursor()
    cur.execute(query)
    return [row[0] for row in cur.fetchall()]

# Function to generate CSV with matched and manually entered values
def generate_csv_report(headers, db_columns_map, user_values, db_table, output_csv, db_file, num_rows=10):
    # Establish DB connection
    conn = create_db_connection(db_file)
    
    # Initialize data for CSV
    data = {header: [] for header in headers}
    
    # Populate matched columns from DB
    for csv_column, db_column in db_columns_map.items():
        if csv_column in headers:
            # Fetch random values from DB and add them to data
            db_values = fetch_random_db_values(conn, db_column, db_table, num_rows)
            data[csv_column].extend(random.choices(db_values, k=num_rows))
    
    # Populate rest of the columns with user input values
    for col, value in user_values.items():
        if col in headers and col not in db_columns_map.keys():
            data[col].extend([value] * num_rows)
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save DataFrame to CSV
    df.to_csv(output_csv, index=False)
    print(f"CSV report generated: {output_csv}")

# Example of how the function would be used
if __name__ == "__main__":
    # Specify headers you want in your CSV
    headers = ['Name', 'Age', 'City', 'Occupation']

    # Mapping of CSV columns to database columns
    db_columns_map = {
        'Name': 'name_column',
        'City': 'city_column'
    }

    # Values for other columns not populated from the database
    user_values = {
        'Age': 30,
        'Occupation': 'Engineer'
    }

    # Specify the name of your DB table and output CSV file
    db_table = 'your_table_name'
    db_file = 'your_database.db'
    output_csv = 'generated_report.csv'
    
    # Generate the report
    generate_csv_report(headers, db_columns_map, user_values, db_table, output_csv, db_file, num_rows=10)