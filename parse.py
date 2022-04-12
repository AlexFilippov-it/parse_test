from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

driver = webdriver.Chrome(ChromeDriverManager().install())

data = []

driver.get("https://dveri.com/catalog/dveri-mezhkomnatnyye?page=1")

wait = WebDriverWait(driver, 10)

elements_xpath = '//div[@class=" products__item "]/a[@class="card"]'
# Wait for emelents to load
wait.until(EC.element_to_be_clickable((By.XPATH, elements_xpath)))

num_elements = len(driver.find_elements(By.XPATH, elements_xpath))
ac = ActionChains(driver)

for i in range(num_elements):
    # Wait until elements are clickable
    wait.until(EC.element_to_be_clickable((By.XPATH, elements_xpath)))
    # Get all elements and select only the i-th one
    element = driver.find_elements(By.XPATH, elements_xpath)[i]
    # Click the element with the offset from center to actually go to the other page
    ac.move_to_element(element).move_by_offset(0, 100).click().perform()

    # Here do whatever has to be done on a specific webpage
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title = soup.find('h1', class_='product__title').text
    category = soup.find('ul', class_='breadcrumbs__list scroll-hidden').text
    colour = soup.find('div', class_='product__collection').text
    price = soup.find('div', class_='product__price').text
    #size = soup.find('div', {"class": "product__size-list"}).text
    picture = soup.find('div', class_='product__img-wrap')
    describe = soup.find('li', class_='tabs__content-item active').text
    documents = soup.find('div', class_='product__property')

    elements_mirror = '//div[@class="product__size-list"]/a'

    mirror = len(driver.find_elements(By.XPATH, elements_mirror))
    ac = ActionChains(driver)
    mirror = driver.find_elements(By.XPATH, elements_mirror)[i]
    ac.move_to_element(mirror).click().perform()
    for i in range(mirror):
        if elements_mirror is not None:
            print("Нет элементов")

        data.append([title, category, colour, price, size, picture, describe, documents])

        time.sleep(1)
        # Go back to the previous page
        driver.execute_script("window.history.go(-1)")




header = ['title', 'category', 'colour', 'price', 'size', 'picture', 'describe', 'documents']
df = pd.DataFrame(data, columns=header)
df.to_csv('/Users/apple/Documents/QA/pageobject/bravo_parse.csv', sep=';', encoding='utf8')