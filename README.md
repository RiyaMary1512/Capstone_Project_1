# Capstone_Project_1
Repository for storing code of capstone project - 1

# Census Data Analysis and Visualization

This project aims to clean, process, and analyze census data from a given source. It includes tasks such as data renaming, missing data handling, state/UT name standardization, new state/UT formation handling, data storage, database connection, querying, and visualization using Streamlit.

## Tasks

1. **Rename Column Names**: Rename specific columns in the census data for uniformity and clarity.
2. **Rename State/UT Names**: Standardize the state/UT names by capitalizing the first letter of each word, except for "and" which should be in lowercase.
3. **New State/UT Formation**: Handle the formation of new states/UTs like Telangana and Ladakh by updating the corresponding district data.
4. **Find and Process Missing Data**: Identify and handle missing data by filling in values using information from other columns.
5. **Save Data to MongoDB**: Store the processed data in a MongoDB database.
6. **Database Connection and Data Upload**: Fetch data from MongoDB and upload it to a relational database (MySQL) while maintaining appropriate table structures, primary keys, and foreign keys.
7. **Run Queries on the Database and Streamlit Visualization**: Execute SQL queries on the MySQL database to retrieve various census-related information and visualize the results using Streamlit.

## Dependencies

- Python 3.x
- pandas
- numpy
- pymongo
- mysql.connector
- streamlit

## Usage

1. **Install Dependencies**
- Install the required Python dependencies by running the following command: pip install -r requirements.txt
  This will install the necessary libraries like pandas, numpy, pymongo, mysql.connector, and streamlit.

2. **Set up MongoDB**
- Install MongoDB on your machine or set up a MongoDB Atlas cluster (cloud-based MongoDB service).
- If you're using a local MongoDB instance, make sure the MongoDB server is running.
- If you're using MongoDB Atlas, obtain the connection string from the Atlas dashboard.

3. **Set up MySQL**
- Install MySQL on your machine or use a cloud-based MySQL service.
- Create a new database for the project.
- Obtain the MySQL connection details (host, user, password, database name).

4. **Update Connection Strings and Credentials**
- In the Python code (`Answers_task1-7.py`), locate the sections where the MongoDB and MySQL connections are established.
- Replace the placeholders with your actual connection strings and credentials.
- For MongoDB, update the `MongoClient` connection string.
- For MySQL, update the `mysql.connector.connect` parameters with your host, user, password, and database name. For example:
  ```python
  mysql_connection = mysql.connector.connect(
    host="provide host name",
    user="provide user name",
    password="provide your password",
    database="Capstone_Project") #Your database name) ```

5. **Run the Python Script**
- Open a terminal or command prompt.
- Navigate to the project directory containing the `Answers_task1-7.py` file.
- Run the Python script using the following command: python Answers_task1-7.py

The script will execute the tasks in order, including data renaming, missing data handling, state/UT name standardization, new state/UT formation handling, data storage in MongoDB, and database connection and data upload to MySQL.

6. **Streamlit Visualization (Task 7)**
- After running the Python script, the Streamlit app for Task 7 will be launched automatically.
- The app will display various visualizations and query results based on the census data stored in the MySQL database.
- You can interact with the app, view the visualizations, and explore the query results.

Note: Ensure that you have the necessary permissions and configurations set up for MongoDB and MySQL connections. If you encounter any issues, refer to the official documentation or seek assistance from the respective communities.

## File Structure

- `Answers_task1-7.py`: Contains the Python code for all tasks.
- `Telangana.txt`: Text file containing the list of districts included in Telangana.
- `census_2011.xlsx`: Sample census data in an Excel file format.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
