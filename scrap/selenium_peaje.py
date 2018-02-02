import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

class Telepeaje_Scrap():
    """ scrap of telepeage to enquiry what is your balance """

    def __init__(self, url):
        self.url = url
    
    def enquiry(self, login, password, counterpart):

        driver = self.init_driver()
        msg = self.lookup(driver, login, password, counterpart)
        driver.quit()

        return msg

    def init_driver(self):
        binary = FirefoxBinary('/usr/bin/firefox')
        driver = webdriver.Firefox(
            firefox_binary=binary, executable_path="/home/franco/code/pbot/scrap/geckodriver")
        #driver = webdriver.Firefox()
        driver.wait = WebDriverWait(driver, 2)
        return driver

    def lookup(self, driver, login, password, counterpart):
        driver.get(self.url)
        msg_response = ''
        try:
            query = login
            pwd = password

            box_login = driver.wait.until(EC.presence_of_element_located(
                (By.NAME, "rtxt_login")))        
            box_login.send_keys(query)

            box_pwd = driver.wait.until(EC.presence_of_element_located(
                (By.NAME, "txt_password")))
            box_pwd.send_keys(pwd)

            button = driver.wait.until(EC.element_to_be_clickable(
                (By.NAME, "rbtn_aceptar")))
            res =  button.click()
            estado = driver.find_element_by_id('rgvw_estadocuenta')
            lookup_word = 'Asignado '
            ix_start = estado.text.find(lookup_word)
            estado = estado.text[ix_start + len(lookup_word):]

            ix_end = estado.find(' ')
            lookup_value = estado[:ix_end]
            #now find first space
            print('su saldo es : ' + str(lookup_value))
            msg_response = str(lookup_value)


        except TimeoutException:        
            msg_response = ""

        finally:
            return msg_response


#scrap = Telepeaje_Scrap(
#    "https://200.105.229.50/sgt_tele_quito/pages/inic/sgt_login.aspx")
#respuesta = scrap.enquiry('1103535223','frol1107','GSI2085')
#print(respuesta)
