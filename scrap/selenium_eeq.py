import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
from datetime import datetime


class eeq_scrap():
    """ scrap of telepeage to enquiry what is your balance """

    def __init__(self, url):
        self.url = url
    
    def enquiry(self,counterpart):
        
        start_time = datetime.now()
        
        driver = self.init_driver()
        msg = self.lookup(driver, counterpart)
        driver.quit()
        
        c = datetime.now() - start_time
        print(c.seconds)
        return msg

    def init_driver(self):
        binary = FirefoxBinary('/usr/bin/firefox')
        driver = webdriver.Firefox(
            firefox_binary=binary, executable_path="/home/franco/code/pbot/scrap/geckodriver")
        #driver = webdriver.Firefox()
        driver.wait = WebDriverWait(driver, 2)
        return driver

    def lookup(self, driver, counterpart):
        driver.get(self.url)
        msg_response = ''
        try:

            select = Select(driver.find_element_by_id('vTIPODOCUMENTO'))
            select.select_by_value('3')

            box_login = driver.wait.until(EC.presence_of_element_located(
                (By.NAME, "vNRODATO")))
            box_login.send_keys(counterpart)      
          
            button = driver.wait.until(EC.element_to_be_clickable(
                (By.NAME, "BUTTON1")))
            res =  button.click()

            saldo = driver.wait.until(EC.visibility_of_element_located((By.ID, 'span_W0021vGRILLAMONTO_0001')))
            print('saldo')

            #falta el otro click y traer la fecha           
            msg_response = saldo.text

        except TimeoutException:        
            msg_response = ""
        except Exception as e1:
            print(e1)

        finally:
            return msg_response


scrap = eeq_scrap(
    "http://190.120.76.177:8080/consultaplanillas/servlet/gob.ec.sapconsultas")
respuesta = scrap.enquiry('200011355167')
print(respuesta)
