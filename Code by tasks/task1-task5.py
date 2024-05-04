#Problem Statement : 
#The task is to clean, process, and analyze census data from a given source, including data renaming, missing data handling, state/UT name standardization, new state/UT formation handling, data storage, database connection, and querying. The goal is to ensure uniformity, accuracy, and accessibility of the census data for further analysis and visualization.

#Task 1: Rename the Column names
#For uniformity in the datasets and taking into consideration the census year, we need to rename some columns. 
#State name  to State/UT
#District name  to District
#Male_Literate to Literate_Male
#Female_Literate to Literate_Female
#Rural_Households  to Households_Rural
#Urban_ Households  to Households_Urban
#Age_Group_0_29 to Young_and_Adult
#Age_Group_30_49 to Middle_Aged
#Age_Group_50 to Senior_Citizen
#Age not stated to Age_Not_Stated

#importing necessary library
import pandas as pd
#reading the contents of uploaded excel file
df = pd.read_excel("/content/sample_data/census_2011.xlsx")     
#using rename function to rename columns of dataset
df.rename(columns={'State name':'State/UT', 'District name':'District', 'Male_Literate':'Literate_Male',
                   'Female_Literate':'Literate_Female', 'Rural_Households':'Households_Rural', 'Urban_Households':'Households_Urban',
                   'Age_Group_0_29':'Young_and_Adult', 'Age_Group_30_49':'Middle_Aged','Age_Group_50':'Senior_Citizen',
                  'Age not stated':'Age_Not_Stated'}, inplace=True)
#print output 
df


#Task 2: Rename State/UT Names
#The State/UT names are in all caps in the census data, For uniformity across datasets we use the names so that only the first character of each word in the name is in upper case and the rest are in lower case. However, if the word is “and” then it should be all lowercase.

# Define a function for renaming the state names
def rename_state(state):
    # Splitting each word in the state name
    words = state.split()
    # Creating a list for storing renamed words in the state name
    renamed_words = []
    for i in words:
        if i == 'AND':
            # If the word 'and' is found, store it into the list after converting it into lowercase
            renamed_words.append(i.lower())
        else:
            # For all other words, make the first letter uppercase and the rest lowercase
            renamed_words.append(i.capitalize())
    # Join the appended words using a space
    return ' '.join(renamed_words)

# Applying the rename_state function to 'State/UT' column
df['State/UT'] = df['State/UT'].apply(rename_state)
# Display the DataFrame
df


#Task 3: New State/UT formation
#In 2014 Telangana was formed after it split from Andhra Pradesh, The districts that were included in Telangana are stored in Data/Telangana.txt . Read the text file and Rename the State/UT From “Andhra Pradesh” to “Telangana” for the given districts.
#In 2019 Ladakh was formed after it split from Jammu and Kashmir, which included the districts Leh and Kargil.  Rename the State/UT From “Jammu and Kashmir” to “Ladakh” for the given districts. 

# Renaming state name from 'Andhra Pradesh' to 'Telangana' for districts in text file
with open('/content/sample_data/Telangana.txt', 'r', encoding='utf-8-sig') as txt_file:
    # Opening the text file in read mode and removing newline character from each line, storing into a list
    txt_districts = [i.strip() for i in txt_file]

# Defining a function for renaming state name
def new_state(row):
    # If district in text file is found in any row of 'District' column, replace state name as 'Telangana'
    if row['District'] in txt_districts:
        return 'Telangana'
    else:
        # For all other districts, maintain the same old state name
        return row['State/UT']

# Applying the function to every row of 'State/UT' column
df['State/UT'] = df.apply(new_state, axis=1)

# Verifying the results
filter_rows = df[df['State/UT'] == 'Telangana']
result = filter_rows[['State/UT', 'District']]
# Printing the result
print(result)  

# Renaming state name from 'Jammu and Kashmir' to 'Ladakh' for Leh and Kargil
def new_state(row):
    # If district in text file is found in any row of 'District' column, replace state name as 'Ladakh'
    if row['District'] in jk_district:
        return 'Ladakh'
    else:
        # For all other districts, maintain the same old state name
        return row['State/UT']

# Applying the function to every row of 'State/UT' column
df['State/UT'] = df.apply(new_state, axis=1)

