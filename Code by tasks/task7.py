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
