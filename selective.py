
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from undetected_chromedriver import Chrome, ChromeOptions
import time

# Set up the undetected Chrome browser
options = ChromeOptions()
browser = Chrome(options=options)

registered_emails = ['mwacharomwanyolo@gmail.com', 'example1@gmail.com', 'example2@gmail.com']
subjects = ['Management', 'Marketing', 'Biology', 'Physics', 'Finance', 'Law', 'Nursing', 'Technology', 'Education',
            'Business', 'Finance', 'Economics', 'Chemistry', 'Communications and Media', 'Ethics', 'Linguistics',
            'Medicine and Health', 'Nature', 'Political Science', 'Religion and Theology', 'Tourism', 'Others',
            'Project Management', 'Geography', 'criminal justice', 'I.T', 'FINANCE', 'HEALTHCARE', 'Programming',
            'Art (Fine arts, Performing arts)', 'International Relations', 'Music,anthropology',
            'Architecture and architectural designs', 'Accounting', 'Accounting and Finance', 'Environmental Science',
            'Statistics', 'Computer Science', 'Mathematics', 'Psychology', 'Sociology']

def check_user_is_registered(email):
    return email in registered_emails

def bid_on_order(order_element):
    # Click on the top-most order
    order_element.click()
    print("Clicked on the top-most order...")

    # Handle the bidding process in a new window
    try:
        new_window_handle = browser.window_handles[1]
        browser.switch_to.window(new_window_handle)

        # Wait for the "Request / Bid" button to be clickable
        print("Waiting for the btn-take to be clickable...")
        btn_take = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='btn-take']"))
        )
        browser.execute_script("arguments[0].scrollIntoView();", btn_take)
        btn_take.click()
        print("Clicked on the btn_take...")

        print("Finding modal...")
        bidding_modal = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "modal-bidding-form"))
        )

        # Filling out the bidding form
        print("Filling out the bidding form...")
        description_input = WebDriverWait(bidding_modal, 30).until(
            EC.element_to_be_clickable((By.NAME, "description"))
        )
        description_input.clear()
        description_input.send_keys(custom_bid_message
        )
        print("Message filled")

        # Placing the bid
        place_bid_button = WebDriverWait(bidding_modal, 30).until(
            EC.element_to_be_clickable((By.ID, "btn-request"))
        )
        place_bid_button.click()
        print("Bid placed successfully!")

        browser.close()  # Close the new window after bidding
        browser.switch_to.window(browser.window_handles[0])  # Switch back to the original window
    except Exception as e:
        print(f"Error during bidding: {e}")
        if len(browser.window_handles) > 1:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

def process_order_if_subject_matches(order_element, selected_subjects):
    try:
        print("Order details:", order_element.text)

        order_subject_element = order_element.find_element(By.XPATH, ".//td[@class='text-truncate'][2]")
        order_subject = order_subject_element.text.strip()

        if any(subject.lower() == order_subject.lower() for subject in selected_subjects):
            print(f"Selected subject found: '{order_subject}'. Proceeding with bidding...")
            bid_on_order(order_element)
        else:
            print(f"Skipping order with subject '{order_subject}' as it is not in the selected subjects.")
    except Exception as e:
        print(f"Error processing order: {e}")

def process_orders(selected_subjects):
    try:
        orders = WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tr[@class='single-order']"))
        )
        for order in orders:
            process_order_if_subject_matches(order, selected_subjects)
            time.sleep(1)
    except TimeoutException:
        print("No orders available. Refreshing...")

def retry_operation(operation, max_retries=10):
    for _ in range(max_retries):
        try:
            operation()
            return
        except TimeoutException as e:
            print(f"Timeout exception: {e}. Retrying...")
    print(f"Operation failed after {max_retries} retries.")

def click_new_link():
    new_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='/orders/available/']"))
    )
    new_link.click()

user_email = input('Enter your email: ')
# prompt for the user to enter their custom bid message
custom_bid_message = input('Enter your custom bid message: ')

if not check_user_is_registered(user_email):
    print('You are not registered. Please register or exit program execution.')
else:
    user_password = input('Enter your password: ')

    print('Available subjects:')
    for i, subject in enumerate(subjects, 1):
        print(f"{i}. {subject}")

    selected_subjects_indices = input('Enter the numbers of subjects you want to bid on (comma-separated): ').split(',')
    selected_subjects = [subjects[int(index) - 1] for index in selected_subjects_indices]

    print(f"You have selected the following subjects: {', '.join(selected_subjects)}")

    try:
        browser.get("https://writer.writersadmin.com/")

        email_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.NAME, "password")))

        email_input.clear()
        password_input.clear()

        email_input.send_keys(user_email)
        password_input.send_keys(user_password)

        login_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_button.click()

        print("Logged in successfully.")

        try:
            notification_modal = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-header')))
            close_button = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'close')))
            ActionChains(browser).move_to_element(close_button).click().perform()
            WebDriverWait(browser, 10).until_not(EC.visibility_of_element_located((By.CLASS_NAME, 'modal-header')))
            print("Notification modal closed.")
        except TimeoutException as e:
            print(f"Notification modal not found: {e}. Proceeding with the script.")

        print("Clicking on the 'Available' menu item...")
        available_menu_item = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@id='side-menu-item-available-group']/a"))
        )
        available_menu_item.click()

        print("Clicking on the 'New' link...")
        retry_operation(click_new_link)

        max_iterations = 100
        for _ in range(max_iterations):
            process_orders(selected_subjects)
            print("Refreshing for new orders...")
            time.sleep(30)  # Wait time before refreshing for new orders
            browser.refresh()

        print("Maximum iterations reached. Ending script.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        browser.quit()
