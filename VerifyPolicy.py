# Import the required modules
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from Niid_Correction import correct_regNoNiid

# Main Function


def verify_policy(certi_No,platform_data):
    # Provide the email and password
    email = platform_data[1]
    password = platform_data[2]

    # Provide policy number
    certi = certi_No

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')

    # Provide the path of chromedriver present on your system.
    path = (r"chromedriver.exe")
    service = Service(executable_path=path)
    driver = webdriver.Chrome(options=options, service=service)
    # driver.set_window_size(1920, 1080)

    # Send a get request to the url
    driver.get(platform_data[0])
    time.sleep(0.2)

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
    time.sleep(0.2)

    # Find the Utility button and click on it.
    driver.find_element(
        by="xpath", value='//div[@class="menu-list"]/ul/ul/div[6]/div/li/a').click()
    time.sleep(0.2)

    # The policy button location is different for both platforms
    # verifying which platform has been selected to check where the button is for that particular platform
    if platform_data[3] == 'Scratch Card Platform':
        # Find the Verify Policy button and click on it.
        driver.find_element(
            by="xpath", value='//div[@class="menu-list"]/ul/ul/div[6]/div[2]/ul/li[4]').click()
        time.sleep(0.2)
    else:
        # Find the Verify Policy button and click on it.
        driver.find_element(
            by="xpath", value='//div[@class="menu-list"]/ul/ul/div[6]/div[2]/ul/li[1]').click()
        time.sleep(0.2)


    # Find the SearchBy (select attribute) option and click on it.
    driver.find_element(
        by="xpath", value='//div[@class="col-md-offset-3 col-md-4 center-block panel-primary panel-heading"]/select').click()
    time.sleep(0.2)

    # Find the fetch by policy button and click on it.
    driver.find_element(
        by="xpath", value='//div[@class="col-md-offset-3 col-md-4 center-block panel-primary panel-heading"]/select/option[3]').click()
    time.sleep(0.2)



    # Finds the input box by name in DOM tree to send
    # the provided certificate number in it.
    certi_number = driver.find_element(
        by="xpath", value='//div[@class="col-md-offset-3 col-md-4 center-block panel-primary panel-heading"]/input')
    certi_number.send_keys(certi)

    # Find the Verify button and click on it.
    driver.find_element(by="xpath",
                        value='//div[@class="col-md-offset-3 col-md-4 center-block panel-primary panel-heading"]/div[5]/div/input').click()
    time.sleep(1)

    # Checking if the screen is loading
    cssValue = driver.find_element(
        by="xpath", value='//div[4]').value_of_css_property('display')
    print(cssValue)

    # Waiting for Screen to load before Updating the policy
    while cssValue == 'block':
        cssValue = driver.find_element(
            by="xpath", value='//div[4]').value_of_css_property('display')
        print(cssValue)
        print('Loading...')
        time.sleep(1.2)
        if cssValue == 'none':
            print("Done Loading✅")


    # Check if the error box showed up and print the message
    errobox_value = driver.find_element(
        by="xpath",
        value='//div[@class="col-md-offset-3 col-md-4 center-block panel-primary panel-heading"]/span').text

    if errobox_value == '':
        print("policy found")
    else:
        print(f"error message ={errobox_value}")
        return errobox_value

    time.sleep(0.2)


    # Find the records table heading which is Record
    Header = driver.find_element(
        by="xpath", value='//div[@class="col-md-offset-3 col-md-10 center-block panel-primary panel-heading"]/div').text
    print(Header)

    time.sleep(0.2)

    # Finds the Text on the table
    titles = driver.find_elements(
        by="xpath", value='//div[@class="col-md-offset-3 col-md-10 center-block panel-primary panel-heading"]/div[2]/table/tbody/tr/th')
    subtitles = driver.find_elements(
        by="xpath", value='//div[@class="col-md-offset-3 col-md-10 center-block panel-primary panel-heading"]/div[2]/table/tbody/tr[2]/td')

    Ttitle = []
    SubTtitle = []

    # Iterating over the texts on the table head and appending to the Title
    for title in titles:
        Ttitle.append(title.text)
    # Iterating over the texts on the table row and appending to the Subtitle
    for subtitle in subtitles:
        SubTtitle.append(subtitle.text)

    # Creating a new array and joinig both the Title array and the SubTitle array together
    new = [f"{Ttitle[i]} - {SubTtitle[i]}" for i in range(len(Ttitle))]

    print("Gotten the data")
    # Quits the driver
    driver.close()
    driver.quit()

    return new
