import requests
import json
import time
import re
import os
import datetime
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
from Reptiles import Reptiles_XHR, Reptiles_DOM, Reptiles

class ShanXi(Reptiles_XHR):
    def getResponseBody(self, requestId):
        return

class HuNan(Reptiles_XHR):
    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['bodyData']
        patent_info_cnt = len(data['list'])
        data_json = []

        for index in range(0, patent_info_cnt):
            data_json.append({
                'patent_id': data['list'][index]['ipc'],
                'patent_type': data['list'][index]['penterClassName'],
                'patent_owner': data['list'][index]['applicant'],
                'license_fee': data['list'][index]['price'],
                'license_deadline': data['list'][index]['openEndStr'],
                'create_time': data['list'][index]['createDateStr']
            })
        return data_json

class HaiNan(Reptiles_XHR):
    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['data']
        patent_info_cnt = len(data['list'])
        data_json = []

        for index in range(0, patent_info_cnt):
            data_json.append({
                'patent_id': data['list'][index]['patent_sn'],
                'patent_type': data['list'][index]['type_name'],
                'patent_owner': data['list'][index]['patent_user'] if data['list'][index]['apply_user']=="" else data['list'][index]['apply_user'],
                'license_fee': data['list'][index]['suggest_price'],
                'license_period': data['list'][index]['license_time'],
                'license_location': data['list'][index]['license_scope'],
                'create_time': data['list'][index]['create_time']
            })
        return data_json
    def getPageNum(self):
        return 27

class GuangXi(Reptiles_XHR):
    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['data']
        patent_info_cnt = len(data['content'])
        data_json = []

        for index in range(0, patent_info_cnt):
            data_json.append({
                'patent_id': data['content'][index]['attr']['zlh']['value'].replace(" ",""),
                'patent_type': data['content'][index]['attr']['fbzllx']['value'],
                'patent_owner': data['content'][index]['attr']['zlqr']['value'],
                'patent_owner_type': data['content'][index]['attr']['tjzlx']['value'],
                'license_fee': data['content'][index]['attr']['yczff_ycxqefy']['value'],
                'license_fee_type': data['content'][index]['attr']['xkfybz']['value'],
                'license_deadline': data['content'][index]['attr']['xkqxjmr']['value'],
                'createTime': data['content'][index]['createTime']
            })
        return data_json

class ShaanXi(Reptiles_XHR):
    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['data']
        patent_info_cnt = len(data['list'])
        data_json = []

        for index in range(0, patent_info_cnt):
            licenseTimeStart = time.strftime("%Y-%m-%d", time.localtime(data['list'][index]['licenseTimeStart']/1000))
            licenseTimeEnd = time.strftime("%Y-%m-%d", time.localtime(data['list'][index]['licenseTimeEnd']/1000))
            d1 = datetime.datetime.strptime(licenseTimeStart, '%Y-%m-%d')
            d2 = datetime.datetime.strptime(licenseTimeEnd, '%Y-%m-%d')

            patent_owner_list = data['list'][index]['assigneeList']
            data_json.append({
                'patent_id': data['list'][index]['appNumber'],
                'patent_type': data['list'][index]['type'],
                'patent_owner': patent_owner_list[0] if len(patent_owner_list)>0 else "null",
                'license_fee': data['list'][index]['licenseFee'],
                'license_deadline': licenseTimeEnd,
                'license_period': int((d2 - d1).days / 365),
                'license_location': data['list'][index]['licenseArea']
            })
        return data_json
    def getPageNum(self):
        return int(re.findall(r"\d+", self.br.find_element(By.CSS_SELECTOR, self.bar_xpath).text)[0])

class ShangHai(Reptiles_XHR):
    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['data']
        patent_info_cnt = len(data)
        data_json = []

        for index in range(0, patent_info_cnt):
            content = data[index]['content']
            content = re.sub(r"<[^>]+>", "", content)
            content = content.replace("&nbsp;", "")
            content = content.replace(" ", "")
            patent_id_pattern = re.findall(r"专利号：(.+?)专利权人：", content)
            patent_type_pattern = re.findall(r"专利类型：(.+?)专利号：", content)
            patent_owner_pattern = re.findall(r"专利权人：(.+?)许可范围：", content)
            license_fee_pattern = re.findall(r"许可使用费：(.+?)许可使用费支付方式：", content)
            license_fee_type_pattern = re.findall(r"许可使用费支付方式：(.*?)交易中心联系人：", content)
            license_deadline_pattern = re.findall(r"许可期限届满日：(\d+年\d+月\d+日)", content)
            license_location_pattern = re.findall(r"许可范围：(.+?)许可期限届满日", content)
            data_json.append({
                'patent_id': patent_id_pattern[0] if len(patent_id_pattern)>0 else "null",
                'patent_type': patent_type_pattern[0] if len(patent_type_pattern)>0 else "null",
                'patent_owner': patent_owner_pattern[0] if len(patent_owner_pattern)>0 else "null",
                'license_fee': license_fee_pattern[0] if len(license_fee_pattern)>0 else "null",
                'license_fee_type': license_fee_type_pattern[0] if len(license_fee_type_pattern)>0 else "null",
                'license_deadline': license_deadline_pattern[0] if len(license_deadline_pattern)>0 else "null",
                'license_location': license_location_pattern[0] if len(license_location_pattern)>0 else "null",
                'create_time': data[index]['createTime']
            })
        return data_json

