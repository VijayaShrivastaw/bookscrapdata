from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import mysql.connector  as mysql

conn = mysql.connect(
    user = "root",
    password="Root@1234",
    host="localhost",
    database = "booksData"
)
if conn.is_connected :
    print("connection successfully connected") 
cursor = conn.cursor()



driver = webdriver.Chrome()
driver.maximize_window()
driver.get('https://books.toscrape.com/?utm_source=chatgpt.com')
numbers = driver.find_elements(By.XPATH, value='//form[@class="form-horizontal"]//strong')
page_num = int(numbers[-1].text)

for page in range(1, page_num+1):
    if page == 1:
        url = 'https://books.toscrape.com/?utm_source=chatgpt.com'
    else :
        url = f'https://books.toscrape.com/catalogue/page-{page}.html'
    driver.get(url)
    product_data = driver.find_elements(By.XPATH , value="//article[@class='product_pod']")
    for product in product_data:
        # print(product.text)
        book_title = product.find_element(By.XPATH, './/h3/a').get_attribute('title')
        book_price = driver.find_element(By.XPATH, value='//p[@class="price_color"]').text
    
        star_ratings = driver.find_element(By.XPATH, "//p[contains(@class,'star-rating')]")

    
        classes = star_ratings.get_attribute("class")   # e.g. "star-rating Three"
        rating = classes.replace("star-rating", "").strip()
        
        sql = "insert into books (title,price,rating) values (%s,%s,%s)"
        value = (book_title,book_price,rating)

        cursor.execute(sql,value)
        conn.commit()
        print(f"Inserted: {book_title} | {book_price} | {rating}")
        
        
time.sleep(3)
cursor.close()
conn.close()
driver.quit()