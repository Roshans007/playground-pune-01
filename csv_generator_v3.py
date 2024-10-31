import pandas as pd
import cx_Oracle
import random

# Database connection setup for Oracle
def create_db_connection(user, password, host, port, service_name):
    """Create a database connection to an Oracle database."""
    dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
    try:
        conn = cx_Oracle.connect(user=user, password=password, dsn=dsn)
        return conn
    except cx_Oracle.DatabaseError as e:
        print(f"Error connecting to Oracle DB: {e}")
        return None

# Fetch full rows from the database for columns specified in db_columns_map
def fetch_db_rows(conn, db_columns_map, table_name, num_rows):
    columns = ', '.join(db_columns_map.values())
    query = f"SELECT {columns} FROM {table_name} FETCH FIRST {num_rows} ROWS ONLY"
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

# Function to generate CSV with matched and manually entered values
def generate_csv_report(headers, db_columns_map, user_values, db_table, output_csv, conn, num_rows=10):
    # Initialize data for CSV
    data = {header: [] for header in headers}
    
    # Fetch rows from DB for the specified columns in db_columns_map
    db_rows = fetch_db_rows(conn, db_columns_map, db_table, num_rows)

    # Randomly select rows from fetched data
    selected_rows = random.choices(db_rows, k=num_rows)
    
    # Populate matched columns from DB rows
    db_columns = list(db_columns_map.keys())
    for i, row in enumerate(selected_rows):
        for j, csv_column in enumerate(db_columns):
            if csv_column in headers:
                data[csv_column].append(row[j])
    
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
        'Name': 'NAME_COLUMN',
        'City': 'CITY_COLUMN'
    }

    # Values for other columns not populated from the database
    user_values = {
        'Age': 30,
        'Occupation': 'Engineer'
    }

    # Specify the name of your DB table and output CSV file
    db_table = 'YOUR_TABLE_NAME'
    
    # Oracle Database connection details
    db_user = 'your_username'
    db_password = 'your_password'
    db_host = 'your_db_host'
    db_port = 'your_db_port'
    db_service_name = 'your_service_name'

    # Establish connection to Oracle DB
    conn = create_db_connection(db_user, db_password, db_host, db_port, db_service_name)

    if conn:
        # Specify the output CSV file
        output_csv = 'generated_report.csv'
        
        # Generate the report
        generate_csv_report(headers, db_columns_map, user_values, db_table, output_csv, conn, num_rows=10)
        
        # Close the DB connection
        conn.close()