class ZheJiang(Reptiles):
    def collectData(self):
        href_list_1 = self.collectCategoryData("免费", "//div[contains(text(),'免费')]")
        href_list_2 = self.collectCategoryData("收费", "//div[contains(text(),'收费')]")
        href_list_3 = self.collectCategoryData("绿色", "//div[contains(text(),'绿色')]")
        href_list = href_list_1 + href_list_2 + href_list_3
        for href in href_list:
            self.br.execute_script("window.open(arguments[0],'_self','')", href)
            self.br.back()
            time.sleep(0.1)
        detail_list, data_list = self.getRequestId()
        data_1 = []
        data_2 = []
        for id in detail_list:
            data_1.append(self.getResponseBody("detail", id))
        for id in data_list:
            data_2.append(self.getResponseBody("data", id))
        data_1 = pd.DataFrame(data_1)
        data_2 = pd.DataFrame(data_2)
        return data_1.set_index("id").join(data_2.set_index("id"), on="id", how="inner").reset_index().drop_duplicates()

    def collectCategoryData(self, category_type, category_xpath):
        self.br.find_element(By.XPATH, category_xpath).click()
        self.br.find_element(By.XPATH, self.pagenum_xpath + "/li[3]").click()
        n_page = self.getPageNum()
        print(category_type, "共", n_page, "页")

        href_list = []
        for page_i in range(1, n_page+1):
            rows = self.getRowNum(page_i, n_page)
            print(page_i, "页", rows, "行")
            for index in range(1, rows + 1):
                href_list.append(
                    self.br.find_element(By.XPATH,
                                         self.rownum_xpath + "/li[" + str(index) + "]/a[1]").get_attribute('href')
                )
            if page_i < n_page:
                self.nextPage()
                time.sleep(0.5)
        return href_list

    def getResponseBody(self, type, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        if type=="detail":
            data = json.loads(response_body['body'])['data']
            return {
                'id': data['PrjId'],
                'patent_owner_type': data['RIGHTTYPE'],
                'license_fee': data['XKSYFBZSM'],
                'license_deadline': data['XKSMJMRQ1'],
                'license_location': data['XKDYFW_NOTE'],
                'license_period': data['DCXKQX']
            }
        else:
            data = json.loads(response_body['body'])['data'][0]
            return {
                'id': data['tprj_info_ext_ID'],
                'patent_id': data['ZLBH'],
                'patent_type': data['ZLLX_NOTE'],
                'patent_owner': data['ZLQR']
            }
    def getRequestId(self):
        logs = self.br.get_log("performance")
        log_xhr_detail_array = []
        log_xhr_data_array = []
        for log_data in logs:
            message_ = log_data['message']
            try:
                log_json = json.loads(message_)
                log = log_json['message']
                if log['method'] == 'Network.responseReceived':
                    type_ = log['params']['type']
                    id = log['params']['requestId']
                    data_type = log['params']['response']['url']
                    if type_.upper() == "XHR":
                        if data_type.find("Detail") != -1:
                            log_xhr_detail_array.append(id)
                        elif data_type.find("Data") != -1:
                            log_xhr_data_array.append(id)
            except:
                pass
        return log_xhr_detail_array, log_xhr_data_array
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

class BeiJing(Reptiles_XHR):
    def getPageNum(self):
        return int(re.findall(r"\d+",self.br.find_element(By.CLASS_NAME, "total").text)[0])
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

class GuangDong(Reptiles_XHR):
    def getResponseBody(self, requestId):
        try:
            response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        except exceptions.WebDriverException:
            return
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
    def nextPage(self):
        input = self.br.find_element(By.XPATH, self.next_page_xpath)
        input.send_keys(Keys.CONTROL+'a')
        input.send_keys(Keys.DELETE)
        input.send_keys(self.curr_page)
        input.send_keys(Keys.ENTER)
        self.curr_page = self.curr_page+1

class HuBei(Reptiles):
    def collectData(self):
        return

class LiaoNing(Reptiles_XHR):
    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['data']
        patent_info_cnt = len(data['records'])
        data_json = []

        for index in range(0, patent_info_cnt):
            data_json.append({
                'patent_id': data['records'][index]['patentNum'],
                'patent_type': data['records'][index]['type'],
                'patent_owner': data['records'][index]['company'],
                'license_fee': data['records'][index]['price'],
                'create_time': data['records'][index]['createTime']
            })
        return data_json

class SiChuan(Reptiles_XHR):
    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['data']
        patent_info_cnt = len(data['result'])
        data_json = []

        for index in range(0, patent_info_cnt):
            data_json.append({
                'patent_id': data['result'][index]['patent_number'],
                'patent_owner': data['result'][index]['patentee'],
                'patent_type': data['result'][index]['patent_type'],
                'license_period': data['result'][index]['license_period'],
                'license_fee_type': data['result'][index]['license_fee'],
            })
        return data_json

class ShanDong(Reptiles_DOM):
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
    def getPageNum(self):
        bar = self.br.find_element(By.XPATH, "//div[@id='NavPage']").text
        return int(re.findall(r"/(.+?)（", bar)[0])

class JiangSu(Reptiles_XHR):
    def getResponseBody(self, requestId):
        response_body = self.br.execute_cdp_cmd('Network.getResponseBody', {'requestId': requestId})
        data = json.loads(response_body['body'])['data']
        patent_info_cnt = len(data)
        data_json = []

        for index in range(0, patent_info_cnt):
            patent_type_list = ['发明', '实用新型', '外观设计']
            patent_owner_type_list = ['高校', '科研院所', '国有企业', '个人', '其他']
            data_json.append({
                'patent_id': data[index][1],
                'patent_type': patent_type_list[int(data[index][13]-1)],
                'patent_owner': data[index][3],
                'patent_owner_type': patent_owner_type_list[int(data[index][6])-1],
                'license_fee': data[index][9],
                'license_fee_type': data[index][11],
                'license_period': data[index][8],
                'create_time': json.loads(response_body['body'])['createTime']
            })
        return data_json

class FuJian(Reptiles_DOM):
    def collectData(self):
        n_page = self.getPageNum()
        print("共", n_page, "页")
        href_list = []
        for page_i in range(1, n_page + 1):
            rows = self.getRowNum(page_i, n_page)
            print(page_i, "页", rows, "行")
            for index in range(1, rows + 1):
                href = self.br.find_element(By.XPATH, "//body/div[4]/div[1]/div[2]/div[" + str(index) + "]/h4[1]/a[1]")
                href_list.append(href.get_attribute('href'))
            if page_i < n_page:
                self.nextPage()
        data = []
        for href in href_list:
            self.br.execute_script("window.open(arguments[0],'_self','')", href)
            data.append(self.getTuple(-1))
            self.br.back()
            time.sleep(0.1)
        variables = list(data[0].keys())
        return pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)

    def getPageNum(self):
        return int(self.br.find_element(By.XPATH, "//span[@id='tnum']").text)
    def getTuple(self, index):
        patent_id = self.br.find_element(By.XPATH, "//span[contains(text(),'专利号')]").text[4:]
        patent_owner = self.br.find_element(By.XPATH, "//span[contains(text(),'专利权人')]").text[5:]
        patent_type = self.br.find_element(By.XPATH, "//span[@class='patenttype-type']").text
        license_fee_type = self.br.find_element(By.XPATH, "//span[contains(text(),'许可费用')]").text[5:]
        license_location = self.br.find_element(By.XPATH, "//span[contains(text(),'许可地域范围')]").text[7:]
        license_deadline = self.br.find_element(By.XPATH, "//span[@id='notice_time ']").text
        return {
            'patent_id': patent_id,
            'patent_type': patent_type,
            'patent_owner': patent_owner,
            'license_deadline': license_deadline,
            'license_fee_type': license_fee_type,
            'license_location': license_location
        }

