#-*-coding=utf-8-*-

import gl
import os
#gl.init()
gl.setOverallStatus('userName','msh195')
gl.getOverallStatus('userName')
print gl.Dict()


def f(func):
    def war(*args,**kwargs):
        print('after')
        return func(*args,**kwargs)
    return war

@f
def xz():
    print('1231412434555556')

xz()


def isExistPath(xPath):
    if not os.path.exists(xPath):
        os.mkdir(xPath)
    else:
        print('path is exist:'+xPath)

str = r'd:\PHJ\Reporter\LOGS'
#报告文件路径
reporPath = os.path.join(str,'report')
isExistPath(reporPath) #创建文件夹

print(reporPath)

imgPath = os.path.join(reporPath,'\\Image')
print(imgPath)

def isNumeric(value):
    try:
        tv = float(value)
        return int(tv)
    except ValueError:
        return value

print(isNumeric('12313.98'))