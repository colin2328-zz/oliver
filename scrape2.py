from selenium import webdriver

driver = webdriver.Chrome()

driver.get('http://provider.bcbs.com/')

ele = driver.find_element_by_css_selector('.keyword-search')
ele.send_keys('lpc')

ele = driver.find_element_by_css_selector('#locationaddress')
ele.send_keys('San Francisco')
