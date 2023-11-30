# import dependencies
import selenium
import pandas as pd
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import smtplib
import time


# Get current date and time
dt = datetime.datetime.today()
 
# Format datetime string
dt = dt.strftime("%Y-%m-%d %I:%M:%S %p")

print(f'\nStarting Zipps Scrape: {dt}')

# create empty dataframe to store scraped data from all the stores
df = pd.DataFrame()

# define list of stores to scrape
store_list = ['Zipps Liquor - FM 1488',
              'Zipps Liquor - Conroe HWY 242'
             ]

# define max attempts when program fails (per store)
max_attempts = 3

# loop through stores
for store in store_list:
      
    # define counter for failed attempts
    attempt = 1
   
    # loop until the number of failed attempts reaches the max
    while attempt <= max_attempts:

        # try becuase sometimes the chrome webdriver randomly fails
        try:
            
            # define url to start scrape
            url = 'https://shop.zippsliquor.com/shop/?subtype=whiskey&order=price+desc'   

            # create a dataframe to store the data from this store
            df_store = pd.DataFrame()
        
            # Set up Selenium WebDriver, run headless so no window appears
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)

            # Navigate to the URL
            driver.get(url)

            # -------------------------- NAVIGATE TO STORE -------------------------------

            # Wait for the Change button to be clickable and get the button
            change_store_xpath = "//button[@class='button ch-button']"
            change_store_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, change_store_xpath)))

            # Click the Change button to open the store selection modal
            change_store_button.click()

            # Wait for the store selection modal to appear and get the select store button
            select_store_xpath = f"//div[@aria-label='{store}']//button[@aria-label='Select business']"
            select_store_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, select_store_xpath)))

            # Click the select store button 
            select_store_button.click()


            # -------------------------- PAGE 1 -------------------------------


            # Scrape the names of the bottles from the page 
            bottle_xpath = "//div[@class='ch-product-name']"
            bottles = driver.find_elements(By.XPATH, bottle_xpath)           
            bottle_list = [bottle.text for bottle in bottles]

            # Scrape the prices from the page 
            price_xpath = "//span[@class='ch-single-product-price'] | //div[@class='price-range']"
            prices = driver.find_elements(By.XPATH, price_xpath)
            price_list = [price.text.split(' ')[0].replace('$','').replace(',','') for price in prices]

            # add the data to the store dataframe
            df_store['bottles'] = bottle_list
            df_store['price'] = price_list
            df_store['store'] = store
            df_store['ts'] = dt

            # append the data from the store dataframe to the master dataframe
            df = pd.concat([df,df_store], ignore_index=True)

            # -------------------------- PAGE 2 -------------------------------    

            # move to next page
            next_button_xpath = f"//a[@class='button ch-btn nav-button']"
            next_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, next_button_xpath)))

            # Click the next page button
            next_button.click()

            # Scrape the names of the bottles from the page 
            bottles = driver.find_elements(By.XPATH, bottle_xpath)           
            bottle_list = [bottle.text for bottle in bottles]

            # Scrape the prices from the page 
            prices = driver.find_elements(By.XPATH, price_xpath)
            price_list = [price.text.split(' ')[0].replace('$','').replace(',','') for price in prices]

            # add the data to the store dataframe
            df_store['bottles'] = bottle_list
            df_store['price'] = price_list
            df_store['store'] = store
            df_store['ts'] = dt

            # append the data from the store dataframe to the master dataframe
            df = pd.concat([df,df_store], ignore_index=True)

            # -------------------------- Navigate Back to Previous Page -------------------------------    

            # get the back button
            back_button_xpath = f"//a[@data-hook='search-results-previous-page']"
            back_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, back_button_xpath)))

            # Click the Back button 
            back_button.click()

            # if this was all successfull, increment the attempt variable so the loop will not repeat
            attempt = max_attempts + 1

            # print out that this attempt was successfull
            print(f'{store}: Success')


        # if the program fails
        except Exception as e:
            
            # if final attempt, print the final failure message and just move on
            if attempt >= (max_attempts - 1):
                print(f'{store}: Final Failure')

            # if not the final attempt, print a failure message and try again
            else:
                print(f'{store}: Failed Attempt #{attempt}')

                # increment attempt to mark this failure
                attempt += 1

    # Close the browser
    driver.quit()
    
    
# drop any bad data points
df = df[df['price'] != '']

