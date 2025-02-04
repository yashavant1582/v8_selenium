import time  # Import time module for sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up WebDriver
try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
except Exception as e:
    print(f"❌ WebDriver Initialization Failed: {e}")
    exit(1)  # Exit script if WebDriver fails to start

try:
    # Navigate to the login page
    url = "https://v8dev.edeveloperz.com"
    print(f"🔄 Navigating to {url}")
    driver.get(url)

    wait = WebDriverWait(driver, 10)  # Define wait for reuse

    # Wait for username and password fields to be visible
    username_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[formcontrolname="userid"]')))
    password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[formcontrolname="pass"]')))

    # Enter login credentials
    username = "meenakshi@ebrandz.com"
    password = "Ser!@#1234567890"

    username_field.send_keys(username)
    password_field.send_keys(password)

    # Locate login button and ensure it is clickable
    signin = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-bg .btn-login")))

    print("🔑 Clicking Sign-In Button...")
    signin.click()

    # Wait for the page to redirect by checking the new URL
    wait.until(EC.url_contains("globaldashboard"))

    print("✅ Login Successful! Redirected to dashboard.")

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
    print(f"❌ Error: {e}")

finally:
    print("🛑 Closing browser...")
    driver.quit()
