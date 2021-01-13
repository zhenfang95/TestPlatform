# -*- coding:utf-8 -*-

import unittest
from MyApp.A_WQRFhtmlRunner import HTMLTestRunner

class Test(unittest.TestCase):
    '测试类'
    def demo(self,step):
        print(step.api_url)

def make_defself(step):
    def tool(self):
        Test.demo(self,step)
    setattr(tool,"__doc__",u"%s"%step.name)
    return tool

def make_def(steps):
    for i in range(len(steps)):
        setattr(Test,'test_'+str(steps[i].index).zfill(3),make_defself(steps[i]))   #保持执行顺序正确,而用法就是字符串.zfill(固定长度)

def run(Case_id,Case_name,steps):
    make_def(steps)
    suit = unittest.makeSuite(Test)
    filename = 'MyApp/templates/Reports/%s.html'%Case_id
    fp = open(filename,'wb')
    runner = HTMLTestRunner(fp,title='接口测试报告:%s'%Case_name,description='用例描述')
    runner.run(suit)