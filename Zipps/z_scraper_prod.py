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

# define function to send text message
def send_message(message):
    recipient = '9365370533' + "@mms.att.net"
    email = "johnodonnell123@gmail.com"
    pw = "vcqe kxvm ruaw djhz"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email, pw) 
    server.sendmail(email, recipient, message)
    
# =============================================== HEAVEN HILL 17 SCRAPE ===============================================

# Get current date and time, format
dt = datetime.datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")

# Log start of scrape
print(f'\nStarting HH17 Scrape: {dt}')

# get urls for HH17
url = 'https://shop.zippsliquor.com/shop/product/heaven-hill-heritage-17-year/641a4c01e0370a2b71f3d32d?option-id=c0d41a9528378ea6f90b1abdbcdbb2b40773912dac4125a0a0a1b616df634616'

# Set up Selenium WebDriver, run headless so no window appears
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Navigate to the URL
driver.get(url)

# ------------- NAVIGATE TO STORE 

# Wait for the "change store" button to be clickable and get the button
change_store_xpath = "//button[@class='button ch-button']"
change_store_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, change_store_xpath)))

# Click the "change store" button to open the store selection modal
change_store_button.click()

# Wait for the store selection modal to appear and get the "select store" button
select_store_xpath = f"//div[@aria-label='Zipps Liquor - FM 1488']//button[@aria-label='Select business']"
select_store_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, select_store_xpath)))

# Click the "select store" button 
select_store_button.click()

# ------------- Check for Add to Cart Button 

# Get the text associated with the purchase button 
button_xpath = "//span[@class='mat-button-wrapper']/span"
hh_result = driver.find_elements(By.XPATH, button_xpath)           
hh_result = [i.text.strip() for i in hh_result]

# If buyable: send message
if len(hh_result) > 0:
    send_message('\n Heaven Hill Found')
    
print('- Success')

driver.quit()    
    
# Log end of scrape
dt = datetime.datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")
print(f'Finished HH17 Scrape: {dt}')






# =============================================== Zipps Whiskey Scrape ===============================================
    
    
    
# Log start of scrape
dt = datetime.datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")
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

            # ------------- NAVIGATE TO STORE 

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
            
            # Define the number of pages to scrape
            n_pages = 3
            
            # scrape the pages
            for page in range(n_pages):

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

                # move to next page
                next_button_xpath = f"//a[@class='button ch-btn nav-button'][last()]"
                next_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, next_button_xpath)))

                # Click the next page button
                next_button.click()

            # once pages are scraped, nagivate back to first page
            for page in range(n_pages - 1):

                # get the back button
                back_button_xpath = f"//a[@data-hook='search-results-previous-page']"
                back_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, back_button_xpath)))

                # Click the Back button 
                back_button.click()


            # print out that this attempt was successfull
            print(f'- {store}: Success')
            
            # if this was all successfull, break while loop and move to next store            
            break


        # if the program fails
        except Exception as e:
            
            # if final attempt, print the final failure message and just move on
            if attempt >= max_attempts:
                print(f'- {store}: Final Failure')

            # if not the final attempt, print a failure message and try again
            else:
                print(f'- {store}: Failed Attempt #{attempt}')

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
    records = pd.read_csv('Python/web_scraping/Zipps/records/zipps_records.csv')
    
except:
    records = pd.read_csv('records/zipps_records.csv')

# get new records
new_bottles = [i for i in df['bottles'].unique() if i not in records['bottles'].unique()]
    
# subset dataframe 
new = df[df['bottles'].isin(new_bottles)]

# get price drops
data_cols = ['bottles','store','price']
join_cols = ['bottles','store']
min_price_drop = 100
df2 = pd.merge(left= df[data_cols], right=records[data_cols],how='inner',on=join_cols, suffixes=('_current', '_records'))
df2 = df2[df2['price_current'] < (df2['price_records'] - min_price_drop)]

# append new records
records = pd.concat([records, new], ignore_index=True)

# write out records (local vs cron hack)
try:
    records.sort_values(by='ts', ascending=False).to_csv('Python/web_scraping/Zipps/records/zipps_records.csv',index=False)
    
except:
    records.sort_values(by='ts', ascending=False).to_csv('records/zipps_records.csv',index=False)

if len(new_bottles) > 0:
    
    string = ''
    
    # get dataframe of new bottles
    temp = df[df['bottles'].isin(new_bottles)]
    
    # for each new bottle, add name and price to string
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'- {a}: {b}\n'
    
    # send text message alert
    send_message('\nNew Addition to Zipps Records:' + f'\n{string}')

if len(df2) > 0:
    
    string = ''
    
    # for each new bottle, add name and price to string
    for a,b,c in zip(df2['bottles'].unique(), df2['price_records'].unique(), df2['price_current'].unique()):
        string += f'{a} price drop from {b} to {c}'
    
    # send text message alert
    send_message(string)
    
    
# Log end of scrape
dt = datetime.datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")
print(f'Finished Zipps Scrape: {dt} \n')





# =============================================== Bear Creek Whiskey Scrape ===============================================





# Log start of scrape
dt = datetime.datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")
print(f'Starting Bear Creek Scrape: {dt}')

# create empty dataframe to store scraped data 
df = pd.DataFrame()

# define max attempts when program fails (per store)
max_attempts = 2

# define counter for failed attempts
attempt = 1

