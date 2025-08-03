from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import csv
import time
import os

# Setup Chrome driver
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Optional: Headless mode if you don't want the browser to open
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# Create CSV if not exists
filename = "companies.csv"
if not os.path.exists(filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Search Term", "Name", "Address", "Phone Number", "Rating", "Number of Reviews"])

try:
    # Open Google Maps
    driver.get("https://www.google.com/maps")
    wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))

    while True:
        search_term = input("Enter a search term (or type 'exit' to quit): ")
        if search_term.lower() == 'exit':
            break

        # Enter search
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.ENTER)

        # Wait for results to load
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc")))  # current card class
        except TimeoutException:
            print("Timeout while waiting for results.")
            continue

        time.sleep(3)  # Let it fully render

        # Get top 3 results
        results = driver.find_elements(By.CLASS_NAME, "hfpxzc")[:3]
        all_data = []

        for res in results:
            # Click on the result to load details
            try:
                res.click()
                time.sleep(3)  # wait for sidebar to load
            except:
                continue

            # Now extract info from the sidebar
            try:
                name = driver.find_element(By.CLASS_NAME, "DUwDvf").text
            except NoSuchElementException:
                name = "N/A"

            try:
                address = driver.find_element(By.CLASS_NAME, "Io6YTe").text
            except NoSuchElementException:
                address = "N/A"

            try:
                rating = driver.find_element(By.CLASS_NAME, "F7nice").text
            except NoSuchElementException:
                rating = "N/A"

            try:
                reviews = driver.find_element(By.CLASS_NAME, "UY7F9").text.split()[0]
            except NoSuchElementException:
                reviews = "N/A"

            try:
                phone_elem = driver.find_elements(By.CLASS_NAME, "UsdlK")[0]
                phone = phone_elem.text if phone_elem else "N/A"
            except:
                phone = "N/A"

            print(f"Scraped: {name}, {address}, {phone}, {rating}, {reviews}")
            all_data.append([search_term, name, address, phone, rating, reviews])

        # Save to CSV
        with open(filename, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(all_data)
        print("Saved to CSV!")

except Exception as e:
    print("Error:", e)
finally:
    driver.quit()
