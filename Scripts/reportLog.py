#*_*coding:utf-8*_*

import xml.dom.minidom as xmlDoc
import os
import gl
import sys
import time


class cREPORTXML(object):
    def __init__(self):
        self.__struct = self.createReportNode()

    #创建report节点
    def createReportNode(self):
        try:
            xmlD = xmlDoc.Document()

            #xml样式
            xlstNode = xmlD.createProcessingInstruction("xml-stylesheet","href=\"../../LOG.XSLT\" type=\"text/xsl\"")
            xmlD.appendChild(xlstNode)

            report = xmlD.createElement('REPORT')
            xmlD.appendChild(report)

            overStatus = xmlD.createElement('OVER_STATUS')
            overStatus.appendChild(xmlD.createTextNode(str(gl.getOverallStatus('OVER_STATUS'))))
            report.appendChild(overStatus)



            returnResult = []
            returnResult.append(xmlD)
            returnResult.append(report)
            returnResult.append(overStatus)

        except Exception,ex:
            return ex.message
        return returnResult
        '''
            def writeOverStatus(self,overStatus = 'PASSED'):
                self.__struct[2]._get_childNodes().item(0).nodeValue = overStatus
        '''

    def writeReport(self,dict,xmlPath):
        #reportNodeList = self.createReportNode()

        entry = self.createLogEntry(self.__struct[0],dict)
        self.__struct[1].appendChild(entry)

        self.writeXml(self.__struct[0],xmlPath + r'\reportLog.xml')
        #self.writeXml(self.__struct[0],gl.reporterPath+'reportxml_%s.xml'%(gl.curTimeStr))


 #-------------创建xml格式-有多个相同的节点，并且该节点下有4个名称相同的子节点----------------
        #createLogEntry(self,docObj,executeTime,stepResult,description,stepDiscription,action,index,element,value,expectResult):
    def createLogEntry(self,docObj,dict):
        entry = docObj.createElement("LOG_ENTRY")

        status = docObj.createElement("STATUS")
        nodeStep = docObj.createElement("STEP")
        nodeExecuteTime = docObj.createElement("EXECUTION_TIME")
        nodeStepResult = docObj.createElement("STEP_RESULT")
        nodeComponentName = docObj.createElement("DESCRIPTION")
        nodeStepDiscription = docObj.createElement("STEP_DESCRIPTION")
        nodeActin = docObj.createElement("ACTION")
        nodeIndex = docObj.createElement("INDEX")
        nodeElement = docObj.createElement("ELEMENT")
        nodeValue = docObj.createElement("VALUE")
        nodeExpectResult = docObj.createElement("EXPECTED_RESULTS")
        nodeimagePath = docObj.createElement('IMAGE_PATH')

        status.appendChild(docObj.createTextNode(dict['stepResult']))

        nodeStep.appendChild(docObj.createTextNode(str(dict['Step'])))
        nodeExecuteTime.appendChild(docObj.createTextNode(dict['executeTime']))
        nodeStepResult.appendChild(docObj.createTextNode(dict['stepResult']))
        nodeComponentName.appendChild(docObj.createTextNode(dict['description']))
        nodeStepDiscription.appendChild(docObj.createTextNode(dict['stepDiscription']))
        nodeActin.appendChild(docObj.createTextNode(dict['action']))
        nodeIndex.appendChild(docObj.createTextNode(dict['index']))
        nodeElement.appendChild(docObj.createTextNode(dict['element']))
        nodeValue.appendChild(docObj.createTextNode(dict['value']))
        nodeExpectResult.appendChild(docObj.createTextNode(dict['expectResult']))
        nodeimagePath.appendChild(docObj.createTextNode(dict['ImagePath']))

        entry.appendChild(status)
        entry.appendChild(nodeStep)
        entry.appendChild(nodeExecuteTime)
        entry.appendChild(nodeStepResult)
        entry.appendChild(nodeComponentName)
        entry.appendChild(nodeStepDiscription)
        entry.appendChild(nodeActin)
        entry.appendChild(nodeIndex)
        entry.appendChild(nodeElement)
        entry.appendChild(nodeValue)
        entry.appendChild(nodeExpectResult)
        entry.appendChild(nodeimagePath)
        return entry


    #参数，xml对象，准备存储xml文件路径，文件模式：读 and 写 (r and w)
    def writeXml(self,xmlDoc,xmlPath):
        f = open(xmlPath,"w")
        xmlDoc.writexml(f,indent='\t', addindent='\t', newl='\n', encoding="utf-8")
        f.close()




if __name__=='__main__':
     #createLogEntry(self,docObj,executeTime,stepResult,description,stepDiscription,action,index,element,value,expectResult):
    curTime = time.strftime('%Y.%m.%d %H:%M:%S',time.localtime())
    print(curTime)
    dict = {
            'step':'',
            'executeTime':curTime,
            'stepResult':'PASSED',
            'description':'普惠家登录',
            'stepDiscription':"输入'用户名'",
            'action':'input',
            'index':'By.XPATH',
            'element':"//Input[@id='userName']",
            'value':'msh195',
            'expectResult':'输入用户名'}

    reportx =cREPORTXML()
    reportx.writeReport(dict)
