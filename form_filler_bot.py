import time
import random
import threading
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

themes = [
    1, 
    2, 
    3, 
    4, 
    5, 
    6, 
    8, 
    11
]

activities = [
    [8, 6, 4, 5, 3, 2, 1],
    [9, 10, 11],
    [12, 13, 14, 15, 16, 18, 19],
    [20, 21, 22, 23, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 43, 45, 46, 47, 48, 49, 50, 51, 52, 53],
    [54, 55],
    [57, 58, 59, 60, 61, 62, 63, 64],
    [66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 78, 79, 80, 81, 82, 83, 84, 85, 86],
    [128, 129, 130, 131]
]

# awc_number = 706871 # Karla Bk 1
awc_number = 706881 # Laghul 1

total_count = 0
successful_submission = 0
already_exists = 0
failed_attempt = 0
aborted = 0



# Start Firefox driver
driver = webdriver.Firefox()

# Go to website
url = 'https://poshanabhiyaan.gov.in/login'
driver.get(url)

# Credentials
username = 'mow&cd-2751103'
password = 'mow&cd-2751103'

# Wait for username field to be visible and enabled
user_field = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.NAME, "username"))
)


# Enter username
user_field.send_keys(username)  
pass_field = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.NAME, "password"))  
)

# Enter password 
pass_field.send_keys(password)

submit_btn = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
)
driver.execute_script("arguments[0].scrollIntoView();", submit_btn)

# Click login button
time.sleep(2)
submit_btn.click()
print("Logged In")

def fill_static_details():
    global adult_male, adult_female, child_male, child_female, submit_btn
    time.sleep(2)
    level_select = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "SelectLevel"))
    )
    level_select = Select(level_select)
    level_select.select_by_value("5")
    print("Level Selected")

    #############################################

    # Select AWC
    time.sleep(2)
    level_select = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "awc_center"))
    )
    level_select = Select(level_select)
    level_select.select_by_value(f"{awc_number}")
    print("AWC Selected")

    #############################################

    time.sleep(1)
    today = date.today()
    today_str = today.strftime("%Y-%m-%d")
    date1_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "SelectDateFrom"))
    )
    date1_input.send_keys(today_str) 

    # Set same date in second field 
    date2_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "SelectDateTo"))
    )
    date2_input.send_keys(today_str)
    print("dates entered")

    #############################################

    time.sleep(1)
    adult_male = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "CountAdultMale"))
    )

    adult_female = WebDriverWait(driver, 10).until(  
        EC.presence_of_element_located((By.NAME, "CountAdultFemale"))
    )

    child_male = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "CountChildMale"))  
    )

    child_female = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "CountChildFemale"))
    )

    submit_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]'))
    )

fill_static_details()

def fill_form(theme, activity):
    time.sleep(1)
    global total_count, successful_submission, already_exists, failed_attempt, aborted
    global adult_male, adult_female, child_male, child_female, submit_btn

    mean = 5  # Mean of the distribution
    std_dev = 2  # Standard deviation

    # Generate random numbers following a normal distribution
    rand1 = round(random.gauss(mean, std_dev))
    rand2 = round(random.gauss(mean, std_dev))
    rand3 = round(random.gauss(mean, std_dev))
    rand4 = round(random.gauss(mean, std_dev))

    # Ensure the generated numbers are within the desired range of 0 to 10
    rand1 = max(1, min(rand1, 9))
    rand2 = max(1, min(rand2, 9))
    rand3 = max(1, min(rand3, 9))
    rand4 = max(1, min(rand4, 9))

    driver.execute_script("arguments[0].value = '';", adult_male)
    driver.execute_script("arguments[0].value = '';", adult_female)
    driver.execute_script("arguments[0].value = '';", child_male)
    driver.execute_script("arguments[0].value = '';", child_female)

    # Enter random numbers
    adult_male.send_keys(str(rand1))  
    adult_female.send_keys(str(rand2))
    child_male.send_keys(str(rand3))
    child_female.send_keys(str(rand4))
    print("People entered")
    #####################
    time.sleep(1)
    theme_select_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "SelectTheme"))
    )
    theme_select = Select(theme_select_element)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, f"option[value='{theme}']"))
    )

    theme_select.select_by_value(f'{theme}')
    print("Theme Selected")
    
    #############################################

    # Select Activity
    time.sleep(2)
    level_select = Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "SelectActivity"))
    ))
    level_select.select_by_value(f"{activity}")
    print("Activity Selected")
    #############################################


    # Check if the submit button element exists
    if submit_btn:
        time.sleep(1)
        submit_btn.click()  # Clicking the button with the mouse cursor
        print(f"\n\n Application Submitted for THEME: {theme} and ACTIVITY: {activity} \n\n")
        total_count = total_count + 1

        try:
            time.sleep(2)
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.form-submitted-section p'))
            )
            print(f" {element.text} \n\n")
            if element.text == "Succesfully Submitted":
                successful_submission = successful_submission + 1
            elif element.text == "This activity participation data already exists on this interval!":
                already_exists = already_exists + 1
        except Exception as e:
            print(f"Error: {e}")
            print("\nElement not found after 10 seconds. Retrying...")
            failed_attempt = failed_attempt + 1
            raise e  # Raise the exception to report it to the main loop

        print(f"\n Total Count: {total_count} Total_Success: {successful_submission + already_exists} Success: {successful_submission} Already exists: {already_exists} Failed Attempt: {failed_attempt} Aborted: {aborted} \n")
        print("*"*10)
        print("\n\n")
    else:
        print("Submit button not found")


# Loop through themes and activities
for theme, activity_list in zip(themes, activities):
    for activity in activity_list:
        # Retry for a set number of times if something doesn't work
        max_retries = 100
        for _ in range(max_retries):
            try:
                fill_form(theme, activity)
                # If everything is successful, break out of the retry loop
                break
            except Exception as e:
                print(f"Error: {e}")
                print("Retrying...")
                fill_static_details()
                failed_attempt = failed_attempt + 1
                time.sleep(2)
        else:
            print(f"Failed after {max_retries} retries. Moving on to the next activity.")
            aborted = aborted + 1

# Close the browser
driver.quit()
print("*"*25)
print("\n FINAL STATS\n")
print(f"\n\n\n Total Count: {total_count} ")
print(f" Total Success: {successful_submission + already_exists} ")
print(f" Success: {successful_submission} ")
print(f" Already exists: {already_exists} ")
print(f" Failed Attempt: {failed_attempt} \n\n\n")
print(f" Aborted: {aborted} \n\n\n")
print("*"*25)