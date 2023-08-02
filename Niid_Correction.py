# Import the required modules
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


# Main Function
def correct_regNoNiid():
    # Provide the email and password
    email = 'mayowaa'
    password = 'Lovely1'

    # Provide policy number
    policy = 'P/AG/PMI/23/TPC/2582669'#policy_number
    incorrect_regNo = 'WER758JZ1'#reg_number

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')

    # Provide the path of chromedriver present on your system.
    path = "C:/Users/itachi/Documents/chromedriver-win64"
    service = Service(executable_path=path)
    driver = webdriver.Chrome(options=options, service=service)
    # driver.set_window_size(1920, 1080)

    # Send a get request to the url
    driver.get('https://niid.org/default.aspx')
    time.sleep(0.5)

    # Finds the input box by name in DOM tree to send both
    # the provided email and password in it.
    username = driver.find_element(by="xpath",
                                   value='//div[@id="MainContent_UpdatePanel1"]/table/tbody/tr[2]/td[2]/span/input')
    username.send_keys(email)
    keycode = driver.find_element(by="xpath",
                                  value='//input[@class="riTextBox riEnabled Textbox_Large"]')
    keycode.send_keys(password)
    time.sleep(0.5)

    # Find the Login button and click on it.
    driver.find_element(by="xpath", value='//div[@id="MainContent_UpdatePanel1"]/table/tbody/tr[7]/td/a/input').click()
    time.sleep(0.5)

    # Find the Request(Endorsements) link and click on it.
    driver.find_element(by="xpath", value='//form/table/tbody/tr[7]/td['
                                          '2]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/div/table'
                                          '/tbody/tr[2]/td[2]/div/div/table/tbody/tr[2]/td['
                                          '2]/table/tbody/tr/td/table/tbody/tr/td[2]/a').click()
    time.sleep(0.5)

    # Find the Motor Vehicle Endorsement link and click on it.
    driver.find_element(by="xpath", value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table'
                                          '/tbody/tr/td/div/div/table/tbody/tr[2]/td['
                                          '2]/div/div/table/tbody/tr/td/table/tbody/tr/td[3]/a').click()
    time.sleep(0.5)

    # Entering the Policy number
    policy_number = driver.find_element(by="xpath",
                                        value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td[2]/span/input')
    policy_number.send_keys(policy)
    time.sleep(0.5)

    #Entering the incorrect Reg number
    reg_No = driver.find_element(by="xpath",
                                 value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[5]/td[2]/span/input')
    reg_No.send_keys(incorrect_regNo)
    time.sleep(0.5)

    driver.find_element(by="xpath", value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[6]/td/span/input').click()
    time.sleep(50)



correct_regNoNiid()
