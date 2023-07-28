import requests
import json
import time
import re
import os
import pandas as pd
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from Reptiles import Reptiles

class ShanXi(Reptiles):
    def collectData(self):
        return

class HuNan(Reptiles):
    def collectData(self):
        return

class HaiNan(Reptiles):
    def collectData(self):
        return

class GuangXi(Reptiles):
    def collectData(self):
        return

class ShaanXi(Reptiles):
    def collectData(self):
        return

class ShangHai(Reptiles):
    def collectData(self):
        return

class ZheJiang(Reptiles):
    def collectData(self):
        df1 = self.collectCategoryData("免费", "//div[contains(text(),'免费')]")
        df2 = self.collectCategoryData("免费", "//div[contains(text(),'收费')]")
        df3 = self.collectCategoryData("免费", "//div[contains(text(),'绿色')]")
        return pd.concat([df1, df2, df3])

    def collectCategoryData(self, category_type, category_xpath):
        self.br.find_element(By.XPATH, category_xpath).click()
        n_page = self.getPageNum()
        print(category_type, "共", n_page, "页")
        data = []
        for page_i in range(1, n_page+1):
            rows = self.getRowNum(page_i, n_page)
            print(page_i, "页", rows, "行")
            for index in range(1, rows + 1):
                data.append(self.getTuple(index))
            if page_i < n_page:
                self.nextPage()
                time.sleep(2)
        variables = list(data[0].keys())
        return pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)


    def getTuple(self, index):
        detail_btn = self.br.find_element(By.XPATH, self.rownum_xpath + "/li[" + str(index) + "]/a[1]")
        detail_btn.click()
        ws = self.br.window_handles
        self.br.switch_to.window(ws[1])
        time.sleep(2)
        self.br.find_element(By.XPATH, "//div[contains(text(),'许可说明')]").click()
        patent_id = self.br.find_element(By.XPATH, "//span[contains(text(),'申请号')]").text[4:]
        patent_owner = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[4]/div[1]/div[1]/div[1]/p[2]/span[6]")
        patent_type = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[4]/div[1]/div[1]/div[1]/p[1]/span[2]/span[2]").text
        license_fee = self.br.find_element(By.XPATH, "//body/div[@id='app']/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[4]/div[1]/table[1]/tr[1]/td[1]/span[1]").text
        license_period = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[3]/ul[1]/li[2]/span[2]").text
        license_location = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[3]/ul[1]/li[3]/span[2]").text
        license_deadline = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/div[3]/div[3]/ul[1]/li[1]/span[2]").text

        self.br.close()
        self.br.switch_to.window(ws[0])
        return {
            'patent_id': patent_id,
            'patent_type': patent_type,
            'patent_owner': patent_owner,
            'license_deadline': license_deadline,
            'license_fee': license_fee,
            'license_period': license_period,
            'license_location': license_location
        }

    def nextPage(self):
        bar = self.br.find_element(By.XPATH, self.pagenum_xpath)
        bar_cnt = len(bar.find_elements(By.TAG_NAME, "li"))
        next_btn = self.br.find_element(By.XPATH, self.pagenum_xpath + "/li[" + str(bar_cnt - 1) + "]/a[1]")
        self.br.execute_script("arguments[0].click()", next_btn)
        self.curr_page = self.curr_page + 1

    def getPageNum(self):
        bar = self.br.find_element(By.XPATH, self.pagenum_xpath)
        bar_cnt = len(bar.find_elements(By.TAG_NAME, "li"))
        return int(self.br.find_element(By.XPATH, self.pagenum_xpath + "/li[" + str(bar_cnt-2) + "]/a[1]").text)

    def getRowNum(self, page_i, n_page):
        menu_table = self.br.find_element(By.XPATH, self.rownum_xpath)
        table_content = menu_table.find_elements(By.TAG_NAME, "li")
        return len(table_content)


