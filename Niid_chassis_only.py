# Import the required modules
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service

# Main Function


def correct_chassisNo_Niid(policy_number, reg_number, chassis_number):
    # Provide the email and password
    email = 'mayowaa'
    password = 'Lovely1'
    comapny_email = 'info@aginsuranceplc.com'

    # Provide policy number
    policy = policy_number  # policy_number
    correct_regNo = reg_number
    correct_chassisNo = chassis_number

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    # options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')

    # Provide the path of chromedriver present on your system.
    path = (r"chromedriver.exe")
    service = Service(executable_path=path)
    driver = webdriver.Chrome(options=options, service=service)
    # driver.set_window_size(1920, 1080)

    # Send a get request to the url
    driver.get('https://niid.org/default.aspx')
    time.sleep(0.2)

    # Finds the input box by name in DOM tree to send both
    # the provided email and password in it.
    username = driver.find_element(by="xpath",
                                   value='//div[@id="MainContent_UpdatePanel1"]/table/tbody/tr[2]/td[2]/span/input')
    username.send_keys(email)
    keycode = driver.find_element(by="xpath",
                                  value='//input[@class="riTextBox riEnabled Textbox_Large"]')
    keycode.send_keys(password)
    time.sleep(0.8)

    # Find the Login button and click on it.
    driver.find_element(
        by="xpath", value='//div[@id="MainContent_UpdatePanel1"]/table/tbody/tr[7]/td/a/input').click()
    time.sleep(0.8)

    # Find the Request(Endorsements) link and click on it.
    driver.find_element(by="xpath", value='//form/table/tbody/tr[7]/td['
                                          '2]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/div/div/table'
                                          '/tbody/tr[2]/td[2]/div/div/table/tbody/tr[2]/td['
                                          '2]/table/tbody/tr/td/table/tbody/tr/td[2]/a').click()
    time.sleep(0.8)

    # Find the Motor Vehicle Endorsement link and click on it.
    driver.find_element(by="xpath", value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table'
                                          '/tbody/tr/td/div/div/table/tbody/tr[2]/td['
                                          '2]/div/div/table/tbody/tr/td/table/tbody/tr/td[3]/a').click()
    time.sleep(0.8)

    # Entering the Policy number
    policy_Number = driver.find_element(by="xpath",
                                        value='//form/table/tbody/tr[7]/td['
                                              '2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[4]/td['
                                              '2]/span/input')
    policy_Number.send_keys(policy)
    time.sleep(0.2)

    # Entering the incorrect Reg number
    reg_No = driver.find_element(by="xpath",
                                 value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table'
                                       '/tbody/tr[5]/td[2]/span/input')
    reg_No.send_keys(correct_regNo)
    time.sleep(0.8)

    # Finding the search Button and clicking on it
    driver.find_element(by="xpath",
                        value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr['
                              '6]/td/span/input').click()
    time.sleep(0.8)

    # Identify the email text box
    email_txt = driver.find_element(by="xpath", value="//form/table/tbody/tr[7]/td["
                                                      "2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[12]/td["
                                                      "2]/input")

    # Fetch the value property of the email
    value_info = email_txt.get_attribute("value")
    print(value_info)

    # Changing the value property of the email if it does not contain '@'
    if '@' in value_info:
        print("Email is verified")
    else:
        print("Invalid email")
        driver.find_element(by="xpath", value="//form/table/tbody/tr[7]/td["
                                              "2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[12]/td["
                                              "2]/input").clear()
        new_email = driver.find_element(by="xpath",
                                        value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table'
                                              '/tbody/tr[12]/td[2]/input')
        new_email.send_keys(comapny_email)
        time.sleep(0.8)

    # Editing the Chassis Number
    driver.find_element(by="xpath",
                        value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr['
                              '16]/td[2]/input').clear()
    time.sleep(0.2)
    driver.find_element(by="xpath",
                        value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr['
                              '16]/td[2]/input').send_keys(
        correct_chassisNo)
    time.sleep(0.2)

    # Finding the change button and clicking on it
    driver.find_element(by="xpath",
                        value='//form/table/tbody/tr[7]/td[2]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr['
                              '30]/td/span/input').click()
    time.sleep(1)

    # Checking for the alert and clicking on it
    alert = driver.switch_to.alert
    alert.accept()

    # closing the Page
    driver.close()
    driver.quit()
