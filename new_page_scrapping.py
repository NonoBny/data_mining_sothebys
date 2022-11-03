from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome(
    '/Users/nonobny/Desktop/Scolaire/ITC/Data_Mining_Sothebys/Selenium_Driver/chromedriver')  # Optional argument,
# if not specified will search path.

driver.get('https://www.sothebys.com/en/buy/auction/2022/monochrome-important-chinese-art')

# login in authentification
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='LinkedText']//a[text()='Log In']"))).click()
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='form-input-row ']//input[@id='email']"))).send_keys("noabenayoun1998@gmail.com")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='form-input-row-password \n                        ']//input[@id='password']"))).send_keys("Wuqu5520")
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='login-button-id']"))).click()

# access the list of results

hoverable_header = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='PageHeader-body']")))
ActionChains(driver)\
        .move_to_element(hoverable_header)\
        .perform()
hoverable_auction = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='PageHeader-body']//div[@class='NavigationItemTitle']//span[text()='Auctions']")))
ActionChains(driver)\
        .move_to_element(hoverable_auction)\
        .perform()

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='SothebysTopNavigationItem']//div[@class='NavigationLink']//a[text()='Results']"))).click()


