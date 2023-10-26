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
import time


# Get current date and time
dt = datetime.datetime.today()
 
# Format datetime string
dt = dt.strftime("%Y-%m-%d %I:%M:%S %p")

print(f'Starting Zipps Scrape: {dt}')

# create empty dataframe to store scraped data from all the stores
df = pd.DataFrame()

# define list of stores to scrape
store_list = ['Zipps Liquor - FM 1488',
              'Zipps Liquor - Conroe HWY 242',
#               'Zipps Liquor - Magnolia'
             ]

# define max attempts when program fails (per store)
max_attempts = 5

# loop through stores
for store in store_list:
      
    # define counter for failed attempts
    attempt = 1
   
    while attempt <= max_attempts:

        # try becuase sometimes the chrome webdriver randomly fails
        try:
            
            # define url to start scrape
            url = 'https://shop.zippsliquor.com/shop/?subtype=whiskey&order=price+desc'   

            # create a dataframe to store the data from this store
            df_store = pd.DataFrame()
        
            # Set up Selenium WebDriver 
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
            
                # if this is the final attempt print the final failure message 
            if attempt >= (max_attempts - 1):
                print(f'{store}: Final Failure')

            # if this isn't the final attempt print the a failure message and try again
            else:
                print(f'{store}: Failed Attempt #{attempt}')

                # increment attempt to mark this failure
                attempt += 1

    # Close the browser
    driver.quit()
        
df['price'] = df['price'].astype(float)        
        
#read in records
records = pd.read_csv('Python/web_scraping/Zipps/records.csv')

# get new records
new_bottles = [i for i in df['bottles'].unique() if i not in records['bottles'].unique()]

# subset dataframe 
new = df[df['bottles'].isin(new_bottles)]

# append new records
records = pd.concat([records, new], ignore_index=True)

# write out records
records.to_csv('Python/web_scraping/Zipps/records.csv',index=False)

## TODO: ADD NEW RECORDS TO STRING?

# define string to text to phone if warranted
string = ''

#----------------- EH Taylor -------------------

temp = df[(df['bottles'].str.contains('colonel|EH Taylor|EH|Taylor', na=False, case=False)) 
              & (df['bottles'].str.contains('single', na=False, case=False))
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
              & (df['price'] <= 100)
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
        string += f'{a}: {b} \n'

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

        
        
        
        

# check if there is any need for an alert    
if len(string) > 0:
    
    account_sid = 'ACdef9e07346d59d4824ccdad578cadd42'
    auth_token = 'c3bd88b76904b2f2368609d483968647'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
      from_='+18667542325',
      body=string,
      to='+19365370533'
    )
    
    print(string)


# Format datetime string
# Get current date and time
dt = datetime.datetime.today()
dt = dt.strftime("%Y-%m-%d %I:%M:%S %p")
print(f'Finished Zipps Scrape: {dt} \n')