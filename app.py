from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from geopy.geocoders import Nominatim
print("Starting Flask app...")

app = Flask(__name__)
CORS(app)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json
    search_term = data.get("query")

    if not search_term:
        return jsonify({"error": "Missing query"}), 400

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.google.com/maps")
    time.sleep(3)

    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.clear()
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.ENTER)
    time.sleep(5)

    results = driver.find_elements(By.CLASS_NAME, "hfpxzc")[:5]
    scraped_data = []

    geolocator = Nominatim(user_agent="map_scraper")

    for res in results:
        try:
            res.click()
            time.sleep(4)

            try:
                name = driver.find_element(By.CLASS_NAME, "DUwDvf").text
            except:
                name = "N/A"

            try:
                address = driver.find_element(By.CLASS_NAME, "Io6YTe").text
            except:
                address = "N/A"

            try:
                rating = driver.find_element(By.CLASS_NAME, "F7nice").text
            except:
                rating = "N/A"

            try:
                reviews = driver.find_element(By.CLASS_NAME, "UY7F9").text
            except:
                reviews = "N/A"

            try:
                phone = driver.find_elements(By.CLASS_NAME, "UsdlK")[0].text
            except:
                phone = "N/A"

            # Get Lat/Lng from address
            try:
                location = geolocator.geocode(address)
                lat = location.latitude if location else None
                lng = location.longitude if location else None
            except:
                lat = None
                lng = None

            scraped_data.append({
                "name": name,
                "address": address,
                "phone": phone,
                "rating": rating,
                "reviews": reviews,
                "lat": lat,
                "lng": lng
            })
        except:
            continue

    driver.quit()
    return jsonify(scraped_data)
if __name__ == "__main__":
    app.run(debug=True)
