import re
import mechanicalsoup
from bs4 import BeautifulSoup
# CHANGE THIS TO MECHANIZE SOUP


class EmmapScrap():

    def __init__(self, url):
        self.url = url

    def enquiry(self, counterpart):
        msg_response = ""
        
        try:            

            browser = mechanicalsoup.StatefulBrowser()

            browser.open(self.url)
            browser.select_form(nr=0)
            browser['Cuenta'] = counterpart
            response = browser.submit_selected()
            
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


#scrap = EmmapScrap('http://consultas.aguaquito.gob.ec/BuscarCuentas.php')
#scrap.enquiry('50674485')
