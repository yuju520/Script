import argparse
import subprocess
import sys
import time

# Function to install missing libraries
def install_libraries():
    print("Installing required libraries...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "schedule", "selenium", "retry"]
    )
    print("Libraries installed successfully.")

# Attempt to import libraries, if not present, install them
try:
    import schedule
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from retry import retry
except ImportError as e:
    print(f"Error: {e}")
    install_libraries()
    # Re-import the libraries after installation
    import schedule
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from retry import retry

@retry(tries=5, delay=1.0, backoff=2.0, jitter=(1.0, 2.0))
def login_to_website(email, password, url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Initialize WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open target webpage
        driver.get(url)

        # Wait for login button to appear and click
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".login-button"))
        )
        login_button.click()

        # Fill in login form
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "login-account-name"))
        ).send_keys(email)

        driver.find_element(By.ID, "login-account-password").send_keys(password)

        # Click login button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        ).click()
        print("Login successful")

        # You can add further steps after login if needed

    finally:
        # Close the WebDriver session
        driver.quit()

def run_login(email, password, url):
    print("Logging in...")
    login_to_website(email, password, url)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Login to a website using Selenium.")
    parser.add_argument("email", type=str, help="Your email address")
    parser.add_argument("password", type=str, help="Your password")
    url = "https://linux.do"
    args = parser.parse_args()

    # Run the login function once immediately
    run_login(args.email, args.password, url)

    # Schedule the login function to run every day at a specific time
    schedule.every().day.at("08:00").do(run_login, args.email, args.password, url)

    # Keep the script running to allow the scheduled jobs to execute
    while True:
        schedule.run_pending()
        time.sleep(1)
