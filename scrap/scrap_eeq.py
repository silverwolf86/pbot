import re
import mechanicalsoup
from bs4 import BeautifulSoup
# CHANGE THIS TO MECHANIZE SOUP


class Eeq_Scrap():

    def __init__(self, url):
        self.url = url

    def enquiry(self, counterpart):
        msg_response = ""
        
        try:      

            import requests
            r = requests.post("http://190.120.76.177:8080/consultaplanillas/servlet/gob.ec.sapconsultas",
                              data={'vNRODATO': counterpart, 'vTIPODOCUMENTO': '3'})
            print(r.status_code, r.reason)


            browser = mechanicalsoup.StatefulBrowser()

            browser.open(self.url)

            #soup_result1 = 1
            form = browser.select_form(nr=0)             

            form['vNRODATO'] = counterpart
            form['vTIPODOCUMENTO'] = '3'

            browser.get_current_form().print_summary()        
            response = browser.submit(
                form, url="http://190.120.76.177:8080/consultaplanillas/servlet/gob.ec.sapconsultas")
            
            soup_result = BeautifulSoup(response.content, "lxml")
            for foo in soup_result.findAll("div", {"class": "section-after"}):
                bar = foo.find('div', attrs={'class': 'right'})
                msg_response = bar.text
                break                

            for foo in soup_result.findAll("section", {"class": "section-bottom"}):
                bar = foo.find('div', attrs={'class': 'data'})
                msg_response += bar.text                                

        except Exception as e1:
            print("errors %s", e1.args)
            msg_response = 'Error, consulte con el administrador'
        finally:
            return msg_response


scrap = Eeq_Scrap('http://190.120.76.177:8080/consultaplanillas/servlet/gob.ec.sapconsultas')
scrap.enquiry('200011355167')
