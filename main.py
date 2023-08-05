# Import the required modules
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from Niid_Correction import correct_regNoNiid


# Main Function
def correct_regNo(policy_number, reg_number):
    # Provide the email and password
    email = 'mayowa_admin'
    password = 'Gbohunmi17'

    # Provide policy number
    policy = policy_number
    correct_regNo = reg_number

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')

    # Provide the path of chromedriver present on your system.
    path = "chromedriver-win64.exe"
    service = Service(executable_path=path)
    driver = webdriver.Chrome(options=options, service=service)
    # driver.set_window_size(1920, 1080)

    # Send a get request to the url
    driver.get('https://aginsuranceapplications.com/card/Index.aspx')
    time.sleep(0.5)
    # https: // auth.geeksforgeeks.org /

    # Finds the input box by name in DOM tree to send both
    # the provided email and password in it.
    username = driver.find_element(by="xpath",
                                   value='//div[@class="col-md-offset-2 col-md-4 center-block panel-primary"]/input[1]')
    username.send_keys(email)
    keycode = driver.find_element(by="xpath",
                                  value='//div[@class="col-md-offset-2 col-md-4 center-block panel-primary"]/input[2]')
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
    driver.find_element(by="xpath",
                        value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div['
                              '3]/div/select').click()
    time.sleep(0.5)

    # Find the fetch by policy button and click on it.
    driver.find_element(by="xpath",
                        value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div['
                              '3]/div/select/option[2]').click()
    time.sleep(0.5)

    #Check if the error box showed up and print the message

    # Finds the input box by name in DOM tree to send
    # the provided Policy in it.
    policy_number = driver.find_element(by="xpath",
                                        value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary '
                                              'panel-heading"]/div/div[2]/input')
    policy_number.send_keys(policy)

    # Find the Fetch button and click on it.
    driver.find_element(by="xpath",
                        value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary '
                              'panel-heading"]/div/div[3]/input').click()
    time.sleep(3)
    # Checking if the screen is loading
    cssValue = driver.find_element(by="xpath", value='//div[4]').value_of_css_property('display')
    print(cssValue)
    # Waiting for Screen to load before Updating the policy
    while cssValue == 'block':
        cssValue = driver.find_element(by="xpath", value='//div[4]').value_of_css_property('display')
        print(cssValue)
        print('waiting')
        time.sleep(3)
        if cssValue == 'none':
            print("done waiting")

    # Checking the value of the reg
    valueofReg = driver.find_element(by="xpath",
                                     value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div['
                                           '8]/div[3]/input').get_attribute("value")
    if valueofReg == "":
        print("There was an error try again later")
        driver.close()
        driver.quit()
    else:
        print("no error")

    # Editing the Reg Number
    driver.find_element(by="xpath",
                        value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div['
                              '8]/div[3]/input').clear()
    reg_No = driver.find_element(by="xpath",
                                 value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary '
                                       'panel-heading"]/div[8]/div[3]/input')
    reg_No.send_keys(correct_regNo)
    time.sleep(0.5)

    # Find the Save button and click on it.
    driver.find_element(by="xpath",
                        value='//div[@class="col-md-offset-3 col-md-8 center-block panel-primary panel-heading"]/div['
                              '14]/div/input').click()
    time.sleep(0.5)

    # Find the Yes button and click on it.
    driver.find_element(by="xpath",
                        value='//div[@class="ui-dialog ui-widget ui-widget-content ui-corner-all ui-draggable '
                              'ui-resizable ui-dialog-buttons"]/div/div/button').click()
    time.sleep(2)
    cssValue = driver.find_element(by="xpath", value='//div[4]').value_of_css_property('display')
    print(cssValue)
    # Waiting for Screen to load before Updating the policy
    while cssValue == 'block':
        cssValue = driver.find_element(by="xpath", value='//div[4]').value_of_css_property('display')
        print(cssValue)
        print('waiting')
        time.sleep(3)
        if cssValue == 'none':
            print("done waiting")

    # Quits the driver
    driver.close()
    driver.quit()