while attempt <= max_attempts:

    # try becuase sometimes the chrome webdriver randomly fails
    try:

        # define url to start scrape
        url = 'https://shop.bearcreekspirits.com/shop/?subtype=whiskey&order=price+desc'   

        # create a dataframe to store the data from this store
        df_store = pd.DataFrame()

        # Set up Selenium WebDriver 
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the URL
        driver.get(url)

        # -------------------------- Age Verification -------------------------------

        # Age button 
        age_button_xpath = "//button[@class='age-check-yes']"
        age_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, age_button_xpath)))

        # Click the Change button to open the store selection modal
        age_button.click()

        n_pages = 3
        
        for page in range(n_pages):

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
            df_store['ts'] = dt

            # append the data from the store dataframe to the master dataframe
            df = pd.concat([df,df_store], ignore_index=True)

            # -------------------------- PAGE 2 -------------------------------    

            # move to next page
            next_button_xpath = f"//a[@class='button ch-btn nav-button'][last()]"
            next_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, next_button_xpath)))

            # Click the next page button
            next_button.click()


        # print out that this attempt was successfull
        print('- Success')
        
        break


    # if the program fails
    except Exception as e:

        # if this is the final attempt print the final failure message 
        if attempt >= (max_attempts - 1):
            print('- Final Failure')

        # if this isn't the final attempt print the a failure message and try again
        else:
            print(f'- Failed Attempt #{attempt}')

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
    records = pd.read_csv('Python/web_scraping/Zipps/records/bc_records.csv')
    
except:
    records = pd.read_csv('records/bc_records.csv')

# get new records
new_bottles = [i for i in df['bottles'].unique() if i not in records['bottles'].unique()]
  
# subset dataframe 
new = df[df['bottles'].isin(new_bottles)]

# append new records
records = pd.concat([records, new], ignore_index=True)

# write out records (local vs cron hack)
try:
    records.sort_values(by='ts',ascending=False).to_csv('Python/web_scraping/Zipps/records/bc_records.csv',index=False)
    
except:
    records.sort_values(by='ts',ascending=False).to_csv('records/bc_records.csv',index=False)

if len(new_bottles) > 0:
    
    string = ''
    
    # get dataframe of new bottles
    temp = df[df['bottles'].isin(new_bottles)]
    
    # for each new bottle, add name and price to string
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'- {a}: {b}\n'
    
    # send text message alert
    try:
        send_message('\nNew Addition to Bear Creek Records:' + f'\n{string}')
    except:
        print('- Bad Character in string')

    
    
# Log end of scrape
dt = datetime.datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")
print(f'Finished  Bear Creek Scrape: {dt}')



# =============================================== Apple Jacks Whiskey Scrape ===============================================




# Log start of scrape
dt = datetime.datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")
print(f'\nStarting Apple Jacks Scrape: {dt}')

# create empty dataframe to store scraped data from all the stores
df = pd.DataFrame()

# define max attempts when program fails (per store)
max_attempts = 2

# define counter for failed attempts
attempt = 1


# loop until the number of failed attempts reaches the max
while attempt <= max_attempts:

    # try becuase sometimes the chrome webdriver randomly fails
    try:

        # define url to start scrape
        url = 'https://applejacksliquor.com/shop?show-search=true&order=price+desc&type=Spirits&subtype=whiskey&style=tiles'   

        # create a dataframe to store the data from this store
        df_store = pd.DataFrame()

        # Set up Selenium WebDriver, run headless so no window appears
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to the URL
        driver.get(url)

        # -------------------------- Age Verification -------------------------------

        # Age button 
        age_button_xpath = "//button[@class='age-check-yes']"
        age_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, age_button_xpath)))

        # Click the Change button to open the store selection modal
        age_button.click()
        
        n_pages = 6
        
        for page in range(n_pages):
            
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
            df_store['ts'] = dt

            # append the data from the store dataframe to the master dataframe
            df = pd.concat([df,df_store], ignore_index=True)

            # move to next page
            next_button_xpath = f"//a[@class='button ch-btn nav-button'][last()]"
            next_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, next_button_xpath)))

            # Click the next page button
            next_button.click()


        # print out that this attempt was successfull
        print('- Success')
        
        break


    # if the program fails
    except Exception as e:

        # if this is the final attempt print the final failure message 
        if attempt >= max_attempts:
            print('- Final Failure')

        # if this isn't the final attempt print the a failure message and try again
        else:
            print(f'- Failed Attempt #{attempt}')

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
    records = pd.read_csv('Python/web_scraping/Zipps/records/aj_records.csv')
    
except:
    records = pd.read_csv('records/aj_records.csv')

# get new records
new_bottles = [i for i in df['bottles'].unique() if i not in records['bottles'].unique()]
  
# subset dataframe 
new = df[df['bottles'].isin(new_bottles)]

# append new records
records = pd.concat([records, new], ignore_index=True)

# write out records (local vs cron hack)
try:
    records.sort_values(by='ts',ascending=False).to_csv('Python/web_scraping/Zipps/records/aj_records.csv',index=False)
    
except:
    records.sort_values(by='ts',ascending=False).to_csv('records/aj_records.csv',index=False)
    
if len(new_bottles) > 0:
    
    string = ''
    
    # get dataframe of new bottles
    temp = df[df['bottles'].isin(new_bottles)]
    
    # for each new bottle, add name and price to string
    for a,b in zip(temp['bottles'].unique(),temp['price'].unique()):
        string += f'- {a}: {b} \n'
    
    # send text message alert
    try:
        send_message('\nNew Addition to Apple Jacks Records:' + f'\n{string}')
    except:
        print('- Bad Character in string')

    
    
# Log end of scrape
dt = datetime.datetime.today().strftime("%Y-%m-%d %I:%M:%S %p")
print(f'Finished Apple Jacks Scrape: {dt} \n\n ------------------------- \n\n')