class BeiJing(Reptiles):
    def getPageNum(self):
        return int(re.findall(r"\d+",self.br.find_element(By.CLASS_NAME, "total").text)[0])

    def collectData(self):
        n_page = self.getPageNum()
        print("共", n_page, "页")
        for page_i in range(1, n_page+1):
            time.sleep(0.3)
            self.nextPage()
        df = pd.DataFrame()
        for id in self.getRequestId():
            res = self.getResponseBody(id)
            df = pd.concat([df, pd.DataFrame(res)])
        return df.drop_duplicates()

    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['rows']
        patent_info_cnt = len(data)
        data_json = []

        for index in range(0, patent_info_cnt):
            data_json.append({
                'patent_id': data[index]['zlnum'],
                'patent_type': data[index]['spare1'],
                'patent_owner': data[index]['cydw'],
                'patent_owner_type': data[index]['zlqrxz'],
                'license_fee_type': data[index]['zlfzffs'],
                'license_fee_detail': ILLEGAL_CHARACTERS_RE.sub(r'', data[index]['spare2']),
                'license_deadline': data[index]['xkqxjmr'],
                'create_time': data[index]['createtime']
            })
        return data_json

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
                    if type_.upper() == "XHR" and data_type.find("page=") != -1:
                        # print("page", data_type[130:])
                        log_xhr_array.append(id)
            except:
                pass
        return list(set(log_xhr_array))

class GuangDong(Reptiles):
    def collectData(self):
        n_page = self.getPageNum()
        print("共", n_page, "页")
        for page_i in range(1, n_page+1):
            time.sleep(0.2)
            self.nextPage()
        df = pd.DataFrame()
        for id in self.getRequestId():
            res = self.getResponseBody(id)
            df = pd.concat([df, pd.DataFrame(res)])
        return df.drop_duplicates()

    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['data']
        patent_info_cnt = len(data['records'])
        data_json = []

        patent_type_list = ['发明', '实用新型', '外观设计']
        patent_owner_type_list = ['高校', '科研院所', '国有企业', '其他']
        for index in range(0, patent_info_cnt):
            data_json.append({
                'patent_id': data['records'][index]['zlxkCode'],
                'patent_type': patent_type_list[int(data['records'][index]['type']) - 1],
                'patent_owner': data['records'][index]['zlxxUser'],
                'patent_owner_type': patent_owner_type_list[int(data['records'][index]['zlxxUsertype']) - 1],
                'license_fee_type': data['records'][index]['xkfyJson'],
                'license_deadline': data['records'][index]['zlxkDate'],
                'license_location': data['records'][index]['zlxkArea']
            })
        return data_json

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
                    if type_.upper() == "XHR" and data_type.find("list?page=") != -1:
                        # print("page", data_type[56:59])
                        log_xhr_array.append(id)
            except:
                pass
        return list(set(log_xhr_array))

class HuBei(Reptiles):
    def collectData(self):
        return

class LiaoNing(Reptiles):
    def getTuple(self, index):
        try:
            detail_btn = self.br.find_element(By.XPATH,"//body/div[@id='app']/div[1]/div[1]/div[2]/div[2]/div[3]/div[1]/div["+str(index)+"]/img[1]")
        except exceptions.NoSuchElementException:
            return
        detail_btn.click()
        ws = self.br.window_handles
        self.br.switch_to.window(ws[1])
        time.sleep(0.2)
        patent_id = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/span[2]").text
        patent_owner = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/span[4]").text[5:]
        patent_type = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]/span[2]").text[5:]
        license_fee = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/span[1]/span[1]").text
        publish_date_str = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/div[3]").text
        publish_date = re.findall(r"发布日期：\n(.+?)", publish_date_str)[0]
        self.br.close()
        self.br.switch_to.window(ws[0])
        return {
            'patent_id': patent_id,
            'patent_type': patent_type,
            'patent_owner': patent_owner,
            'license_fee': license_fee,
            'publish_date': publish_date
        }

class SiChuan(Reptiles):
    def getTuple(self, index):
        patent_id = self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[1]/div[1]").text
        patent_owner = self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[3]/div[1]").text
        patent_type = self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[4]/div[1]").text
        license_fee_type = self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[7]/div[1]").text
        license_period = self.br.find_element(By.XPATH,"//tbody/tr[" + str(index) + "]/td[6]/div[1]").text

        return {
            'patent_id': patent_id,
            'patent_owner': patent_owner,
            'patent_type': patent_type,
            'license_period': license_period,
            'license_fee_type': license_fee_type,
        }

