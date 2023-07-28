from LOR import AnHui, TianJin, HeBei, FuJian, JiangSu, ShanDong, SiChuan, LiaoNing, HuBei, GuangDong, BeiJing, ZheJiang, ShangHai, ShaanXi, GuangXi, HaiNan, HuNan
import os

if __name__=='__main__':
    base_path="D:/专利许可与诉讼/LOR"

    # AH = AnHui(
    #     website='http://www.91ipr.com/openpatlist.jsp',
    #     nextpage_xpath="",
    #     totalnum_xpath="")
    # print("安徽")
    # AH.start()
    # AH.exportData(os.path.join(base_path,"安徽省.xlsx"))

    # TJ = TianJin(
    #     website='https://www.cnipol.com/LicenseTrading/getLicenseList.html',
    #     nextpage_xpath="//a[contains(text(),'下一页')]",
    #     totalnum_xpath=""
    # )
    # print("天津")
    # TJ.start()
    # TJ.exportData(os.path.join(base_path,"天津省.xlsx"))

    # HB = HeBei(
    #     website='https://www.hbips.com/portal/trademark/patentdatabase.html',
    #     nextpage_xpath="//a[contains(text(),'»')]",
    #     totalnum_xpath=""
    # )
    # print("河北")
    # HB.start()
    # HB.exportData(os.path.join(base_path,"河北省.xlsx"))

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # FJ = FuJian(
    #     website='https://zscq.hxee.com.cn/html/list-content-56935181411645444219.html',
    #     nextpage_xpath="//a[contains(text(),'下一页')]",
    #     totalnum_xpath=""
    # )
    # print("福建")
    # FJ.start()
    # FJ.exportData(os.path.join(base_path,"福建省.xlsx"))

    # SD = ShanDong(
    #     website='http://pom.sdips.com.cn/Web/PatentOGL.aspx',
    #     nextpage_xpath="//a[contains(text(),'下一页')]",
    #     totalnum_xpath=""
    # )
    # print("山东")
    # SD.start()
    # SD.exportData(os.path.join(base_path,"山东省.xlsx"))

    # SC = SiChuan(
    #     website='http://yyxt.cipnet.cn/#/openLicense',
    #     nextpage_xpath="//body/div[@id='app']/div[2]/div[2]/div[2]/div[1]/div[1]/div[8]/div[1]/button[2]",
    #     totalnum_xpath="/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[8]/div[1]/span[1]",
    #     pagenum_xpath= "//body/div[@id='app']/div[2]/div[2]/div[2]/div[1]/div[1]/div[8]/div[1]/ul[1]",
    #     rownum_xpath= "/html[1]/body[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[7]/div[1]/div[3]/table[1]/tbody[1]",
    #     rownum_class_name= "el-table__row"
    # )
    # print("四川")
    # SC.start()
    # SC.exportData(os.path.join(base_path,"四川省.xlsx"))

    # 数据获取不全，有“暂无”
    # LN = LiaoNing(
    #     website='https://www.lnipa.cn/#/operate/patent_supply_mall',
    #     nextpage_xpath="//body/div[@id='app']/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/button[2]",
    #     pagenum_xpath="//body/div[@id='app']/div[1]/div[1]/div[2]/div[2]/div[3]/div[2]/ul[1]",
    #     rownum_xpath="//body/div[@id='app']/div[1]/div[1]/div[2]/div[2]/div[3]/div[1]",
    #     rownum_class_name="psm_item",
    #     totalnum_xpath=""
    # )
    # print("辽宁")
    # LN.start()
    # LN.exportData(os.path.join(base_path,"辽宁省.xlsx"))

    # GD = GuangDong(
    #     website='https://zlxk.gpic.gd.cn/#/licensingPatent',
    #     nextpage_xpath="/html//el-content-right[@id='content-wrapper-right']//div[@class='el-pagination is-background']/button[2]",
    #     pagenum_xpath="/html//el-content-right[@id='content-wrapper-right']//ul[@class='el-pager']",
    #     rownum_xpath="//div[@id='tableColumn']//table[@class='el-table__body']",
    #     rownum_class_name="el-table__row",
    #     totalnum_xpath=""
    # )
    # print("广东")
    # GD.start()
    # GD.exportData(os.path.join(base_path,"广东省.xlsx"))

    # BJ = BeiJing(
    #     website='https://patentol.ctex.cn/',
    #     nextpage_xpath="//a[contains(text(),'下一页')]",
    #     pagenum_xpath="",
    #     rownum_xpath="",
    #     rownum_class_name="",
    #     totalnum_xpath=""
    # )
    # print("北京")
    # BJ.start()
    # BJ.exportData(os.path.join(base_path,"北京省.xlsx"))

    # 数据量太大，内存不够
    # ZJ = ZheJiang(
    #     website='https://www.zjipx.com/kfxk.html#/kfxkList',
    #     nextpage_xpath="//body/div[@id='app']/div[1]/div[2]/div[1]/div[5]/div[1]/div[1]/div[2]/ul[1]/li[10]",
    #     pagenum_xpath="//body/div[@id='app']/div[1]/div[2]/div[1]/div[5]/div[1]/div[1]/div[2]/ul[1]",
    #     rownum_xpath="//body/div[@id='app']/div[1]/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/ul[1]",
    #     rownum_class_name="",
    #     totalnum_xpath=""
    # )
    # print("浙江")
    # ZJ.start()
    # ZJ.exportData(os.path.join(base_path,"浙江省.xlsx"))

    # SH = ShangHai(
    #     website='https://www.shsipe.com/property-page/#/openlist',
    #     nextpage_xpath="//body/div[@id='app']/div[1]/div[2]/div[15]/div[1]/button[2]",
    #     pagenum_xpath="//body/div[@id='app']/div[1]/div[2]/div[15]/div[1]/ul[1]",
    #     rownum_xpath="",
    #     rownum_class_name="",
    #     totalnum_xpath=""
    # )
    # print("上海")
    # SH.start()
    # SH.exportData(os.path.join(base_path,"上海省.xlsx"))

    SX = ShaanXi(
        website='https://www.jmrhip.com/#lic_paten',
        nextpage_xpath="//div[@id='router_main_view']/d-include//d-pagination/d-pagination-num/d-text[@class='num-next']",
        pagenum_xpath="d-pagination > d-text",
        rownum_xpath="",
        rownum_class_name="",
        totalnum_xpath=""
    )
    print("陕西")
    SX.start()
    SX.exportData(os.path.join(base_path,"陕西省.xlsx"))





