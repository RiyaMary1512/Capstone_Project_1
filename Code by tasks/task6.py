#Task 6: Database connection and data upload
#Data should be fetched from the mongoDB and to be uploaded to a relational database using python code . The table names should be the same as the file names without the extension.
#The primary key and foreign key constraints should be included in the tables wherever required.

import pymongo
import mysql.connector
import math

# Connect to MongoDB
mongo_client = pymongo.MongoClient('mongodb+srv://riyamary:mypassword@cluster0.21gljry.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
mongo_db = mongo_client['Capstone_Project']
mongo_collection = mongo_db['census']

# Connect to MySQL
mysql_connection = mysql.connector.connect(
    host="provide host name",
    user="provide user name",
    password="provide your password",
    database="Capstone_Project" # Your database name
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