import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def find_status(license_number):
    print(license_number)
    try:
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        browser.get(f'https://secure.lni.wa.gov/verify/Detail.aspx?LIC={license_number}')

        field = browser.find_element(By.CSS_SELECTOR, 'span#StatusDescription')
        status = field.get_attribute("innerHTML")
        status = ((re.sub(r'<\/?strong>', ' ', status)).split('<br>'))[0].strip()
        browser.quit()
    except:
        return 'Not valid number!'
    return status

def validate_file_extension(value):
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.jpg','.jpeg','.png']
  if not ext in valid_extensions:
    return False