class ShanDong(Reptiles):
    def collectData(self):
        bar = self.br.find_element(By.XPATH, "//div[@id='NavPage']").text
        n_page = int(re.findall(r"/(.+?)（", bar)[0])
        data = []
        for page_i in range(1, n_page+1):
            print(page_i, "页")
            menu_table = self.br.find_element(By.XPATH, "//body/div[3]/div[1]/div[2]/form[1]/ul[1]")
            rows = len(menu_table.find_elements(By.TAG_NAME, "li"))
            for index in range(1, rows + 1):
                data.append(self.getTuple(index))
            if page_i < n_page:
                self.nextPage()

        variables = list(data[0].keys())
        return pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)

    def getTuple(self, index):
        patent_id_str = self.br.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/form[1]/ul[1]/li[" + str(index) + "]/a[1]/div[1]/p[3]").text
        patent_owner_str = self.br.find_element(By.XPATH, "//body/div[3]/div[1]/div[2]/form[1]/ul[1]/li[" + str(index) + "]/a[1]/div[1]/p[2]").text
        license_fee_type_str = self.br.find_element(By.XPATH, "//body/div[3]/div[1]/div[2]/form[1]/ul[1]/li[" + str(index) + "]/a[1]/div[1]/p[4]").text
        patent_id = re.findall(r"【(.+?)】", patent_id_str)[0]
        patent_owner = re.findall(r"(.+?)\s", patent_owner_str)[0]
        license_fee_type = license_fee_type_str[5:]
        license_deadline = self.br.find_element(By.XPATH,"//body/div[3]/div[1]/div[2]/form[1]/ul[1]/li[" + str(index) + "]/a[1]/div[1]/p[1]").text

        return {
            'patent_id': patent_id,
            'patent_owner': patent_owner,
            'license_deadline': license_deadline,
            'license_fee_type': license_fee_type,
        }

class JiangSu(Reptiles):
    def collectData(self):
        return

class FuJian(Reptiles):
    def collectData(self):
        n_page = int(self.br.find_element(By.XPATH, "//span[@id='tnum']").text)

        data = []
        for page_i in range(1, n_page+1):
            menu_table = self.br.find_element(By.XPATH, "//body/div[4]/div[1]/div[2]")
            rows = len(menu_table.find_elements(By.TAG_NAME, "div"))
            print(page_i, "页")
            for index in range(1, rows + 1):
                data.append(self.getTuple(index))
            if page_i < n_page:
                self.nextPage()

        variables = list(data[0].keys())
        return pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)

    def getTuple(self, index):
        detail_btn = self.br.find_element(By.XPATH, "//body/div[4]/div[1]/div[2]/div[" + str(index) + "]/h4[1]/a[1]/button[1]")
        detail_btn.click()
        ws = self.br.window_handles
        self.br.switch_to.window(ws[1])

        patent_id = self.br.find_element(By.XPATH, "//span[contains(text(),'专利号')]").text[4:]
        patent_owner = self.br.find_element(By.XPATH, "//span[contains(text(),'专利权人')]").text[5:]
        patent_type = self.br.find_element(By.XPATH, "//span[@class='patenttype-type']").text
        license_fee_type = self.br.find_element(By.XPATH, "//span[contains(text(),'许可费用')]").text[5:]
        license_location = self.br.find_element(By.XPATH, "//span[contains(text(),'许可地域范围')]").text[7:]
        license_deadline = self.br.find_element(By.XPATH, "//span[@id='notice_time ']").text

        self.br.close()
        self.br.switch_to.window(ws[0])
        return {
            'patent_id': patent_id,
            'patent_type': patent_type,
            'patent_owner': patent_owner,
            'license_deadline': license_deadline,
            'license_fee_type': license_fee_type,
            'license_location': license_location
        }

