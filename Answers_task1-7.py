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


#Task 6: Database connection and data upload
#Data should be fetched from the mongoDB and to be uploaded to a relational database using python code . The table names should be the same as the file names without the extension.
#The primary key and foreign key constraints should be included in the tables wherever required.

import pymongo
import mysql.connector
import math

# Connect to MongoDB
mongo_client = pymongo.MongoClient('Provide mongodb connection string here..')
mongo_db = mongo_client['Capstone_Project']
mongo_collection = mongo_db['census']

# Connect to MySQL
mysql_connection = mysql.connector.connect(
    host="provide host name",
    user="provide user name",
    password="provide your password",
    database="Capstone_Project"   #your database name
)
mysql_cursor = mysql_connection.cursor()

# Fetch data from MongoDB and convert it to a list
mongo_data = list(mongo_collection.find())

# Define a function to replace brackets with underscores in column names
def clean_column_name(column_name):
    return column_name.replace("[", "_").replace("]", "_")

# Define a dictionary to map column names from mongo db to MySQL
column_map = {
    "District code": "dist_code",
    "State/UT": "state_ut",
    "District": "district",
    "Population": "population",
    "Male": "male_pop",
    "Female": "female_pop",
    "Literate": "literate_pop",
    "Literate_Male": "literate_male",
    "Literate_Female": "literate_female",
    "SC": "sc_pop",
    "Male_SC": "sc_male",
    "Female_SC": "sc_female",
    "ST": "st_pop",
    "Male_ST": "st_male",
    "Female_ST": "st_female",
    "Workers": "workers",
    "Male_Workers": "male_workers",
    "Female_Workers": "female_workers",
    "Main_Workers": "main_workers",
    "Marginal_Workers": "marginal_workers",
    "Non_Workers": "non_workers",
    "Cultivator_Workers": "cultivator_workers",
    "Agricultural_Workers": "agri_workers",
    "Household_Workers": "hh_workers",
    "Other_Workers": "other_workers",
    "Hindus": "hindu_pop",
    "Muslims": "muslim_pop",
    "Christians": "christian_pop",
    "Sikhs": "sikh_pop",
    "Buddhists": "buddhist_pop",
    "Jains": "jain_pop",
    "Others_Religions": "other_religion_pop",
    "Religion_Not_Stated": "religion_not_stated",
    "LPG_or_PNG_Households": "lpg_png_hh",
    "Housholds_with_Electric_Lighting": "elec_lighting_hh",
    "Households_with_Internet": "internet_hh",
    "Households_with_Computer": "computer_hh",
    "Households_Rural": "rural_hh",
    "Households_Urban": "urban_hh",
    "Households": "house_holds"
    "Households Below_Primary_Education": "below_primary_edu_hh",
    "Primary_Education": "primary_edu_pop",
    "Middle_Education": "middle_edu_pop",
    "Secondary_Education": "secondary_edu_pop",
    "Higher_Education": "higher_edu_pop",
    "Graduate_Education": "graduate_edu_pop",
    "Other_Education": "other_edu_pop",
    "Literate_Education": "literate_edu_pop",
    "Illiterate_Education": "illiterate_edu_pop",
    "Total_Education": "total_edu_pop",
    "Young_and_Adult": "young_adult_pop",
    "Middle_Aged": "middle_aged_pop",
    "Senior_Citizen": "senior_citizen_pop",
    "Age_Not_Stated": "age_not_stated_pop",
    "Households_with_Bicycle": "bicycle_hh",
    "Households_with_Car_Jeep_Van": "car_jeep_van_hh",
    "Households_with_Radio_Transistor": "radio_transistor_hh",
    "Households_with_Scooter_Motorcycle_Moped": "scooter_motorcycle_hh",
    "Households_with_Telephone_Mobile_Phone_Landline_only": "landline_only_hh",
    "Households_with_Telephone_Mobile_Phone_Mobile_only": "mobile_only_hh",
    "Households_with_TV_Computer_Laptop_Telephone_mobile_phone_and_Scooter_Car": "tv_computer_phone_scooter_car_hh",
    "Households_with_Television": "tv_hh",
    "Households_with_Telephone_Mobile_Phone": "telephone_mobile_hh",
    "Households_with_Telephone_Mobile_Phone_Both": "telephone_mobile_both_hh",
    "Condition_of_occupied_census_houses_Dilapidated_Households": "dilapidated_hh",
    "Households_with_separate_kitchen_Cooking_inside_house": "separate_kitchen_hh",
    "Having_bathing_facility_Total_Households": "bathing_facility_hh",
    "Having_latrine_facility_within_the_premises_Total_Households": "latrine_facility_hh",
    "Ownership_Owned_Households": "owned_hh",
    "Ownership_Rented_Households": "rented_hh",
    "Type_of_bathing_facility_Enclosure_without_roof_Households": "open_bathing_hh",
    "Type_of_fuel_used_for_cooking_Any_other_Households": "other_cooking_fuel_hh",
    "Type_of_latrine_facility_Pit_latrine_Households": "pit_latrine_hh",
    "Type_of_latrine_facility_Other_latrine_Households": "other_latrine_hh",
    "Type_of_latrine_facility_Night_soil_disposed_into_open_drain_Households": "open_drain_latrine_hh",
    "Type_of_latrine_facility_Flush_pour_flush_latrine_connected_to_other_system_Households": "flush_latrine_other_system_hh",
    "Not_having_bathing_facility_within_the_premises_Total_Households": "no_bathing_facility_hh",
    "Not_having_latrine_facility_within_the_premises_Alternative_source_Open_Households": "no_latrine_facility_open_hh",
    "Main_source_of_drinking_water_Un_covered_well_Households": "uncovered_well_water_hh",
    "Main_source_of_drinking_water_Handpump_Tubewell_Borewell_Households": "handpump_tubewell_water_hh",
    "Main_source_of_drinking_water_Spring_Households": "spring_water_hh",
    "Main_source_of_drinking_water_River_Canal_Households": "river_canal_water_hh",
    "Main_source_of_drinking_water_Other_sources_Households": "other_water_sources_hh",
    "Main_source_of_drinking_water_Other_sources_Spring_River_Canal_Tank_Pond_Lake_Other_sources__Households": "other_water_sources_combined_hh",
    "Location_of_drinking_water_source_Near_the_premises_Households": "water_source_near_premises_hh",
    "Location_of_drinking_water_source_Within_the_premises_Households": "water_source_within_premises_hh",
    "Main_source_of_drinking_water_Tank_Pond_Lake_Households": "tank_pond_lake_water_hh",
    "Main_source_of_drinking_water_Tapwater_Households": "tap_water_hh",
    "Main_source_of_drinking_water_Tubewell_Borehole_Households": "tubewell_borehole_water_hh",
    "Household_size_1_person_Households": "hh_size_1_person",
    "Household_size_2_persons_Households": "hh_size_2_persons",
    "Household_size_1_to_2_persons": "hh_size_1_2_persons",
    "Household_size_3_persons_Households": "hh_size_3_persons",
    "Household_size_3_to_5_persons_Households": "hh_size_3_5_persons",
    "Household_size_4_persons_Households": "hh_size_4_persons",
    "Household_size_5_persons_Households": "hh_size_5_persons",
    "Household_size_6_8_persons_Households": "hh_size_6_8",
    "Household_size_9_persons_and_above_Households": "hh_size_9_plus",
    "Location_of_drinking_water_source_Away_Households": "water_source_away_hh",
    "Married_couples_1_Households": "married_couples_1_hh",
    "Married_couples_2_Households": "married_couples_2_hh",
    "Married_couples_3_Households": "married_couples_3_hh",
    "Married_couples_3_or_more_Households": "married_couples_3_plus_hh",
    "Married_couples_4_Households": "married_couples_4_hh",
    "Married_couples_5__Households": "married_couples_5_hh",
    "Married_couples_None_Households": "married_couples_none_hh",
    "Power_Parity_Less_than_Rs_45000": "power_parity_less_45000",
    "Power_Parity_Rs_45000_90000": "power_parity_45000_90000",
    "Power_Parity_Rs_90000_150000": "power_parity_90000_150000",
    "Power_Parity_Rs_45000_150000": "power_parity_45000_150000",
    "Power_Parity_Rs_150000_240000": "power_parity_150000_240000",
    "Power_Parity_Rs_240000_330000": "power_parity_240000_330000",
    "Power_Parity_Rs_150000_330000": "power_parity_150000_330000",
    "Power_Parity_Rs_330000_425000": "power_parity_330000_425000",
    "Power_Parity_Rs_425000_545000": "power_parity_425000_545000",
    "Power_Parity_Rs_330000_545000": "power_parity_330000_545000",
    "Power_Parity_Above_Rs_545000": "power_parity_above_545000",
    "Total_Power_Parity": "total_power_parity"
}

