# import dependencies
import selenium
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client


# Get current date and time
dt = datetime.datetime.today()
 
# Format datetime string
dt = dt.strftime("%Y-%m-%d %H:%M:%S")

print(f'Starting Seelbachs Scrape: {dt}')

# define max attempts when program fails
max_attempts = 3

# define counter for failed attempts
attempt = 1

while attempt <= max_attempts:

    # define url to start scrape
    url = 'https://seelbachs.com/products/13th-colony-double-oaked-bourbon'

    # try becuase sometimes the chrome webdriver randomly fails
    try:

        # Set up Selenium WebDriver 
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the URL
        driver.get(url)


        # -------------------------- PAGE 1 -------------------------------


        # Scrape the names of the bottles from the page 
        bottle_xpath = "//span[@id='AddToCartText-product-template']"
        bottles = driver.find_elements(By.XPATH, bottle_xpath)           
        bottle_list = [bottle.text for bottle in bottles]

        # if this was all successfull, increment the attempt variable so the loop will not repeat
        attempt = max_attempts + 1

        # print out that this attempt was successfull
        print('Success')


    # if the program fails
    except Exception as e:

        # if this is the final attempt print the final failure message 
        if attempt >= (max_attempts - 1):
            print('Final Failure')

        # if this isn't the final attempt print the a failure message and try again
        else:
            print(f'Failed Attempt #{attempt}')

            # increment attempt to mark this failure
            attempt += 1

    # Close the browser
    driver.quit()
        
        
results = bottle_list[0]


# check if there is any need for an alert    
if results == 'ADD TO CART':
    account_sid = 'ACdef9e07346d59d4824ccdad578cadd42'
    auth_token = 'c3bd88b76904b2f2368609d483968647'
    client = Client(account_sid, auth_token)
    

    message = client.messages.create(
      from_='+18667542325',
      body='Seelbachs Thirteenth Colony !!!!',
      to='+19365370533'
    )

# Format datetime string
# Get current date and time
dt = datetime.datetime.today()
dt = dt.strftime("%Y-%m-%d %H:%M:%S")
print(f'Finished Zipps Scrape: {dt} \n')