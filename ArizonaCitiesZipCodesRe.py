import time
import csv
import os
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from bs4 import BeautifulSoup
import pandas as pd

# List of cities with their names and zip codes
cities = [
    {"name": "Cameron", "zip": "86020"},
    {"name": "Camp Verde", "zip": "86322"},
    {"name": "Carefree", "zip": ""},
    {"name": "Casa Grande", "zip": "85223"},
    {"name": "Cashion", "zip": "85329"},
    {"name": "Catalina", "zip": ""},
    {"name": "Cave Creek", "zip": "85327"},
    {"name": "Central", "zip": "85531"},
    {"name": "Chambers", "zip": "86502"},
    {"name": "Chandler", "zip": ""},
    {"name": "Chandler Heights", "zip": ""},
    {"name": "Chinle", "zip": "86503"},
    {"name": "Chino Valley", "zip": "86323"},
    {"name": "Chloride", "zip": "86431"},
    {"name": "Cibecue", "zip": "85911"},
    {"name": "Cibola", "zip": ""},
    {"name": "Clarkdale", "zip": "86324"},
    {"name": "Clay Springs", "zip": "85923"},
    {"name": "Claypool", "zip": "85532"},
    {"name": "Clifton", "zip": "85533"},
    {"name": "Cochise", "zip": "85606"},
    {"name": "Colorado City", "zip": "86021"},
    {"name": "Concho", "zip": "85924"},
    {"name": "Congress", "zip": "85332"},
    {"name": "Coolidge", "zip": "85228"},
    {"name": "Cornville", "zip": "86325"},
    {"name": "Cortaro", "zip": "85652"},
    {"name": "Cottonwood", "zip": "86326"},
    {"name": "Crown King", "zip": "86343"}
]

def scrape_city(city):
    city_name = city["name"]
    city_zip = city["zip"]

    print(f"Processing data for city: {city_name} ({city_zip})")

    # Set up the Chrome WebDriver
    msedge_driver_path = r"C:\Users\shang\edgedriver_win64\msedgedriver.exe"  # Update with the actual path
    driver = webdriver.Edge(executable_path=msedge_driver_path)

    # Step 1: Visit the initial page with the list of programs
    url = f"https://programs.dsireusa.org/system/program?zipcode={city_zip}"
    driver.get(url)

    # Wait for the dynamic content to load
    time.sleep(5)

    # Get the page source after the dynamic content has loaded
    page_source = driver.page_source

    # Get the page source after the dynamic content has loaded
    page_source = driver.page_source

    # Step 2: Parse the page source with BeautifulSoup to get the links to individual program pages
    soup = BeautifulSoup(page_source, "html.parser")

    # Find the table containing the data
    table = soup.find("table")

    if table:
        # Find all rows in the table except the header row
        rows = table.find_all("tr")[1:]

        # Initialize an empty list to store the structured data
        structured_data = []

        # Extract data from each row
        for row in rows:
            cells = row.find_all(["th", "td"])
            link = cells[0].find("a")["href"]  # Get the link to the program page
            program_name = cells[0].text.strip()

            # Step 3: Visit the individual program page
            program_url = f"https://programs.dsireusa.org{link}"
            driver.get(program_url)

            # Wait for the dynamic content to load
            time.sleep(5)

            # Get the page source after the dynamic content has loaded
            program_page_source = driver.page_source

            # Step 4: Parse the program page to extract the data from the "program-detail wrapper" division
            program_soup = BeautifulSoup(program_page_source, "html.parser")
            program_detail_div = program_soup.find("div", {"class": "programOverview"})

            if program_detail_div:
                # Find all points in the "program-detail wrapper" division
                points = program_detail_div.find_all("li")

                # Create a dictionary to store the details of the current program
                program_details = {
                    "Program Name": program_name
                }

                # Extract and store the details in the dictionary
                for point in points:
                    parts = point.get_text(strip=True).split(":", 1)
                    if len(parts) == 2:
                        key, value = parts
                        program_details[key.strip()] = value.strip()

                # Append the dictionary to the structured_data list
                structured_data.append(program_details)
            else:
                print(f"No 'program-detail wrapper' division found on the program page for '{program_name}'.")

        # CSV file path to save the data
        csv_file_path = fr"{output_directory}\{city_name}_{city_zip}_program_details.csv"


        # Use pandas to normalize (flatten) the nested dictionaries
        flattened_data = pd.json_normalize(structured_data)

        # Write the flattened data to a CSV file
        flattened_data.to_csv(csv_file_path, index=False, encoding="utf-8")

        print(f"CSV file for city {city_name} ({city_zip}) has been created successfully.")
    else:
        print(f"No table found on the initial page for city {city_name} ({city_zip}).")


    # Close the browser
    driver.quit()

# Directory to save the CSV files
output_directory = r"C:\cdm data\ArizonaCitiesZipcode"

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Scrape cities concurrently
with ThreadPoolExecutor(max_workers=5) as executor:  # You can adjust max_workers as needed
    executor.map(scrape_city, cities)

print("All cities have been processed.")