# Define function to handle nan values
def handle_nan(value):
    if isinstance(value, float) and math.isnan(value):
        return None
    return value

# Define function to escape special characters
def escape_special_characters(value):
    if isinstance(value, str):
        return value.replace("`", "``")  # Escape backticks
    return value

# Create a single MySQL table
create_table_query = "CREATE TABLE IF NOT EXISTS census ("
column_names = set(column_map.values())
for document in mongo_data:
    document_column_names = {clean_column_name(key.replace("/", "_").replace(" ", "_").replace("(", "_").replace(")", "_"))[:64] for key in document.keys() if key not in column_map}
    column_names.update(document_column_names)
for column_name in column_names:
    if column_name in ["state_ut", "district"]:
        create_table_query += f"`{column_name}` VARCHAR(255), "  # Adjust size as needed
    else:
        create_table_query += f"`{column_name}` MEDIUMTEXT, "
create_table_query = create_table_query[:-2] + ")"
mysql_cursor.execute(create_table_query)
mysql_connection.commit()

# Insert data into MySQL table
for document in mongo_data:
    filtered_data = {column_map.get(key, clean_column_name(key.replace("/", "_").replace(" ", "_").replace("(", "_").replace(")", "_"))[:64]): handle_nan(escape_special_characters(value)) for key, value in document.items() if key != "_id"}
    column_names = [key for key in filtered_data.keys()]
    values = tuple(filtered_data.values())
    placeholders = ", ".join(["%s"] * len(filtered_data))
    insert_query = f"INSERT INTO census ({', '.join(column_names)}) VALUES ({placeholders})"
    mysql_cursor.execute(insert_query, values)
    mysql_connection.commit()