class HeBei(Reptiles):
    def collectData(self):
        df0 = self.collectCategoryData("", "//body/article[@id='miao']/div[1]/div[1]/dl[4]/div[2]/a[1]")
        df1 = self.collectCategoryData("高校", "//body/article[@id='miao']/div[1]/div[1]/dl[4]/div[2]/a[2]")
        df2 = self.collectCategoryData("研究院", "//body/article[@id='miao']/div[1]/div[1]/dl[4]/div[2]/a[3]")
        df3 = self.collectCategoryData("大中型国有企业", "//body/article[@id='miao']/div[1]/div[1]/dl[4]/div[2]/a[4]")
        df4 = self.collectCategoryData("中小微企业", "//body/article[@id='miao']/div[1]/div[1]/dl[4]/div[2]/a[5]")
        df5 = self.collectCategoryData("个人", "//body/article[@id='miao']/div[1]/div[1]/dl[4]/div[2]/a[6]")
        df_category = pd.concat([df1, df2, df3, df4, df5])
        merged_table = pd.concat([df0, df_category]).drop_duplicates(subset='patent_id', keep='last').reset_index(drop=True)
        return merged_table

    def getPageNum(self, bar_xpath):
        try:
            self.br.find_element(By.XPATH, bar_xpath)
        except exceptions.NoSuchElementException:
            return 1 if len(self.br.find_element(By.XPATH, "//body/article[@id='zlsclist']/ul[1]").find_elements(By.TAG_NAME, "li")) > 0 else 0

        bar = self.br.find_element(By.XPATH, bar_xpath)
        n_bar_elements = len(bar.find_elements(By.TAG_NAME, "li"))
        last_page_xpath = bar_xpath + "/li[" + str(n_bar_elements-1) + "]/a[1]"
        return int(self.br.find_element(By.XPATH, last_page_xpath).text)

    def collectCategoryData(self, owner_type, category_xpath):
        category_btn = self.br.find_element(By.XPATH, category_xpath)
        self.br.execute_script("arguments[0].click()", category_btn)
        n_page = self.getPageNum("/html[1]/body[1]/ul[1]/ul[1]")
        print(n_page, "页")
        if n_page ==0:
            return
        data = []
        for page_i in range(1, n_page+1):
            menu_table = self.br.find_element(By.XPATH, "/html[1]/body[1]/article[3]/ul[1]")
            rows = len(menu_table.find_elements(By.TAG_NAME, "li"))
            print(rows)
            for index in range(1,rows+1):
                data.append(self.getTuple(owner_type, index))
            if page_i < n_page:
                self.nextPage()
        variables = list(data[0].keys())
        return pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)

    def getTuple(self, owner_type, index):
        self.br.find_element(By.XPATH, "//body/article[@id='zlsclist']/ul[1]/li[" + str(index) + "]/a[1]/img[1]").click()
        patent_id = self.br.find_element(By.XPATH, "/html[1]/body[1]/article[2]/div[1]/div[2]/ul[1]/li[1]/span[3]").text
        patent_type = self.br.find_element(By.XPATH, "/html[1]/body[1]/article[2]/div[1]/div[2]/ul[1]/li[2]/span[3]").text
        license_fee = self.br.find_element(By.XPATH, "/html[1]/body[1]/article[2]/div[1]/div[2]/ul[1]/li[4]/span[3]/i[1]").text
        license_fee_type = self.findDetailFee()
        license_deadline = self.br.find_element(By.XPATH, "/html[1]/body[1]/article[2]/div[1]/div[2]/ul[1]/li[5]/span[3]").text

        self.br.back()
        return {
            'patent_id': patent_id,
            'patent_type': patent_type,
            'patent_owner_type': owner_type,
            'license_deadline': license_deadline,
            'license_fee': license_fee,
            'license_fee_type': license_fee_type
        }

    def findDetailFee(self):
        try:
            pattern1_1 = self.br.find_element(By.XPATH, "//span[contains(text(),'入门费')]")
            pattern1_2 = self.br.find_element(By.XPATH, "//span[contains(text(),'提成费')]")
        except exceptions.NoSuchElementException:
            pass
        else:
            return pattern1_1.text +pattern1_2.text
        try:
            pattern2_1 = self.br.find_element(By.XPATH, "//span[contains(text(),'一次总付')]")
            pattern2_2 = self.br.find_element(By.XPATH, "//span[contains(text(),'一次性支付')]")
        except exceptions.NoSuchElementException:
            pass
        else:
            return pattern2_1.text + pattern2_2.text
        try:
            pattern3 = self.br.find_element(By.XPATH, "//p[contains(text(),'分期支付')]")
        except exceptions.NoSuchElementException:
            pass
        else:
            return pattern3.text
        try:
            pattern4 = self.br.find_element(By.XPATH, "//p[contains(text(),'免费')]")
        except exceptions.NoSuchElementException:
            pass
        else:
            return pattern4.text
        try:
            pattern5 = self.br.find_element(By.XPATH, "//p[contains(text(),'入门费')]")
        except exceptions.NoSuchElementException:
            pass
        else:
            return pattern5.text
        try:
            pattern6 = self.br.find_element(By.XPATH, "//p[contains(text(),'一次总付')]")
        except exceptions.NoSuchElementException:
            pass
        else:
            return pattern6.text
        return "fail"

