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


