from selenium import webdriver

driver = webdriver.Firefox()

driver.implicitly_wait(30)
driver.maximize_window()

driver.get('http://google.com')

# get the search textbox
search_field = driver.find_element_by_id("lst-ib")
search_field.clear()

# enter search keyword and submit
search_field.send_keys("Python Interview questions")
search_field.submit()

# get the list of elements which are displayed after the search
# on result page using find_elements_by_class_name  method
lists = driver.find_elements_by_class_name("_Rm")

# get the number of elements found
print("Found {} searches".format(str(len(lists))))

# iterate through each element and print the text that is
# name of the search

for listitem in lists:
    print(listitem)
# close the browser window
driver.quit()
