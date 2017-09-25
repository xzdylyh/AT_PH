#-*-coding=utf-8-*-
try:
    import os
    from selenium import webdriver
    from selenium.webdriver import ActionChains #鼠标操作
    from selenium.webdriver.common.keys import Keys #键盘操作
    from selenium.common.exceptions import NoSuchElementException,TimeoutException #异常
    from selenium.webdriver.support.ui import WebDriverWait #等待元素
    from selenium.webdriver.support import expected_conditions as ec #条件，配合webDriverWait
    from selenium.webdriver.common.by import By
    from Scripts import reportLog
    from Scripts import gl
    import time
except ImportError,ex:
    print(ex.message)

class ph_web(object):
    def __init__(self):
        #self.url ='https://test.puhuijia.com/phjpc-web-front/login_8.html'
        self.driver = self.browserSelect() #实例化，driver对象
        self.reportx =reportLog.cREPORTXML() #报告实例

    #转到url页
    def toUrl(self,url):
        self.driver.get(url)

    #浏览器选择
    def browserSelect(self):
        if str(gl.getOverallStatus('browserSelect')).lower()=='ie':
            return webdriver.Ie() #返回必须带括号，否则调用时，需要重新实例化 比如这里不加括号，sele.driver(),get(url)就需要这么用driver()
        if str(gl.getOverallStatus('browserSelect')).lower()=='chrome':
            return webdriver.Chrome()
        if str(gl.getOverallStatus('browserSelect')).lower()=='firefox':
            return webdriver.Firefox()


    #装饰器，作用在函数前，或在后做点什么，哈……
    def WriteReport_After(func):
        def report(*args,**kwargs):
            ret = func(*args,**kwargs)

            gl.setOverallStatus('action',kwargs.get('action','None'))
            gl.setOverallStatus('element',kwargs.get('element','None'))
            gl.setOverallStatus('value',kwargs.get('value','None'))

            return ret
        return report

    #获取当前系统时间
    def getCurTime(self):
        curTimeStr = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime()).decode('utf-8')
        return curTimeStr

    #生成报告路径
    def reportPathCreate(self):
        list = []
        #报告文件路径
        reporPath = os.path.join(gl.reporterPath,gl.curTimeStr)
        self.isExistPath(reporPath) #创建文件夹
        gl.setOverallStatus('reportPath',reporPath)

        imgPath = os.path.join(reporPath,'Image')
        self.isExistPath(imgPath) #创建image文件夹

        list.append(reporPath)
        list.append(imgPath)
        return list

    #初始化报告值
    def setReportDictVal(self,index,action,element,value,status,msg):
        gl.setOverallStatus('executeTime',self.getCurTime())
        gl.setOverallStatus('index',index)
        gl.setOverallStatus('action',action)
        gl.setOverallStatus('element',element)
        gl.setOverallStatus('value',value)
        gl.setOverallStatus('stepResult',status)
        if msg!='':
            gl.setOverallStatus('stepDiscription',msg)


    #找页面元素
    #@WriteReport_After
    def Find_Element(self,index='By.XPATH',element='',value='',action=''):
        action = str(action)
        element = str(element)
        index = str(index)
        value = str(value)
        #报告文件路径
        reporPath =self.reportPathCreate()
        try:
            WebDriverWait(self.driver,10,1).until(ec.presence_of_element_located((self.switchBy(index),element)))
            if str.lower(str(index))!='':
                ement = self.driver.find_element(self.switchBy(index),element)
            else:
                ement = element
            #选择，执行的操作方式
            if str.lower(str(action))=='switch_to':
                self.switch_to(index,action,ement) #swicth to切换操作
            elif str.lower(str(action))=='driver':
                self.driver_Action(ement,action,value)
            else:
                self.mouse_Action(ement,action,value) #操作

            #写日志
            self.setReportDictVal(index,action,element,value,'PASSED','')
            imgPath = reporPath[1]+r'\image_'+self.getCurTime()+'.png'
            if str.lower(action)=='verify':
                self.driver.save_screenshot(imgPath)
                gl.setOverallStatus('ImagePath',imgPath)

            self.reportx.writeReport(gl.Dict(),reporPath[0])
            gl.setOverallStatus('ImagePath','')
        except (NoSuchElementException,TimeoutException),ex:
            #写日志
            self.setReportDictVal(index,action,element,value,'FAILED',ex.message)
            imgPath = reporPath[1]+r'\image_'+self.getCurTime()+'.png'
            self.driver.save_screenshot(imgPath)
            gl.setOverallStatus('ImagePath',imgPath)
            gl.setOverallStatus('OVER_STATUS','FAILED')
            self.reportx.writeReport(gl.Dict(),reporPath[0])

    '''
    #function:判断路径是否存在，不存在创建
    #parameter:要校验或被创建路径
    '''
    def isExistPath(self,xPath):
        if not os.path.exists(xPath):
            os.mkdir(xPath)
        else:
            print('path is exist:'+xPath)

    #driver方法封装
    def driver_Action(self,element,action,value):
        if str.lower(action) =='driver' and str.lower(element) =='add_cookie': #增加cookies
            self.driver.add_cookie(eval(value))
        if str.lower(action) =='driver' and str.lower(element) =='close': #关闭当前浏览器
            self.driver.close()
        if str.lower(action) =='driver' and str.lower(element) =='back': #浏览器，向前
            self.driver.back()
        if str.lower(action) =='driver' and str.lower(element) =='create_web_element': #创建web元素 传id
            self.driver.create_web_element(element_id=value)
        if str.lower(action) =='driver' and str.lower(element) =='current_url': #获取当前url
            return self.driver.current_url
        if str.lower(action) =='driver' and str.lower(element) =='current_window_handle':#获取当前window聚丙
            return  self.driver.current_window_handle
        if str.lower(action) =='driver' and str.lower(element) =='delete_all_cookies':#删除所有cookies
            self.driver.delete_all_cookies()
        if str.lower(action) =='driver' and str.lower(element) =='delete_cookie':#删除指定name的cookies
            self.driver.delete_cookie(str(value))
        if str.lower(action) =='driver' and str.lower(element) =='execute_script': #执行，js脚本
            return self.driver.execute_script(str(value))
        if str.lower(action) =='driver' and str.lower(element) =='window_handles':#获取所有窗口聚丙
            return self.driver.window_handles
        if str.lower(action) =='driver' and str.lower(element) =='title':#获取浏览器标题
            return self.driver.title
        if str.lower(action) =='driver' and str.lower(element) =='set_window_size':#当前窗口大小
            sws = str(value).split(',')
            self.driver.set_window_size(sws[0],sws[1])
        if str.lower(action) =='driver' and str.lower(element) =='set_page_load_timeout': #设置页面加载超时时间
            self.driver.set_page_load_timeout(value)
        if str.lower(action) =='driver' and str.lower(element) =='save_screenshot': #截图
            self.driver.save_screenshot(element)
        if str.lower(action) =='driver' and str.lower(element) =='set_window_rect':#设置窗口位置及大小
            swr = str(value).split(',')
            self.driver.set_window_rect(swr[0],swr[1],swr[2],swr[3]) #x,y,w,h

    '''
    #function:鼠标操作
    #parameter:元素对象，动作(click、doubleclick等)，值(发送按键或坐标要用)
    '''
    def mouse_Action(self,element,action,value = ''):
        if  str.lower(action) == 'click': #单击
            element.click()
        if str.lower(action)=='clear': #清除
            element.clear()
        if str.lower(action) =='input': #输入；并且输入前先清除
            element.clear()
            element.send_keys(value)
        if str.lower(action) =='rightclick': #右键单击
            ActionChains(self.driver).context_click(element).perform()
        if str.lower(action)=='doubleclick': #左键双击
            ActionChains(self.driver).double_click(element).perform()
        if str.lower(action)=='clickhold': #左键按下
            ActionChains(self.driver).click_and_hold(element).perform()
        if str.lower(action)=='drag_and_drop': #拖拽
            ele = str(element).split('@_@')
            ActionChains(self.driver).drag_and_drop(ele[0],ele[1]).perform()
        if str.lower(action)=='drag_and_drop_by_offset': #将一个元素，拖拽到x,y位置
            ele = str(value).split(',')
            ActionChains(self.driver).drag_and_drop_by_offset(element,ele[0],ele[1]).perform()
        if str.lower(action)=='move_by_offset': #按坐标移动
            ele = str(value).split(',')
            ActionChains(self.driver).move_by_offset(ele[0],ele[1]).perform()
        if str.lower(action)=='move_to_element': #移动到元素位置
            ActionChains(self.driver).move_to_element(element).perform()
        if str.lower(action)=='move_to_element_with_offset': #从元素位置，移动到坐标位置
            ele = str(value).split(',')
            ActionChains(self.driver).move_to_element_with_offset(element,ele[1],ele[2]).perform()
        if str.lower(action)=='send_keys': #发送按键
            ActionChains(self.driver).send_keys(value).perform()
        if str.lower(action)=='input': #发送内容到元素
            element.clear()
            ActionChains(self.driver).send_keys_to_element(element,value).perform()

    #switch元素，切换
    def switch_to(self,index='',action='switch_to',element=''):
        if str.lower(action)=='switch_to' and str.lower(index)=='window':
            self.driver.switch_to.window(str(element))
        if str.lower(action)=='switch_to' and str.lower(index)=='frame':
            self.driver.switch_to.frame(element)
        if str.lower(action)=='switch_to' and str.lower(index)=='default_content':
            self.driver.switch_to.default_content()
        if str.lower(action)=='switch_to' and str.lower(index)=='active_element':
            self.driver.switch_to.active_element()
        if str.lower(action)=='switch_to' and str.lower(index)=='alert':
            self.driver.switch_to.alert()
        if str.lower(action)=='switch_to' and str.lower(index)=='parent_frame':
            self.driver.switch_to.parent_frame()

    '''
    #将字By对象名字符串转换为By对象
    #By.xPath 等对象名字符串
    '''
    def switchBy(self,index):
        index = str(index)
        if str.upper(index)=='BY.XPATH':
            return By.XPATH
        if str.upper(index)=='BY.ID':
            return By.ID
        if str.upper(index)=='BY.NAME':
            return By.NAME
        if str.upper(index)=='BY.LINK_TEXT':
            return By.LINK_TEXT
        if str.upper(index) =='BY.CLASS_NAME':
            return By.CLASS_NAME
        if str.upper(index) =='BY.CSS_SELECTOR':
            return By.CSS_SELECTOR
        if str.upper(index) =='BY.TAG_NAME':
            return By.TAG_NAME
        if str.upper(index)=='BY.PARTIAL_LINK_TEXT':
            return By.PARTIAL_LINK_TEXT





if __name__=="__main__":
    webStart = ph_web()
    webStart.toUrl()
    webStart.Find_Element(element="//Input[@id='userName']",value='msh195',action='input')
    webStart.Find_Element(element="//Input[@id='password']",value='112233',action='input')
    webStart.Find_Element(index=By.LINK_TEXT,element='立即登录',action='click')
    #webStart.driver.quit()