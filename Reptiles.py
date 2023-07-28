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
    def __init__(self, website, nextpage_xpath, totalnum_xpath, pagenum_xpath, rownum_xpath, rownum_class_name):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('w3c', True)
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
        self.website = website
        self.nextpage_xpath = nextpage_xpath
        self.totalnum_xpath = totalnum_xpath
        self.pagenum_xpath = pagenum_xpath
        self.rownum_xpath = rownum_xpath
        self.rownum_class_name = rownum_class_name
        self.data = pd.DataFrame()
        self.curr_page = 1

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
        time.sleep(2)
        # zoom_out = "document.body.style.zoom='0.25'"
        # self.br.execute_script(zoom_out)
        if self.totalnum_xpath != "":
            self.totalnum = int(re.findall(r"\d+", self.br.find_element(By.XPATH, self.totalnum_xpath).text)[0])

    def getPageNum(self):
        bar = self.br.find_element(By.XPATH, self.pagenum_xpath)
        last_page_num = len(bar.find_elements(By.TAG_NAME, "li"))
        return int(self.br.find_element(By.XPATH, self.pagenum_xpath+"/li[" + str(last_page_num) + "]").text)

    def getRowNum(self, page_i, n_page):
        menu_table = self.br.find_element(By.XPATH, self.rownum_xpath)
        table_content = menu_table.find_elements(By.CLASS_NAME, self.rownum_class_name)
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
                time.sleep(2)
                self.nextPage()
                variables = list(data[0].keys())
                print(pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables))

        variables = list(data[0].keys())
        return pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)

    def nextPage(self):
        next_btn = self.br.find_element(By.XPATH, self.nextpage_xpath)
        self.br.execute_script("arguments[0].click()", next_btn)
        self.curr_page = self.curr_page + 1

    def getTuple(self, index):
        pass