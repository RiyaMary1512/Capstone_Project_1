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

1. Install the required dependencies using `pip install -r requirements.txt`.
2. Set up MongoDB and MySQL databases with the appropriate configurations.
3. Update the connection strings and database credentials in the code.
4. Run the Python script to execute the tasks.
5. For Task 7, the Streamlit app will be launched, and you can interact with the visualizations and query results.

## File Structure

- `Answers_task1-7.py`: Contains the Python code for all tasks.
- `Telangana.txt`: Text file containing the list of districts included in Telangana.
- `census_2011.xlsx`: Sample census data in an Excel file format.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
