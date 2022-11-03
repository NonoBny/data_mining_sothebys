from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(
    '/Users/nonobny/Desktop/Scolaire/ITC/Data_Mining_Sothebys/Selenium_Driver/chromedriver')  # Optional argument,
# if not specified will search path.

driver.get('https://www.sothebys.com/en/buy/auction/2022/monochrome-important-chinese-art')

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='LinkedText']//a[text()='Log In']"))).click()



#WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element(By.XPATH,"//div[@class='form-input-row']//input[@id='email']").send_keys("noabenayoun1998@gmail.com")))
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element(By.XPATH,'//input[@id="password"]').send_keys("Wuqu5520")))
#WebDriverWait(driver, 20).until(EC.element_to_be_clickable(driver.find_element(By.XPATH,'//button[@id="login-button-id"]'))).click()


