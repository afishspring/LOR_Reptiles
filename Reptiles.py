import requests
import json
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class Reptiles(object):
    def __init__(self, website, next_page_xpath="", bar_xpath="", bar_child_tag_name="", n_page_offset=0):
        self.load_browser()

        self.website = website
        self.next_page_xpath = next_page_xpath
        self.bar_xpath = bar_xpath
        self.bar_child_tag_name = bar_child_tag_name
        self.n_page_offset = n_page_offset

        self.data = pd.DataFrame()
        self.curr_page = 1
    def load_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('w3c', True)
        prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disk-cache-size=1073741824")
        chrome_options.add_argument("--media-cache-size=1073741824")
        caps = DesiredCapabilities.CHROME
        caps["goog:loggingPrefs"] = {"performance": "ALL"}
        self.br = webdriver.Chrome(desired_capabilities=caps, options=chrome_options)
        self.br.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
    def start(self):
        self.openWebSite(self.website)
        self.data = self.collectData()
        print(self.data)
        self.br.quit()
    def exportData(self, path):
        self.data.to_excel(path, index=False)
    def openWebSite(self, website):
        self.br.get(website)
        self.br.maximize_window()
        self.br.implicitly_wait(10)
        # zoom_out = "document.body.style.zoom='0.25'"
        # self.br.execute_script(zoom_out)
    def nextPage(self):
        next_btn = self.br.find_element(By.XPATH, self.next_page_xpath)
        self.br.execute_script("arguments[0].click()", next_btn)
        self.curr_page = self.curr_page + 1
    def getPageNum(self):
        bar = self.br.find_element(By.XPATH, self.bar_xpath)
        n_bar_child = len(bar.find_elements(By.TAG_NAME, self.bar_child_tag_name))
        n_page_xpath = self.bar_xpath + "/" + self.bar_child_tag_name + "[" + str(n_bar_child - self.n_page_offset) + "]"
        return int(self.br.find_element(By.XPATH, n_page_xpath).text)
    def collectData(self):
        pass

class Reptiles_XHR(Reptiles):
    def __init__(self, website, next_page_xpath="", bar_xpath="", bar_child_tag_name="", n_page_offset=0,
                 xhr_pattern="page"):
        super(Reptiles_XHR, self).__init__(website, next_page_xpath, bar_xpath, bar_child_tag_name, n_page_offset)
        self.xhr_pattern = xhr_pattern
    def collectData(self):
        n_page = self.getPageNum()
        print("共", n_page, "页")
        for page_i in range(1, n_page+1):
            print("第", page_i, "页")
            if page_i < n_page:
                time.sleep(0.1)
                self.nextPage()
        time.sleep(5)
        df = pd.DataFrame()
        for id in self.getRequestId():
            res = self.getResponseBody(id)
            df = pd.concat([df, pd.DataFrame(res)])
        return df.drop_duplicates()
    def getResponseBody(self, requestId):
        pass
    def getRequestId(self):
        logs = self.br.get_log("performance")
        log_xhr_array = []
        for log_data in logs:
            message_ = log_data['message']
            try:
                log_json = json.loads(message_)
                log = log_json['message']
                if log['method'] == 'Network.responseReceived':
                    type_ = log['params']['type']
                    id = log['params']['requestId']
                    data_type = log['params']['response']['url']
                    if type_.upper() == "XHR" and data_type.find(self.xhr_pattern) != -1:
                        log_xhr_array.append(id)
            except:
                pass
        return list(set(log_xhr_array))

class Reptiles_DOM(Reptiles):
    def __init__(self, website, next_page_xpath="", bar_xpath="", bar_child_tag_name="", n_page_offset=0,
                 table_xpath="", table_tuple_type=By.CLASS_NAME, table_tuple_class_name=""):
        super(Reptiles_DOM, self).__init__(website, next_page_xpath, bar_xpath, bar_child_tag_name, n_page_offset)
        self.table_xpath = table_xpath
        self.table_tuple_type = table_tuple_type
        self.table_tuple_class_name = table_tuple_class_name
    def getRowNum(self, page_i, n_page):
        menu_table = self.br.find_element(By.XPATH, self.table_xpath)
        table_content = menu_table.find_elements(self.table_tuple_type, self.table_tuple_class_name)
        rows = 0
        if page_i == n_page:
            for ele in table_content:
                try:
                    ele.is_displayed()
                    ele.is_enabled()
                except exceptions.StaleElementReferenceException or exceptions.NoSuchElementException:
                    break
                else:
                    rows = rows + 1
        else:
            rows = len(table_content)
        return rows
    def collectData(self):
        n_page = self.getPageNum()
        print("共", n_page, "页")
        data = []
        for page_i in range(1, n_page + 1):
            rows = self.getRowNum(page_i, n_page)
            print(page_i, "页", rows, "行")
            for index in range(1, rows + 1):
                data.append(self.getTuple(index))
            if page_i < n_page:
                time.sleep(0.2)
                self.nextPage()

        variables = list(data[0].keys())
        return pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)
    def getTuple(self, index):
        pass
