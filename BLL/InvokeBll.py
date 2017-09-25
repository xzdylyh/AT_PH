#-*-coding=utf-8-*-
from Scripts import BaseScript
from Scripts import excel as ex
from Scripts import gl
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ph_bll(object):

    #入口
    def Launch_Page(self):
        webStart = BaseScript.ph_web()  #driver对象
        #遍历，数据表，行数据进行执行动作
        for dictRunData in self.loadTestData(sheetName='Run'): #执行标志Sheet
            if str.upper(str(dictRunData['flag']))=='Y' and str.upper(str(dictRunData['Sheet Name']))!='LOGIN': #run标志，执行配置表中，模块执行标志
                self.runFuncModule(webStart,'Login') #执行登录模块
                self.runFuncModule(webStart,dictRunData['Sheet Name'])

        #webStart.driver.quit()关闭所有IE浏览器

    #功能模块遍历执行
    def runFuncModule(self,webStart,sheetName):
        for dictData in self.loadTestData(str(sheetName)): #遍历功能模块表
            print(dictData)
            if str.upper(str(dictData['action']))=='GET':
                gl.setOverallStatus('browserSelect',str(dictData['Element'])) #设置，要启动的浏览器类型
                webStart.toUrl(str(dictData['Value'])) #打开login页面
                continue

            if str.upper(str(dictData['flag']))=='Y':
                gl.setOverallStatus('description',dictData['Description'])
                gl.setOverallStatus('stepDiscription',dictData['step Description'])
                gl.setOverallStatus('expectResult',dictData['Expected Results '])
                gl.setOverallStatus('Step',int(dictData['Step']))
                webStart.Find_Element(element=dictData['Element'],index=dictData['Index'],value=dictData['Value'],action=dictData['action'])
                    #有报错，停止执行
            if str.upper(gl.getOverallStatus('stepResult')) =='FAILED':
                break
        #除了登录功能，其它模块执行完，关闭浏览器
        if str.upper(str(sheetName))!='LOGIN':
            webStart.driver.quit()#功能执行完关闭浏览器


    #获取测试用例数据，返回list[dict,dict,.......,dict]
    #dict存储一行数据,key为列名
    def loadTestData(self,sheetName):
        xls = ex.Excel(gl.xlsPath)
        listData = xls.getAllData(startRowNum=5,sheetName=sheetName)
        return listData


if __name__=="__main__":
    ph_bll().Launch_Page()
