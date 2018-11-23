import re
from pyquery import  PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

def search():
    # 判断搜索框和搜索按钮是否加载成功
    try:
        browser.get('https://www.tmall.com/')
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mq'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'#mallSearch > form > fieldset > div > button'))
        )
        input.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                '#content > div > div.ui-page > div > b.ui-page-skip > form'))
        )
        return total[0].text

    except TimeoutError:
        return search()

def get_product():
    #获取商品信息
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#J_ItemList .product  .product-iWrap'))
    )
    html = browser.page_source
    doc = pq(html, parser="html")
    items = doc('#J_ItemList .product  ').items()
    for item in items:
        # print(item)
        product = {
            'title': item.find('.productTitle a').text(),
            'image': 'https:{0}'.format(item('.product .product-iWrap .productImg-wrap a img').attr('src')),
            'price': item.find('.productPrice').text().replace('\n',''),
            'shop': item.find('.productShop .productShop-name').text(),
            'productStatus': item.find('.productStatus span em').text()
        }
        print(product)
def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))
    print(total)
    get_product()

if __name__ == '__main__':
    main()