from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import tkinter
from tkinter.messagebox import *
from time import sleep
import time
import os
# 读取学号密码
from selenium.webdriver.common.by import By
from tkinter import *


def infoInput():
    root = Tk()
    root.title("初次使用，请输入信息")
    root.geometry("300x200")
    Label(root, text='学号').grid(row=0, column=0)  # label：文本
    Label(root, text='密码').grid(row=1, column=0)  # grid：表格结构
    Label(root, text='定时时间(0~23)').grid(row=2, column=0)  # grid：表格结构
    Label(root, text='扫描间隔(s)').grid(row=3, column=0)  # grid：表格结构

    number = StringVar()  # 设置了这个可以设置输入的属性
    password = StringVar()
    time = StringVar(value="8")
    scanFreq = StringVar(value="10")

    e1 = Entry(root, textvariable=number).grid(row=0, column=1, padx=10, pady=5)  # entry：输入框
    e2 = Entry(root, textvariable=password, show='*').grid(row=1, column=1, padx=10, pady=5)  # 想显示什么就show=
    e3 = Entry(root, textvariable=time, show='8').grid(row=2, column=1, padx=10, pady=5)  # 想显示什么就show=
    e4 = Entry(root, textvariable=scanFreq, show='').grid(row=3, column=1, padx=10, pady=5)  # 想显示什么就show=

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def show():
        n = number.get()
        p = password.get()
        t = time.get()
        s = scanFreq.get()
        if n == "" or p == "" or t == "" or s == "":
            showerror(title='Error', message='输入不完整！')
            return
        if not is_number(t) or not is_number(s) or int(t) < 0 or int(t) > 23:
            window = tkinter.Tk()
            window.withdraw()  # 退出默认 tk 窗口
            showerror(title='Error', message='输入值类型或范围不正确！')
            return
        with open('./user.txt', 'a') as f:
            f.write(n + '\n' + p + '\n' + t + '\n' + s)
        f.close()
        root.destroy()

    Button(root, text='提交', width=10, command=show) \
        .grid(row=4, column=0, sticky=W, padx=10, pady=10)
    Button(root, text='退出', width=10, command=root.quit) \
        .grid(row=4, column=1, sticky=E, padx=10, pady=10)

    root.mainloop()


if __name__ == '__main__':
    if not os.path.exists('./user.txt'):
        infoInput()
    with open('./user.txt', 'r') as f:
        account = f.read()
        number, password, t, scanFreq = account.split("\n")
        t = int(t)
        scanFreq = int(scanFreq)
        f.close()

    css1 = 'body > table > tbody > tr:nth-child(2) > td > table:nth-child(2) > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(11) > td > img:nth-child(1)'
    css2 = 'body > div:nth-child(1) > div:nth-child(4) > div > section > section > div > a'
    css3 = '#d-RADIO_799044 > div > label:nth-child(1) > input[type=radio]'
    css_save = '#d-RADIO_799044 > div > label:nth-child(1)'
    url = 'http://ids.hhu.edu.cn/amserver/UI/Login?goto=http://form.hhu.edu.cn/pdc/form/list'
    isDayReport = False
    while True:
        if time.localtime().tm_hour < t:
            isDayReport = False
        if time.localtime().tm_hour >= t and not isDayReport:
            browser = webdriver.Edge("msedgedriver.exe")
            browser.get(url)
            isLogin = False;
            while True:
                try:
                    # sleep(0.5)
                    if not isLogin:
                        browser.find_element_by_name('IDToken1').send_keys(number)  # 学号
                        browser.find_element_by_name('IDToken2').send_keys(password)
                        # sleep(2)  # 等待一秒
                        # a = browser.find_element(By.CSS_SELECTOR,css1)
                        # browser.execute_script("arguments[0].click();",a)
                        js1 = "defaultSubmit()"
                        browser.execute_script(js1)
                        # browser.find_element_by_css_selector(css1).click()  # 登陆
                        sleep(2)
                    isLogin = True
                    a = browser.find_element(By.CSS_SELECTOR, css2)
                    browser.get(a.get_property("href"))
                    # browser.execute_script("arguments[0].click();",a)
                    sleep(2)
                    a = browser.find_element(By.CSS_SELECTOR, css3)
                    browser.execute_script("arguments[0].click();", a)  # 选择体温正常
                    sleep(1)
                    browser.find_element_by_id('saveBtn').click()  # 提交
                    sleep(4)
                    text = browser.find_element_by_xpath('//*[@id="successSubmit"]/div[1]/h3').text
                    # print(text)
                except NoSuchElementException:
                    browser.get(url)
                    # print(1)
                    continue
                if text == '提交成功！':
                    browser.quit()
                    isDayReport = True
                    window = tkinter.Tk()
                    window.withdraw()  # 退出默认 tk 窗口

                    result = showinfo('提示', '打卡成功')
                    # print(f'提示: {result}')
                    break
        sleep(scanFreq)
        # print(1)