class TianJin(Reptiles):
    def collectData(self):
        data = pd.DataFrame()
        page = 0
        while (True):
            page = page + 1
            print("page", page)
            data = pd.concat([data, self.getPage()])
            try:
                self.br.find_element(By.XPATH, self.nextpage_xpath)
            except exceptions.NoSuchElementException:
                return data
            else:
                self.nextPage()

    def getPage(self):
        data = []

        menu_table = self.br.find_element(By.XPATH, "/html[1]/body[1]/section[2]/div[2]/table[1]")
        rows = menu_table.find_elements(By.TAG_NAME, 'tr')

        for index in range(1, len(rows)):
            data.append(self.getTuple(index))
        variables = list(data[0].keys())
        return pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)

    def getTuple(self, index):
        patent_id = self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[1]").text
        patent_owner = self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[3]").text
        license_deadline = self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[5]").text

        detail_btn = self.br.find_element(By.XPATH, "//tbody/tr[" + str(index) + "]/td[6]/a[1]")
        self.br.execute_script("arguments[0].click()", detail_btn)
        patent_type = self.br.find_element(By.XPATH,
                                           "/html[1]/body[1]/section[2]/div[2]/div[2]/div[2]/div[1]/div[3]/span[2]").text
        license_fee_type = self.br.find_element(By.XPATH,
                                                "/html[1]/body[1]/section[2]/div[3]/div[2]/div[1]/table[2]/tbody[1]/tr[1]/td[2]").text
        license_fee_detail = self.br.find_element(By.XPATH,
                                                  "/html[1]/body[1]/section[2]/div[3]/div[2]/div[1]/table[2]/tbody[1]/tr[1]/td[3]").text
        effective_date = self.br.find_element(By.XPATH,
                                              "/html[1]/body[1]/section[2]/div[2]/div[2]/div[2]/div[1]/div[5]/span[2]").text

        self.br.back()
        return {
            'patent_id': patent_id,
            'patent_owner': patent_owner,
            'patent_type': patent_type,
            'license_deadline': license_deadline,
            'license_fee_type': license_fee_type,
            'license_fee_detail': license_fee_detail,
            'effective_date': effective_date
        }

class AnHui(Reptiles):
    def collectData(self):
        data = []

        menu_table = self.br.find_element(By.XPATH, "//body/div[2]/div[1]/table[1]")
        rows = menu_table.find_elements(By.TAG_NAME, 'tr')

        for index in range(1, int(len(rows) / 2) + 1):
            # print("第", index, "行")
            data.append(self.getTuple(index))
        variables = list(data[0].keys())
        return pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)

    def getTuple(self, index):
        patent_id = self.br.find_element(By.XPATH, "//tbody/tr[" + str(2 * index - 1) + "]/td[3]").text
        patent_type = self.br.find_element(By.XPATH, "//tbody/tr[" + str(2 * index - 1) + "]/td[4]").text
        license_deadline = self.br.find_element(By.XPATH, "//tbody/tr[" + str(2 * index - 1) + "]/td[5]").text
        license_fee_type = self.br.find_element(By.XPATH, "//tbody/tr[" + str(2 * index - 1) + "]/td[6]").text
        license_period = self.br.find_element(By.XPATH, "//tbody/tr[" + str(2 * index - 1) + "]/td[7]").text
        return {
            'patent_id': patent_id,
            'patent_type': patent_type,
            'license_deadline': license_deadline,
            'license_fee_type': license_fee_type,
            'license_period': license_period
        }
