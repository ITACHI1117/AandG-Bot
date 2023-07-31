# Import the required modules
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


# Main Function
if __name__ == '__main__':

    # Provide the email and password
    email = 'mayowa_admin'
    password = 'Gbohunmi17'

    #Provide policy number
    policy = 'P/AG/PMI/23/TPC/2582314'
    correct_regNo = 'LSR201HT'

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')

    # Provide the path of chromedriver present on your system.
    path = "C:/Users/itachi/Documents/chromedriver-win64"
    service = Service(executable_path=path)
    driver = webdriver.Chrome(options=options, service=service)
    # driver.set_window_size(1920, 1080)

    # Send a get request to the url
    driver.get('https://aginsuranceapplications.com/card/Index.aspx')
    time.sleep(0.5)
    # https: // auth.geeksforgeeks.org /

    # Finds the input box by name in DOM tree to send both
    # the provided email and password in it.
    username = driver.find_element(by="xpath", value='//div[@class="col-md-offset-2 col-md-4 center-block panel-primary"]/input[1]')
    username.send_keys(email)
    keycode = driver.find_element(by="xpath", value='//div[@class="col-md-offset-2 col-md-4 center-block panel-primary"]/input[2]')
    keycode.send_keys(password)

    # Find the signin button and click on it.
    driver.find_element(by="xpath", value='//div/input[3]').click()
    time.sleep(0.5)

    # Find the Policy operations button and click on it.
    driver.find_element(by="xpath", value='//div[@class="menu-list"]/ul/ul/div[4]/div/li/a').click()
    time.sleep(0.5)

    # Find the Update Policy button and click on it.
    driver.find_element(by="xpath", value='//div[@class="menu-list"]/ul/ul/div[4]/div[2]/ul/li[2]').click()
    time.sleep(0.5)

    # Find the Search by option and click on it.
    driver.find_element(by="xpath", value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div[3]/div/select').click()
    time.sleep(0.5)

    # Find the fetch by policy button and click on it.
    driver.find_element(by="xpath",value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div[3]/div/select/option[2]').click()
    time.sleep(0.5)

    # Finds the input box by name in DOM tree to send
    # the provided Policy in it.
    policy_number = driver.find_element(by="xpath", value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div/div[2]/input')
    policy_number.send_keys(policy)

    loader = driver.find_element(by="xpath", value='//div[4]').is_displayed()
    print(loader)

    # Find the Fetch button and click on it.
    driver.find_element(by="xpath",value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div/div[3]/input').click()
    time.sleep(0.5)

    loader = driver.find_element(by="xpath", value='//div[4]').is_displayed()
    print(loader)

    if loader:
        time.sleep(15)
    elif loader == False:
        time.sleep(0.5)


    driver.find_element(by="xpath", value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div[8]/div[3]/input').clear()
    reg_No = driver.find_element(by="xpath", value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div[8]/div[3]/input')
    reg_No.send_keys(correct_regNo)
    time.sleep(0.5)

    # Find the Save button and click on it.
    driver.find_element(by="xpath", value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div[14]/div/input').click()
    time.sleep(0.5)

    # Find the Save button and click on it.
    driver.find_element(by="xpath", value='//div[@class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-draggable ui-resizable ui-dialog-buttons"]/div/div/button').click()
    time.sleep(5)

    if loader:
        time.sleep(15)
    elif loader == False:
        time.sleep(0.5)

    close_button = driver.find_element(by="xpath", value='//div[@class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-draggable ui-resizable ui-dialog-buttons"]/div/div/button[1]').is_displayed()
    print(close_button)
    button = driver.find_element(by="xpath", value='//div[@class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-draggable ui-resizable ui-dialog-buttons"]/div/div/button/span')
    button.click()
    time.sleep(35)
    print("Done✅")




    # Quits the driver
    driver.close()
    driver.quit()