# get the price
df['price'] = df['price'].astype(float)
              
# read in records (local vs cron hack)
try:
    records = pd.read_csv('Python/web_scraping/Zipps/records.csv')
    
except:
    records = pd.read_csv('records.csv')

# get new records
new_bottles = [i for i in df['bottles'].unique() if i not in records['bottles'].unique()]

# subset dataframe 
new = df[df['bottles'].isin(new_bottles)]

# append new records
records = pd.concat([records, new], ignore_index=True)

# write out records (local vs cron hack)
try:
    records.sort_values(by='ts',ascending=False).to_csv('Python/web_scraping/Zipps/records.csv',index=False)
    
except:
    records.sort_values(by='ts',ascending=False).to_csv('records.csv',index=False)

    

# TODO: ADD NEW RECORDS TO STRING?

# define string to text to phone if warranted
string = ''

#----------------- EH Taylor -------------------

temp = df[(df['bottles'].str.contains('colonel|EH Taylor|EH|Taylor', na=False, case=False)) 
              & (df['bottles'].str.contains('single|barrel|proof', na=False, case=False))
              & (~df['bottles'].str.contains('small|warehouse', na=False, case=False))
            ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'



#----------------- Caribou -------------------
temp = df[(df['bottles'].str.contains('caribou', na=False, case=False))
               & (df['price'] <= 60)
         ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'


#----------------- HH 17 -------------------
temp = df[(df['bottles'].str.contains('heritage', na=False, case=False)) 
                      & (df['bottles'].str.contains('hill', na=False, case=False))
         ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n $650 is your limit here'


#----------------- MWND -------------------
temp = df[(df['bottles'].str.contains('midwinter', na=False, case=False))
         ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'

#----------------- blantons -------------------
temp = df[(df['bottles'].str.contains('blanton', na=False, case=False))
              & (df['price'] <= 80)
         ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'

#----------------- ETL -------------------
temp = df[(df['bottles'].str.contains('elmer', na=False, case=False))
         ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'

#----------------- limited edition -------------------
temp = df[(df['bottles'].str.contains('roses', na=False, case=False)) 
                      & (df['bottles'].str.contains('limited', na=False, case=False))
         ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'

#----------------- Makers Cellar -------------------
temp = df[(df['bottles'].str.contains('maker', na=False, case=False)) 
                      & (df['bottles'].str.contains('cellar', na=False, case=False))
         ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'


#----------------- blood oath -------------------
temp = df[(df['bottles'].str.contains('blood oath', na=False, case=False))
         ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'

#----------------- coy -------------------
temp = df[(df['bottles'].str.contains('coy', na=False, case=False))
         ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n JDCH goes for 300-400 \n'

#----------------- weller -------------------
temp = df[(df['bottles'].str.contains('weller', na=False, case=False)) 
              & (~df['bottles'].str.contains('larue', na=False, case=False))
              & (df['price'] <= 100)
            ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'

#----------------- jack daniels -------------------
temp = df[(df['bottles'].str.contains('daniel', na=False, case=False)) 
                  & (df['bottles'].str.contains('jack', na=False, case=False))
                  & (df['bottles'] != 'Jack Daniels Year Old Tennessee Whiskey Batch 2')
                  & (~df['bottles'].str.contains('gold', na=False, case=False))
         ]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'

#----------------- jack daniels 10 year-------------------
temp = df[(df['bottles'] == 'Jack Daniels Year Old Tennessee Whiskey Batch 2')]
      
temp = temp[temp['price'] <= 100]

if len(temp) > 0:
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'{a}: {b} \n'

        
# ------ 

CARRIERS = {"att": "@mms.att.net"}
 
EMAIL = "johnodonnell123@gmail.com"
PASSWORD = "vcqe kxvm ruaw djhz"
 
def send_message(phone_number, carrier, message):
    recipient = phone_number + CARRIERS[carrier]
    auth = (EMAIL, PASSWORD)
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    server.sendmail(auth[0], recipient, message)
 
 
phone_number = '9365370533'
carrier = 'att'


# check if there is any need for an alert    
if len(string) > 0:
    
    send_message(phone_number, carrier, 'Check Zipps!!! \n' + string)
    print('<<>> Found <<>>: ' + string)


# Format datetime string
# Get current date and time
dt = datetime.datetime.today()
dt = dt.strftime("%Y-%m-%d %I:%M:%S %p")
print(f'Finished Zipps Scrape: {dt} \n')
