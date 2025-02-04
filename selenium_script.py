import sys
import os
import time
import csv  # Write login results to CSV
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

# Retrieve login details from Flask
if len(sys.argv) < 3:
    print("Error: Missing username or password")
    sys.exit(1)

username = sys.argv[1]
password = sys.argv[2]

# Setup WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # Keep browser open
driver = webdriver.Chrome(service=service, options=options)

# CSV file setup inside the "Logs" folder
logs_folder = "Logs"
os.makedirs(logs_folder, exist_ok=True)
csv_filename = os.path.join(logs_folder, "login_results.csv")
csv_header = ["Timestamp", "Username", "Status"]

# Create CSV file if it doesn't exist and add header
if not os.path.exists(csv_filename):
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)

try:
    # Open login page
    url = "https://v8dev.edeveloperz.com"
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    # Enter login details
    username_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[formcontrolname="userid"]')))
    password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[formcontrolname="pass"]')))

    username_field.send_keys(username)
    password_field.send_keys(password)

    signin = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-bg .btn-login")))
    signin.click()

    # Check for successful login
    wait.until(EC.url_contains("globaldashboard"))
    print("✅ Login Successful!")

    # Take a screenshot after successful login
    os.makedirs("logs", exist_ok=True)
    screenshot_path = os.path.join("logs", f"{username}_success.png")
    driver.save_screenshot(screenshot_path)

    # Write success to CSV file
    with open(csv_filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username, "Success"])

    # **Logout functionality after successful login**

    # Wait for dashboard to load
    print("⏳ Waiting for 10 seconds to load dashboard...")
    time.sleep(10)

    # Locate and click profile icon (user's profile)
    print("👤 Clicking Profile Icon...")
    profile_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".profile-icon-login")))
    profile_icon.click()

    # Wait and click logout button
    print("🚪 Clicking Logout Button...")
    logout_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-hover-effects")))
    logout_button.click()

    # Wait for redirection back to the login page
    wait.until(EC.url_contains("v8dev.edeveloperz.com"))

    print("✅ Logout Successful! Redirected back to login page.")

    # Stay on login page for 5 seconds before closing the browser
    print("⏳ Staying on login page for 5 seconds before closing...")
    time.sleep(5)

except Exception as e:
    print(f"❌ Login Failed: {e}")

    # Save failure screenshot
    os.makedirs("logs", exist_ok=True)
    screenshot_path = os.path.join("logs", f"{username}_failed.png")
    driver.save_screenshot(screenshot_path)

    # Write failure to CSV file
    with open(csv_filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username, "Failed"])

finally:
    driver.quit()