# Verifying the results
filter_rows = df[df['State/UT'] == 'Ladakh']
result = filter_rows[['State/UT', 'District']]
# Printing the result
print(result)  


#Task 4: Find and process Missing Data
#Find and store the percentage of data missing for each column.
#Some data can be found and filled in by using information from other cells. Try to find the correct data by using information from other cells and filling it in. Find and store the percentage of data missing for each column.
#Hint:
#Population = Male + Female
#Literate = Literate_Male + Literate_Female
#Population  = Young_and_Adult+  Middle_Aged + Senior_Citizen + Age_Not_Stated
#Households = Households_Rural + Households_Urban 
#compares the amount of missing data before and after the data-filling process was done. 

# Importing numpy library for NaN (missing or undefined values)
import numpy as np  

# Defining a function to calculate the percentage of missing data in a column
def data_miss_percentage(column):
    missing_rows = column.isnull().sum()
    total_rows = len(column)
    miss_percentage_before_fill = (missing_rows / total_rows) * 100
    return miss_percentage_before_fill

# List of columns required for analysis
columns_required = ['Population', 'Male', 'Female', 'Literate', 'Literate_Male', 'Literate_Female',
                    'Young_and_Adult', 'Middle_Aged', 'Senior_Citizen', 'Age_Not_Stated',
                    'Households', 'Households_Rural', 'Households_Urban']

# Display missing data percentage before filling
for i in columns_required:
    miss_percentage = data_miss_percentage(df[i])
    print(f'Data missing percentage in {i} column before filling data: {miss_percentage}')

print('***********************************************************************************************')

# Filling missing data in population-related columns
df['Population'] = df['Population'].fillna(df['Male'] + df['Female'])
df['Male'] = df['Male'].fillna(df['Population'] - df['Female'])
df['Female'] = df['Female'].fillna(df['Population'] - df['Male'])

# Filling missing data in literacy-related columns
df['Literate'] = df['Literate'].fillna(df['Literate_Male'] + df['Literate_Female'])
df['Literate_Male'] = df['Literate_Male'].fillna(df['Literate'] - df['Literate_Female'])
df['Literate_Female'] = df['Literate_Female'].fillna(df['Literate'] - df['Literate_Male'])

# Filling missing data in age-related columns
df['Population'] = df['Population'].fillna(df['Young_and_Adult'] + df['Middle_Aged'] + df['Senior_Citizen'] + df['Age_Not_Stated'])
df['Young_and_Adult'] = df['Young_and_Adult'].fillna(df['Population'] - (df['Middle_Aged'] + df['Senior_Citizen'] + df['Age_Not_Stated']))
df['Middle_Aged'] = df['Middle_Aged'].fillna(df['Population'] - (df['Young_and_Adult'] + df['Senior_Citizen'] + df['Age_Not_Stated']))
df['Senior_Citizen'] = df['Senior_Citizen'].fillna(df['Population'] - (df['Young_and_Adult'] + df['Middle_Aged'] + df['Age_Not_Stated']))
df['Age_Not_Stated'] = df['Age_Not_Stated'].fillna(df['Population'] - (df['Young_and_Adult'] + df['Middle_Aged'] + df['Senior_Citizen']))

# Filling missing data in household-related columns
df['Households'] = df['Households'].fillna(df['Households_Rural'] + df['Households_Urban'])
df['Households_Rural'] = df['Households_Rural'].fillna(df['Households'] - df['Households_Urban'])
df['Households_Urban'] = df['Households_Urban'].fillna(df['Households'] - df['Households_Rural'])

# Display missing data percentage after filling
for i in columns_required:
    miss_percentage = data_miss_percentage(df[i])
    print(f'Data missing percentage in {i} column after filling data: {miss_percentage}')


#Task  5: Save Data to MongoDB
#Save the processed data to mongoDB with a collection named “census” .

#importing necessary libraries
from pymongo import MongoClient

#connecting to MongoDB Atlas
client = MongoClient('Provide mongodb connection string here..')
#creating the database & collection in MongoDB Cloud
db = client['Capstone_Project']
collection = db['census']

#converting DF to dictionary
data = df.to_dict("records")
#inserting data into MongoDB
collection.insert_many(data)
#closing the connection
client.close()
