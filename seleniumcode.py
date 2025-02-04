from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Start the WebDriver using webdriver-manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Load the login page (use a file:// URL for local HTML files)
    login_page_path = "/home/yashavant/Music/Python/PythonxSelenium/login.html"  # Update this path as needed
    driver.get(f"file://{login_page_path}")

    # Wait for the username field to be present
    wait = WebDriverWait(driver, 10)  # Explicit wait for elements
    username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
    password_field = driver.find_element(By.ID, "password")

    # Enter the username and password
    username_field.send_keys("test")
    password_field.send_keys("test_123")

    # Submit the form
    password_field.send_keys(Keys.RETURN)

    # Wait for the message element to be visible
    message_element = wait.until(EC.visibility_of_element_located((By.ID, "message")))
    message_text = message_element.text

    # Validate the result message
    if "Login successful!" in message_text:
        print("Test Passed: Login successful!")
    elif "Kindly check login details." in message_text:
        print("Test Failed: Incorrect login details.")
    else:
        print("Test Result: Unexpected message:", message_text)

except Exception as e:
    print("An error occurred:", str(e))

finally:
    # Close the browser
    time.sleep(2)  # Optional delay to observe the browser before it closes
    driver.quit()