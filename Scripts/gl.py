#_*_coding:utf-8_*_
import os
import sys
import time
global dataPath #dataĿ¼
global rootPath #���̸�Ŀ¼
global scriptPath #ScriptsĿ¼
global reporterPath #reporterĿ¼
global logsPath #logsĿ¼
global BIIPath #BIIĿ¼
global projectPath #��ĿĿ¼
global curTime #��ǰ����ʱ��
global stepNumber #������
global curTimeStr
overStatus = 'PASSED'

curTimeStr = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime()).decode('utf-8')
curTime = time.strftime('%Y.%m.%d %H:%M:%S',time.localtime()).decode('utf-8')
projectPath = os.path.dirname(os.getcwd())+"\\"
rootPath = os.getcwd().split('\\')[0]+'\\'
reporterPath = projectPath+'Reporter\\LOGS\\'
logsPath = projectPath+'logs\\'
dataPath = projectPath+'Data\\'
scriptPath = os.getcwd()+'\\'

xlsPath = os.path.join(dataPath,'TestCase.xlsx')

_overallStatusDict = {
            'executeTime':'',
            'stepResult':'',
            'description':'',
            'stepDiscription':'',
            'action':'',
            'index':'',
            'element':'',
            'value':'',
            'expectResult':'None',
            'ImagePath':'',
            'reportPath':'',
            'browserSelect':'Ie',
            'OVER_STATUS':'PASSED'
}

#���ļ�ʹ�ñ���
def init():
    global _overallStatusDict
    _overallStatusDict = {}

def setOverallStatus(key,value):
    _overallStatusDict[key]=value

def getOverallStatus(key):
    return _overallStatusDict[key]

def Dict():
    return _overallStatusDict




if __name__=="__main__":
    print curTime
    print projectPath
    print dataPath
    print rootPath
    print scriptPath
    print reporterPath
    print logsPath