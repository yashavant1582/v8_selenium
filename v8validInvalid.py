import os  # Manage directories
import time  # Sleep delays
import csv  # Write login results to CSV
from datetime import datetime  # Timestamps
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
except Exception as e:
    print(f"❌ WebDriver Initialization Failed: {e}")
    exit(1)  # Exit script if WebDriver fails

# Define login test cases (Invalid & Valid)
test_accounts = [
    {"username": "invaliduser@example.com", "password": "WrongPassword123", "expected": "fail"},
    {"username": "meenakshi@ebrandz.com", "password": "Ser!@#1234567890", "expected": "pass"},
]

# Create necessary folders
screenshot_failed_folder = "Failed Logins"
screenshot_success_folder = "Successful Logins"
logs_folder = "Logs"
os.makedirs(screenshot_failed_folder, exist_ok=True)
os.makedirs(screenshot_success_folder, exist_ok=True)
os.makedirs(logs_folder, exist_ok=True)

# CSV file setup inside the "Logs" folder
csv_filename = os.path.join(logs_folder, "login_results.csv")
csv_header = ["Timestamp", "Username", "Status"]

# Create CSV file if it doesn't exist and add header
if not os.path.exists(csv_filename):
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)

# Loop through test cases
for account in test_accounts:
    try:
        # Navigate to the login page
        url = "https://v8dev.edeveloperz.com"
        print(f"🔄 Navigating to {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 10)  # Define wait for reuse

        # Wait for username and password fields
        username_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[formcontrolname="userid"]')))
        password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[formcontrolname="pass"]')))

        # Enter login credentials
        username = account["username"]
        password = account["password"]
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Locate and click login button
        signin = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-bg .btn-login")))
        print(f"🔑 Attempting Login with: {username}")
        signin.click()

        if account["expected"] == "fail":
            # Wait for failure message (adjust as per page response)
            time.sleep(3)  # Short delay for failure detection

            # Capture Screenshot on Failed Login
            screenshot_filename = os.path.join(screenshot_failed_folder, f"failed_login_{username.replace('@', '_').replace('.', '_')}.png")
            driver.save_screenshot(screenshot_filename)
            print(f"❌ Login Failed for {username} - Screenshot saved in '{screenshot_failed_folder}'")

            # Write failure to CSV inside "Logs" folder
            with open(csv_filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username, "Failed"])

            # Wait before next attempt
            print("⏳ Staying on login page for 5 seconds after failed login...")
            time.sleep(5)
            continue  # Skip to next test case

        # ✅ Login should be successful
        wait.until(EC.url_contains("globaldashboard"))
        print(f"✅ Login Successful for {username}")

        # Capture Screenshot on Successful Login
        screenshot_filename = os.path.join(screenshot_success_folder, f"successful_login_{username.replace('@', '_').replace('.', '_')}.png")
        driver.save_screenshot(screenshot_filename)
        print(f"✅ Screenshot after successful login saved in '{screenshot_success_folder}'")

        # Write success to CSV inside "Logs" folder
        with open(csv_filename, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), username, "Success"])

        # ✅ Wait for 10 seconds after loading the dashboard
        print("⏳ Waiting for 10 seconds before logging out...")
        time.sleep(10)

        # Locate and click profile icon
        print("👤 Clicking Profile Icon...")
        profile_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".profile-icon-login")))
        profile_icon.click()

        # Wait and click logout button
        print("🚪 Clicking Logout Button...")
        logout_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-hover-effects")))
        logout_button.click()

        # Wait for redirection to login page
        wait.until(EC.url_contains("v8dev.edeveloperz.com"))

        print("✅ Logout Successful! Redirected back to login page.")

        # ✅ Remain on the login page for 5 seconds before closing
        print("⏳ Staying on login page for 5 seconds...")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Error with {username}: {e}")

# Close the browser after all tests
print("🛑 Closing browser...")
driver.quit()
