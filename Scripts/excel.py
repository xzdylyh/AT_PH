#*_*coding:utf-8*_*
import xlrd as excel
import json
import gc #垃圾回收
import os
import gl
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#Excel操作
class Excel(object):

    def __init__(self,file='file.xls'):
        self.Data = self.OpenExcel(file) #创建EXcel工作表对象

    #创建workbook对象
    def OpenExcel(self,file='file.xls'):
        try:
            data = excel.open_workbook(file)
            data.encoding = 'GB2312'
            return  data
        except Exception,ex:
            print str(ex)

    #获取指定行数据,返回数组
    def getRowData(self,rownum =0):
        try:
            table = self.Data.sheet_by_index(0)
        except Exception,ex:
            return ex.message()
        return table.row_values(rownum)

    #获取所有数据每行一个字典对象，存储在list中
    def getAllData(self,startRowNum=1,sheetName = 'Sheet1'):
        sheet = self.Data.sheet_by_name(sheetName) #根扰sheet名获取sheet表对象
        rowCount = sheet.nrows #所有行
        colCount = sheet.ncols #所有列
        colTitle = sheet.row_values(startRowNum) #指定行号所有行数据，以list返回

        list = [] #存储所有行数据，每行一个字典对象
        for rowNum in range(startRowNum+1,rowCount):
            dict = {} #存储当前行的数据
            rowValue = sheet.row_values(rowNum)
            for value in range(len(rowValue)):
                dict[colTitle[value]] = self.isNumeric(rowValue[value])
            list.append(dict)

        return list

    #判断字符串内容是否为数字，是的话转成int
    def isNumeric(self,value):
        try:
            tv=float(value)
            return int(tv)
        except ValueError:
            return value

if __name__=="__main__":
    xlsPath = os.path.join(gl.dataPath,'TestCase.xlsx')
    print(xlsPath)
    xls = Excel(xlsPath)
    print xls.getRowData(5)

    print(xls.getAllData(startRowNum=5))