class HeBei(Reptiles_DOM):
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

    def getPageNum(self):
        try:
            self.br.find_element(By.XPATH, self.bar_xpath)
        except exceptions.NoSuchElementException:
            return 1 if len(self.br.find_element(By.XPATH, "//body/article[@id='zlsclist']/ul[1]").find_elements(By.TAG_NAME, self.bar_child_tag_name)) > 0 else 0

        bar = self.br.find_element(By.XPATH, self.bar_xpath)
        n_bar_elements = len(bar.find_elements(By.TAG_NAME, "li"))
        last_page_xpath = self.bar_xpath + "/li[" + str(n_bar_elements-1) + "]/a[1]"
        return int(self.br.find_element(By.XPATH, last_page_xpath).text)

    def collectCategoryData(self, owner_type, category_xpath):
        category_btn = self.br.find_element(By.XPATH, category_xpath)
        self.br.execute_script("arguments[0].click()", category_btn)
        n_page = self.getPageNum()
        print(owner_type, "共", n_page, "页")
        if n_page == 0:
            return
        data = []
        for page_i in range(1, n_page+1):
            menu_table = self.br.find_element(By.XPATH, "/html[1]/body[1]/article[3]/ul[1]")
            rows = len(menu_table.find_elements(By.TAG_NAME, "li"))
            print(page_i, "页", rows, "行")
            for index in range(1,rows+1):
                tuple = self.getTuple(index)
                tuple['patent_owner_type'] = owner_type
                data.append(tuple)
            if page_i < n_page:
                self.nextPage()
        variables = list(data[0].keys())
        return pd.DataFrame([[i[j] for j in variables] for i in data], columns=variables)

    def getTuple(self, index):
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

class TianJin(Reptiles_DOM):
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

class AnHui(Reptiles_DOM):
    def collectData(self):
        data = []
        rows = int(self.getRowNum(0, 1)/2)
        for index in range(1, rows+1):
            print("第", index, "行")
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
