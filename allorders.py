from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

import time
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys


# Set up the undetected Chrome browser
options = ChromeOptions()
options.add_argument("--headless")  # Run Chrome in headless mode if desired
browser = Chrome(options=options)

try:
    # Open the website
    print("Opening the website...")
    browser.get("https://writer.writersadmin.com/")

    # Log in to the website (replace with your actual login credentials)
    email = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "email")))
    password = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "password")))

    email.send_keys("mwacharomwanyolo@gmail.com")
    password.send_keys("John@001")

    login_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_button.click()

    print("Logged in successfully.")

    # Wait for the notification modal to appear (modify as needed)
    try:
        notification_modal = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-header')))
        close_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close')))
        ActionChains(browser).move_to_element(close_button).click().perform()
        WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-header')))
        print("Notification modal closed.")
    except TimeoutException as e:
        print(f"Notification modal not found: {e}. Proceeding with the script.")

    # Define the "retry_operation" function
    def retry_operation(operation, max_retries=10):
        for _ in range(max_retries):
            try:
                operation()
                return
            except TimeoutException as e:
                print(f"Timeout exception: {e}. Retrying...")
        print(f"Operation failed after {max_retries} retries.")

    # Click on the "Available" menu item
    print("Clicking on the 'Available' menu item...")
    available_menu_item = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//li[@id='side-menu-item-available-group']/a"))
    )
    available_menu_item.click()

    # Define the "New" link operation
    def click_new_link():
        new_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/orders/available/']"))
        )
        new_link.click()

    # Use the retry_operation function for clicking the "New" link
    print("Clicking on the 'New' link...")
    retry_operation(click_new_link)

    while True:
        # ... (your existing code to click on the top-most order)
        #     # Wait for the top-most order to be present
        print("Waiting for the top-most order to be present...")
        try:
            top_most_order = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//tr[@class='single-order']"))
            )
        except TimeoutException:
            print("No orders available. Refreshing...")
            browser.refresh()
            continue

        # Click on the top-most order

        print("Clicking on the top-most order...")
        top_most_order.click()
        print("Clicked on the top-most order...")

        # opens to a new page
        new_window_handle = browser.window_handles[1]
        browser.switch_to.window(new_window_handle)

        # Wait for the "Request / Bid" button to be clickable
        print("Waiting for the btn-take to be clickable...")
        btn_take = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='btn-take']"))
        )

        # Scroll into view before clicking
        browser.execute_script("arguments[0].scrollIntoView();", btn_take)

        btn_take.click()
        print("Clicked on the btn_take...")

        # Wait for the bidding modal to be present
        try:
            print("finding modal found")
            bidding_modal = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.ID, "modal-bidding-form"))
            )
        except TimeoutException:
            print("Bidding modal not found. Retrying...")
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            continue

        # Retry filling in the bid form
        description_input = WebDriverWait(bidding_modal, 30).until(
            EC.element_to_be_clickable((By.NAME, "description"))
        )

        def fill_bid_form():
            retries = 3
            while retries > 0:
                try:
                    description_input.clear()
                    description_input.send_keys(
                        "I have reviewed the provided instructions and understand the requirements. Rest assured, I am committed to delivering top-notch work, drawing upon my expertise from successfully completing prior tasks. Your project will be approached with the utmost professionalism and dedication to ensure exceptional quality. I am confident that my experience positions me well to meet and exceed your expectations. Kindly consider me."
                    )
                    print("Message filled")
                    return  # Exit the function on successful fill
                except StaleElementReferenceException:
                    print("StaleElementReferenceException. Retrying...")
                    retries -= 1

        fill_bid_form()

        # Locate and click the "Place bid" button
        try:
            place_bid_button = WebDriverWait(bidding_modal, 30).until(
                EC.element_to_be_clickable((By.ID, "btn-request"))
            )
            place_bid_button.click()
            print("Bid placed successfully!")

            # Close the new window handle
            browser.close()

            # Switch back to the original window
            browser.switch_to.window(browser.window_handles[0])

            # Refresh the page every 2 minutes while in the orders window
            refresh_interval = 15  # seconds
            print(f"Refreshing the page after {refresh_interval} seconds...")
            time.sleep(refresh_interval)
            browser.refresh()

        except TimeoutException:
            print("Place bid button not found. Retrying...")
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            continue

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    # Wait for 12 hours before closing the browser
    print("Waiting for 12 hours before closing the browser...")
    time.sleep(12 * 60 * 60)  # 12 hours in seconds

    print("Closing the browser...")
    browser.quit()