# Close connections
mysql_cursor.close()
mysql_connection.close()
mongo_client.close()


#Task 7: Run Query on the database and show output on streamlit:

import mysql.connector
import streamlit as st
import math

# Connect to MySQL
mysql_connection = mysql.connector.connect(
    host="provide host name",
    user="provide user name",
    password="provide your password",
    database="Capstone_Project" # Your database name
)
mysql_cursor = mysql_connection.cursor()

# Function to fetch data from each table and display in Streamlit
def display_data_streamlit():
    st.header("Task 7")
    
    st.write("1. What is the total population of each district?")
    # Query to fetch district and population columns 
    mysql_cursor.execute(f"SELECT District, Population FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display population for each district
    for row in data:
        district, population = row
        st.write(f"District: {district}, Population: {population}")
            
    st.write("2.How many literate males and females are there in each district?")
    # Query 
    mysql_cursor.execute(f"SELECT District, literate_male, literate_female FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display output for each district
    for row in data:
        district, literate_male, literate_female = row
        st.write(f"District: {district}, Literate Male: {literate_male}, Literate Female: {literate_female}")
    
    st.write("3. What is the percentage of workers (both male and female) in each district?")
    # Query 
    mysql_cursor.execute(f"SELECT District, population, workers FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:
        district, population, workers = row
        if population is not None and workers is not None and population != 0 and workers != 0:
            # Convert population and workers to float
            population = float(population)
            workers = float(workers)
            
            percentage = (workers / population) * 100
            st.write(f"District: {district}, Percentage of Workers:{percentage:.2f}%")
    
    st.write("4. How many households have access to LPG or PNG as a cooking fuel in each district?")
    # Query 
    mysql_cursor.execute(f"SELECT District, lpg_png_hh FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:
        district, lpg_png_hh = row
        st.write(f"Households have access to LPG or PNG as a cooking fuel in {district} = {lpg_png_hh}")

    st.write("5. What is the religious composition (Hindus, Muslims, Christians, etc.) of each district?")
    # Query 
    mysql_cursor.execute(f"SELECT District, population, hindu_pop, muslim_pop, christian_pop,sikh_pop,buddhist_pop,jain_pop,other_religion_pop,Religion_Not_Stated FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    #calculation & output
    for row in data:
        district, population, hindu_pop, muslim_pop, christian_pop,sikh_pop,buddhist_pop,jain_pop,other_religion_pop,Religion_Not_Stated = row
        if not None in(population, hindu_pop, muslim_pop, christian_pop, sikh_pop, buddhist_pop, jain_pop, other_religion_pop, Religion_Not_Stated):
        # Convert values to float
            population = float(population)
            hindu_pop = float(hindu_pop)
            muslim_pop = float(muslim_pop)
            christian_pop = float(christian_pop)
            sikh_pop = float(sikh_pop)
            buddhist_pop = float(buddhist_pop)
            jain_pop = float(jain_pop)
            other_religion_pop = float(other_religion_pop)
            Religion_Not_Stated = float(Religion_Not_Stated)

            hin = (hindu_pop/population)*100
            mus = (muslim_pop/population)*100
            chri = (christian_pop/population)*100
            sikh = (sikh_pop/population)*100
            buddh = (buddhist_pop/population)*100
            jain = (jain_pop/population)*100
            oth = (other_religion_pop/population)*100
            not_state = (Religion_Not_Stated/population)*100
            st.write(f"religious composition of {district}: Hindus = {hin:2f}%, Muslims = {mus:.2f}%, Christians = {chri:.2f}%, Sikhs = {sikh:.2f}%, Budhhidts = {buddh:.2f}%, Jains = {jain:.2f}%, Others = {oth:.2f}%, Religion not stated = {not_state:.2f}%")

    st.write("6. How many households have internet access in each district?")
    # Query 
    mysql_cursor.execute(f"SELECT District, internet_hh FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:
        district, internet_hh = row
        st.write(f"Households having internet access in {district} = {internet_hh}")


    st.write("7. What is the educational attainment distribution (below primary, primary, middle, secondary, etc.) in each district?")
    # Query 
    mysql_cursor.execute(f"SELECT District, below_primary_edu_hh, primary_edu_pop, middle_edu_pop, secondary_edu_pop, higher_edu_pop, graduate_edu_pop, other_edu_pop, total_edu_pop FROM capstone_project.census")
    data = mysql_cursor.fetchall()

    # Display output
    for row in data:
        district, below_primary_edu_hh, primary_edu_pop, middle_edu_pop, secondary_edu_pop, higher_edu_pop, graduate_edu_pop, other_edu_pop, total_edu_pop = row

        if total_edu_pop != 0 and None not in (below_primary_edu_hh, primary_edu_pop, middle_edu_pop, secondary_edu_pop, higher_edu_pop, graduate_edu_pop, other_edu_pop, total_edu_pop):
            # Convert values to float if they are not None
            below_primary_edu_hh = float(below_primary_edu_hh) if below_primary_edu_hh is not None else 0
            primary_edu_pop = float(primary_edu_pop) if primary_edu_pop is not None else 0
            middle_edu_pop = float(middle_edu_pop) if middle_edu_pop is not None else 0
            secondary_edu_pop = float(secondary_edu_pop) if secondary_edu_pop is not None else 0
            higher_edu_pop = float(higher_edu_pop) if higher_edu_pop is not None else 0
            graduate_edu_pop = float(graduate_edu_pop) if graduate_edu_pop is not None else 0
            other_edu_pop = float(other_edu_pop) if other_edu_pop is not None else 0

            # Calculate percentages
            below_p = (below_primary_edu_hh / total_edu_pop) * 100
            pr_ed = (primary_edu_pop / total_edu_pop) * 100
            mid_ed = (middle_edu_pop / total_edu_pop) * 100
            sec_ed = (secondary_edu_pop / total_edu_pop) * 100
            high_ed = (higher_edu_pop / total_edu_pop) * 100
            grad_ed = (graduate_edu_pop / total_edu_pop) * 100
            other_ed = (other_edu_pop / total_edu_pop) * 100

            # Write output
            st.write(f"Educational attainment distribution in {district}: Below primary = {below_p:.2f}%, Primary education = {pr_ed:.2f}%, Middle education = {mid_ed:.2f}%, Secondary education = {sec_ed:.2f}%, Higher education = {high_ed:.2f}%, Graduate education = {grad_ed:.2f}%, Other education = {other_ed:.2f}%")



    st.write("8. How many households have access to various modes of transportation (bicycle, car, radio, television, etc.) in each district?")
    # Query 
    mysql_cursor.execute(f"SELECT District, bicycle_hh, car_jeep_van_hh, radio_transistor_hh, scooter_motorcycle_hh, landline_only_hh, mobile_only_hh, tv_computer_phone_scooter_car_hh, tv_hh, telephone_mobile_hh, telephone_mobile_both_hh FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:
        district, bicycle_hh, car_jeep_van_hh, radio_transistor_hh, scooter_motorcycle_hh, landline_only_hh, mobile_only_hh, tv_computer_phone_scooter_car_hh, tv_hh, telephone_mobile_hh, telephone_mobile_both_hh = row

         # Convert string values to integers
        bicycle_hh = int(bicycle_hh) if bicycle_hh and not math.isnan(float(bicycle_hh)) else 0
        car_jeep_van_hh = int(car_jeep_van_hh) if car_jeep_van_hh and not math.isnan(float(car_jeep_van_hh)) else 0
        radio_transistor_hh = int(radio_transistor_hh) if radio_transistor_hh and not math.isnan(float(radio_transistor_hh)) else 0
        scooter_motorcycle_hh = int(scooter_motorcycle_hh) if scooter_motorcycle_hh and not math.isnan(float(scooter_motorcycle_hh)) else 0
        landline_only_hh = int(landline_only_hh) if landline_only_hh and not math.isnan(float(landline_only_hh)) else 0
        mobile_only_hh = int(mobile_only_hh) if mobile_only_hh and not math.isnan(float(mobile_only_hh)) else 0
        tv_computer_phone_scooter_car_hh = int(tv_computer_phone_scooter_car_hh) if tv_computer_phone_scooter_car_hh and not math.isnan(float(tv_computer_phone_scooter_car_hh)) else 0
        tv_hh = int(tv_hh) if tv_hh and not math.isnan(float(tv_hh)) else 0
        telephone_mobile_hh = int(telephone_mobile_hh) if telephone_mobile_hh and not math.isnan(float(telephone_mobile_hh)) else 0
        telephone_mobile_both_hh = int(telephone_mobile_both_hh) if telephone_mobile_both_hh and not math.isnan(float(telephone_mobile_both_hh)) else 0

        total_transportation_hh = sum([bicycle_hh, car_jeep_van_hh, radio_transistor_hh, scooter_motorcycle_hh, landline_only_hh, mobile_only_hh, tv_computer_phone_scooter_car_hh, tv_hh, telephone_mobile_hh, telephone_mobile_both_hh])
        st.write(f"Households having access to various modes of transpor0tation in {district} = {total_transportation_hh}")
        
    st.write("9. What is the condition of occupied census houses (dilapidated, with separate kitchen, with bathing facility, with latrine facility, etc.) in each district?")
    # Query 
    mysql_cursor.execute(f"SELECT District, dilapidated_hh, separate_kitchen_hh, bathing_facility_hh, latrine_facility_hh, owned_hh, rented_hh, open_bathing_hh, other_cooking_fuel_hh, pit_latrine_hh, other_latrine_hh,open_drain_latrine_hh, flush_latrine_other_system_hh, no_bathing_facility_hh, no_latrine_facility_open_hh, uncovered_well_water_hh, handpump_tubewell_water_hh, spring_water_hh, river_canal_water_hh, other_water_sources_hh, other_water_sources_combined_hh, water_source_near_premises_hh, water_source_within_premises_hh, tank_pond_lake_water_hh, tap_water_hh, tubewell_borehole_water_hh FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:
        District, dilapidated_hh, separate_kitchen_hh, bathing_facility_hh, latrine_facility_hh, owned_hh, rented_hh, open_bathing_hh, other_cooking_fuel_hh, pit_latrine_hh, other_latrine_hh,open_drain_latrine_hh, flush_latrine_other_system_hh, no_bathing_facility_hh, no_latrine_facility_open_hh, uncovered_well_water_hh, handpump_tubewell_water_hh, spring_water_hh, river_canal_water_hh, other_water_sources_hh, other_water_sources_combined_hh, water_source_near_premises_hh, water_source_within_premises_hh, tank_pond_lake_water_hh, tap_water_hh, tubewell_borehole_water_hh = row

        st.write(f"Condition of occupied census houses in {district}: Dilapidated_Households = {dilapidated_hh}, Separate Kitchen = {separate_kitchen_hh}, Bathing facility = {bathing_facility_hh}, Latrine facility within premises = {latrine_facility_hh}, Ownership owned households = {owned_hh}, Ownership rented households = {rented_hh}, Bathing encosure withour roof = {open_bathing_hh}, Other cooking fuel = {other_cooking_fuel_hh}, Pit latrine = {pit_latrine_hh}, Other latrine = {other_latrine_hh}, Open drain = {open_drain_latrine_hh}, Flush latrine other systems = {flush_latrine_other_system_hh}, No bathing facility = {no_bathing_facility_hh}, No latrine facility = {no_latrine_facility_open_hh}, Uncovered wells = {uncovered_well_water_hh}, Drinking water = {handpump_tubewell_water_hh}, Source spring: {spring_water_hh}, River canal = {river_canal_water_hh}, Other sources = {other_water_sources_hh}, Combined water sources = {other_water_sources_combined_hh}, Water near premises = {water_source_near_premises_hh}, Within premises = {water_sources_within_premises}, Tank pond lake sources = {tank_pond_lake_water_hh}, Tapwater = {tap_water_hh}, Tubewell borehole = {tubewell_borehole_water_hh} ")
        
    st.write("10. How is the household size distributed (1 person, 2 persons, 3-5 persons, etc.) in each district?"
    # Query 
    mysql_cursor.execute(f"SELECT District, hh_size_1_person, hh_size_2_persons, hh_size_1_2_persons, hh_size_3_persons, hh_size_3_5_persons, hh_size_4_persons, hh_size_5_persons, hh_size_6_8, hh_size_9_plus FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data: 
        district, hh_size_1_person, hh_size_2_persons, hh_size_1_2_persons, hh_size_3_persons, hh_size_3_5_persons, hh_size_4_persons, hh_size_5_persons, hh_size_6_8, hh_size_9_plus = row
        st.write(f"Household size distributed in {district}: 1 person = {hh_size_1_person}, 2 persons = {hh_size_2_persons}, 1 to 2 persons = {hh_size_1_2_persons}, 3 persons = {hh_size_3_persons}, 3 to 5 persons = {hh_size_3_5_persons}, 4 persons = {hh_size_4_persons}, 5 persons = {hh_size_5_persons}, 6 to 8 persons = {hh_size_6_8}, more than 9 persons = {hh_size_9_plus}")
    
    st.write("11. What is the total number of households in each state?")
    # Query 
    mysql_cursor.execute(f"SELECT District, households FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:     
        district, house_holds = row
        st.write(f"Households in {district}:{house_holds}")
    
    st.write("12. How many households have a latrine facility within the premises in each state?")
    # Query 
    mysql_cursor.execute(f"SELECT District, latrine_facility_hh FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:     
        district, latrine_facility_hh = row
        st.write(f"Households having latrine facilities within premises in {district}:{latrine_facility_hh}")   
    
    st.write("13. What is the average household size in each state?")
    # Query 
    mysql_cursor.execute(f"SELECT state,AVG(hh_size_1_person +  2 * hh_size_2_persons +  1.5 * hh_size_1_2_persons +  3 * hh_size_3_persons +  4 * hh_size_3_5_persons +  4.5 * hh_size_4_persons +  5 * hh_size_5_persons +  7 * hh_size_6_8 +  9 * hh_size_9_plus) / (hh_size_1_person +  hh_size_2_persons +  hh_size_1_2_persons +  hh_size_3_persons +  hh_size_3_5_persons +  hh_size_4_persons + hh_size_5_persons + hh_size_6_8 + hh_size_9_plus) AS avg_household_size FROM capstone_project.census GROUP BY state; ")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:     
        state, avg_household_size = row
        st.write(f"What is the average household size in {state}:{avg_household_size:.2f}")  
    
    st.write("14. How many households are owned versus rented in each state?")
    # Query 
    mysql_cursor.execute(f" SELECT state, SUM(owned_hh) AS owned_households, SUM(rented_hh) AS rented_households FROM capstone_project.census GROUP BY state;")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:     
        state, owned_households, rented_households = row
        st.write(f"Owned verses rented households in {state}: Owned = {owned_households}, Rented = {rented_households}")  

    st.write("15. What is the distribution of different types of latrine facilities (pit latrine, flush latrine, etc.) in each state?")
    # Query 
    mysql_cursor.execute(f" SELECT state, pit_latrine_hh, other_latrine_hh, open_drain_latrine_hh, flush_latrine_other_system_hh FROM capstone_project.census GROUP BY state;")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:     
        state, pit_latrine_hh, other_latrine_hh, open_drain_latrine_hh, flush_latrine_other_system_hh = row
        st.write(f"Latrine facilities distribution in {state}: Pit latrine = {pit_latrine_hh}, Other latrine = {other_latrine_hh}, Open drain latrine = {open_drain_latrine_hh}, Flush latrine & other system = {flush_latrine_other_system_hh}")
     
    st.write("16. How many households have access to drinking water sources near the premises in each state?")
    # Query 
    mysql_cursor.execute(f" SELECT state, SUM(water_source_within_premises_hh) AS total_water_sources FROM capstone_project.census GROUP BY state")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:     
        state, total_water_sources = row
        st.write(f"Households having access to drinking water sources near the premises in {state}: {total_water_sources}")
             
    st.write("17. What is the average household income distribution in each state based on the power parity categories?")
    # Query 
    mysql_cursor.execute(f"SELECT state, AVG(power_parity_less_45000), AVG(power_parity_45000_90000), AVG(power_parity_90000_150000), AVG(power_parity_45000_150000), AVG(power_parity_150000_240000), AVG(power_parity_240000_330000), AVG(power_parity_150000_330000), AVG(power_parity_330000_425000), AVG(power_parity_425000_545000), AVG(power_parity_330000_545000), AVG(power_parity_above_545000) FROM capstone_project.census GROUP BY state")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:     
        state, avg_less_45000, avg_45000_90000, avg_90000_150000, avg_45000_150000, avg_150000_240000, avg_240000_330000, avg_150000_330000, avg_330000_425000, avg_425000_545000, avg_330000_545000, avg_above_545000 = row
        st.write(f"Average household income distribution in {state}: Less than $45,000: {avg_less_45000:.2f}, $45,000 - $90,000: {avg_45000_90000:.2f}, $90,000 - $150,000: {avg_90000_150000:.2f}, $45,000 - $150,000: {avg_45000_150000:.2f}, $150,000 - $240,000: {avg_150000_240000:.2f}, $240,000 - $330,000: {avg_240000_330000:.2f}, $150,000 - $330,000: {avg_150000_330000:.2f}, $330,000 - $425,000: {avg_330000_425000:.2f}, $425,000 - $545,000: {avg_425000_545000:.2f}, $330,000 - $545,000: {avg_330000_545000:.2f}, Above $545,000: {avg_above_545000:.2f}")

    st.write("18. What is the percentage of married couples with different household sizes in each state?")
    # Query 
    mysql_cursor.execute(f"SELECT state, married_couples_1_hh / total_married_couples * 100 AS percentage_1_hh, married_couples_2_hh / total_married_couples * 100 AS percentage_2_hh, married_couples_3_hh / total_married_couples * 100 AS percentage_3_hh, married_couples_3_plus_hh / total_married_couples * 100 AS percentage_3_plus_hh, married_couples_4_hh / total_married_couples * 100 AS percentage_4_hh, married_couples_5_hh / total_married_couples * 100 AS percentage_5_hh, married_couples_none_hh / total_married_couples * 100 AS percentage_none_hh FROM (SELECT state, married_couples_1_hh + married_couples_2_hh + married_couples_3_hh + married_couples_3_plus_hh + married_couples_4_hh + married_couples_5_hh + married_couples_none_hh AS total_married_couples FROM capstone_project.census) AS subquery")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:     
        state, percentage_1_hh, percentage_2_hh, percentage_3_hh, percentage_3_plus_hh, percentage_4_hh, percentage_5_hh, percentage_none_hh = row
        st.write(f"Percentage of married couples with different household sizes in {state}:, 1 household: {percentage_1_hh:.2f}%, 2 households: {percentage_2_hh:.2f}%, 3 households: {percentage_3_hh:.2f}%, 3+ households: {percentage_3_plus_hh:.2f}%, 4 households: {percentage_4_hh:.2f}%, 5 households: {percentage_5_hh:.2f}%, None: {percentage_none_hh:.2f}%")

    st.write("19. How many households fall below the poverty line in each state based on the power parity categories?")
    # Query 
    mysql_cursor.execute(f"SELECT state, \
        power_parity_less_45000 + power_parity_45000_90000 + power_parity_90000_150000 + power_parity_45000_150000 + power_parity_150000_240000 + power_parity_240000_330000 + power_parity_150000_330000 + power_parity_330000_425000 + power_parity_425000_545000 + power_parity_330000_545000 + power_parity_above_545000 AS total_below_poverty_line 
        FROM capstone_project.census")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:     
        state, total_below_poverty_line = row
        st.write(f"Number of households falling below the poverty line in {state}: {total_below_poverty_line}")
                         
    st.write("19. What is the overall literacy rate (percentage of literate population) in each state?")
    # Query 
    mysql_cursor.execute(f"SELECT state, (SUM(literate) / SUM(population)) * 100 AS literacy_rate FROM capstone_project.census GROUP BY state")
    data = mysql_cursor.fetchall()
    # Display output
    for row in data:     
        state, literacy_rate = row
        st.write(f"Overall literacy rate in {state}: {literacy_rate:.2f}%")

             
# Call the function to display population by district
display_data_streamlit()

# Close connections
mysql_cursor.close()
mysql_connection.close()
