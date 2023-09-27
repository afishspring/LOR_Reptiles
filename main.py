from LOR import AnHui, TianJin, HeBei, FuJian, JiangSu, ShanDong, SiChuan, LiaoNing, HuBei, GuangDong, BeiJing, ZheJiang, ShangHai, ShaanXi, GuangXi, HaiNan, HuNan
import os
import re
import pandas as pd
def process_file(file_path):
    province = os.path.splitext(os.path.basename(file_path))[0][:2]
    df = pd.read_excel(file_path)
    df['province'] = province
    return df


def extract_middle_12_digits(patent_id_string):
    pattern = r'(?:CN|ZL|zl)?(\d{12})(?:\.\d)?'
    matches = re.findall(pattern, patent_id_string, flags=re.IGNORECASE)

    return matches

if __name__=='__main__':
    base_path = "data"

    # AH = AnHui(
    #     website='http://www.91ipr.com/openpatlist.jsp',
    #     table_xpath="//tbody",
    #     table_tuple_type="tag name",
    #     table_tuple_class_name="tr"
    # )
    # print("安徽")
    # AH.start()
    # AH.exportData(os.path.join(base_path,"安徽省.xlsx"))

    # TJ = TianJin(
    #     website='https://www.cnipol.com/LicenseTrading/getLicenseList.html',
    #     next_page_xpath="//a[contains(text(),'下一页')]",
    #     bar_xpath="//body/section[2]/div[3]",
    #     bar_child_tag_name="a",
    #     n_page_offset=2,
    #     table_xpath="//tbody",
    #     table_tuple_type= "tag name",
    #     table_tuple_class_name="tr"
    # )
    # print("天津")
    # TJ.start()
    # TJ.exportData(os.path.join(base_path,"天津省.xlsx"))

    # HB = HeBei(
    #     website='https://www.hbips.com/portal/trademark/patentdatabase.html',
    #     next_page_xpath="//a[contains(text(),'»')]",
    #     bar_xpath="//body/ul[1]/ul[1]",
    #     bar_child_tag_name="li",
    #     n_page_offset=1,
    #     table_xpath="//body/article[@id='zlsclist']/ul[1]",
    # )
    # print("河北")
    # HB.start()
    # HB.exportData(os.path.join(base_path,"河北省.xlsx"))

    # FJ = FuJian(
    #     website='https://zscq.hxee.com.cn/html/list-content-56935181411645444219.html',
    #     next_page_xpath="//a[contains(text(),'下一页')]",
    #     table_xpath="//body/div[4]/div[1]/div[2]",
    #     table_tuple_class_name="project-wrap"
    # )
    # print("福建")
    # FJ.start()
    # FJ.exportData(os.path.join(base_path,"福建省.xlsx"))

    # 江苏，专利权人类型不明确
    # JS = JiangSu(
    #     website='https://www.jsipp.cn/zhfw/app/zhfw.app?id=SY&:pageCache=createPage&:newData=true&:drillPage=%2Fzhfw%2Fapp%2Fzhfw.app%2Fzhfw%2FYPTJY%2FZLKFXK%2FKFXK_ALL.spg%3F:newData%3Dtrue&:drillPageTitle=%E5%BC%80%E6%94%BE%E8%AE%B8%E5%8F%AF%E5%88%97%E8%A1%A8',
    #     next_page_xpath="//span[contains(text(),'下一页')]",
    #     bar_xpath="//body/div[1]/div[1]/div[5]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]",
    #     bar_child_tag_name="span",
    #     n_page_offset=3,
    #     xhr_pattern="queryData"
    # )
    # print("江苏")
    # JS.start()
    # JS.exportData(os.path.join(base_path,"江苏省.xlsx"))

    # SD = ShanDong(
    #     website='http://pom.sdips.com.cn/Web/PatentOGL.aspx',
    #     next_page_xpath="//a[contains(text(),'下一页')]",
    #     table_xpath="//body/div[3]/div[1]/div[2]/form[1]/ul[1]",
    #     table_tuple_class_name="clearfix"
    # )
    # print("山东")
    # SD.start()
    # SD.exportData(os.path.join(base_path,"山东省.xlsx"))

    # SC = SiChuan(
    #     website='http://yyxt.cipnet.cn/#/openLicense',
    #     next_page_xpath="//body/div[@id='app']/div[2]/div[2]/div[2]/div[1]/div[1]/div[8]/div[1]/button[2]",
    #     bar_xpath="//body/div[@id='app']/div[2]/div[2]/div[2]/div[1]/div[1]/div[8]/div[1]/ul[1]",
    #     bar_child_tag_name="li",
    #     xhr_pattern="listopenlicense?page="
    # )
    # print("四川")
    # SC.start()
    # SC.exportData(os.path.join(base_path,"四川省.xlsx"))

    # LN = LiaoNing(
    #     website='https://www.lnipa.cn/#/operate/patent_supply_mall',
    #     next_page_xpath="//body/div[@id='app']/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/button[2]",
    #     bar_xpath="//body/div[@id='app']/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/ul[1]",
    #     bar_child_tag_name="li",
    #     xhr_pattern="all_pass_page?page="
    # )
    # print("辽宁")
    # LN.start()
    # LN.exportData(os.path.join(base_path,"辽宁省.xlsx"))

    # 网站登录不稳定，数据收集可能不全
    # GD = GuangDong(
    #     website='https://zlxk.gpic.gd.cn/#/licensingPatent',
    #     next_page_xpath="/html//el-content-right[@id='content-wrapper-right']/div[@class='pagination-container']//input[@type='number']",
    #     bar_xpath="/html//el-content-right[@id='content-wrapper-right']//ul[@class='el-pager']",
    #     bar_child_tag_name="li",
    #     xhr_pattern="list?page="
    # )
    # print("广东")
    # GD.start()
    # GD.exportData(os.path.join(base_path,"广东省.xlsx"))

    # BJ = BeiJing(
    #     website='https://patentol.ctex.cn/',
    #     next_page_xpath="//a[contains(text(),'下一页')]"
    # )
    # print("北京")
    # BJ.start()
    # BJ.exportData(os.path.join(base_path,"北京省.xlsx"))

    # 数据量太大，内存不够
    ZJ = ZheJiang(
        website='https://www.zjipx.com/kfxk.html#/kfxkList',
        next_page_xpath="/html//div[@id='app']//div[@class='ant-spin-nested-loading']/div[@class='ant-spin-container']//ul[@class='ant-pagination']/li[@title='下一页']",
        bar_xpath="//body/div[@id='app']/div[1]/div[2]/div[1]/div[5]/div[1]/div[1]/div[2]/ul[1]",
        bar_child_tag_name="li",
        n_page_offset=2
    )
    print("浙江")
    ZJ.start()
    ZJ.exportData(os.path.join(base_path,"浙江省_charge.xlsx"))

    # SH = ShangHai(
    #     website='https://www.shsipe.com/property-page/#/openlist',
    #     next_page_xpath="//body/div[@id='app']/div[1]/div[2]/div[15]/div[1]/button[2]",
    #     bar_xpath="//body/div[@id='app']/div[1]/div[2]/div[15]/div[1]/ul[1]",
    #     bar_child_tag_name="li",
    #     xhr_pattern="newsPage?page="
    # )
    # print("上海")
    # SH.start()
    # SH.exportData(os.path.join(base_path,"上海省.xlsx"))

    # SX = ShaanXi(
    #     website='https://www.jmrhip.com/#lic_paten',
    #     next_page_xpath="//div[@id='router_main_view']/d-include//d-pagination/d-pagination-num/d-text[@class='num-next']",
    #     bar_xpath="d-pagination > d-text",
    #     xhr_pattern="pageNo="
    # )
    # print("陕西")
    # SX.start()
    # SX.exportData(os.path.join(base_path,"陕西省.xlsx"))

    # GX = GuangXi(
    #     website='https://zlkfxk.bbwcq.com/kfxkzl.jhtml',
    #     next_page_xpath="//body/section[1]/div[1]/div[1]/div[4]/div[1]/div[1]/button[2]",
    #     bar_xpath="//body/section[1]/div[1]/div[1]/div[4]/div[1]/div[1]/ul[1]",
    #     bar_child_tag_name="li",
    #     n_page_offset=0,
    #     xhr_pattern="page="
    # )
    # print("广西")
    # GX.start()
    # GX.exportData(os.path.join(base_path,"广西省.xlsx"))

    # HN = HaiNan(
    #     website='https://qszr.ipeh.com.cn/quanshu/specialproject/show.html?id=23',
    #     next_page_xpath="//div[contains(text(),'>')]",
    #     bar_xpath="//div[@id='page-box']",
    #     bar_child_tag_name="div",
    #     n_page_offset=2,
    #     xhr_pattern="show.html?id=23"
    # )
    # print("海南")
    # HN.start()
    # HN.exportData(os.path.join(base_path,"海南省.xlsx"))

    # HuN = HuNan(
    #     website='http://124.232.165.110:32380/patentopen/#/patent',
    #     next_page_xpath="//body/div[@id='app']/div[2]/div[2]/div[1]/button[2]",
    #     bar_xpath="//body/div[@id='app']/div[2]/div[2]/div[1]/ul[1]",
    #     bar_child_tag_name="li",
    #     n_page_offset=0,
    #     xhr_pattern="getPatentopenList"
    # )
    # print("湖南")
    # HuN.start()
    # HuN.exportData(os.path.join(base_path,"湖南省.xlsx"))

    # all_data = []

    # for filename in os.listdir(base_path):
    #     if filename.endswith('省.xlsx'):
    #         file_path = os.path.join(base_path, filename)
    #         data = process_file(file_path)
    #         all_data.append(data)

    # # 合并所有文件的数据
    # final_data = pd.concat(all_data, ignore_index=True)

    # final_data['patent_id'] = final_data['patent_id'].apply(extract_middle_12_digits)

    # final_data = final_data.explode('patent_id')

    # final_data.reset_index(drop=True, inplace=True)

    # final_data.rename(columns={'patent_id': 'appln_nr'}, inplace=True)

    # final_data.to_excel(os.path.join(base_path, 'lor_data.xlsx'), index=False)