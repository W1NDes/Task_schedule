import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import exceptions

def get_element(browser, xpaths):
    """
    判断是否存在元素并获取元素对象
    :param browser: 浏览器对象
    :param xpaths: xpaths表达式
    :return: 元素对象或为空
    """
    try:
        target = browser.find_element(By.XPATH, xpaths)
    except exceptions.NoSuchElementException:
        return False
    else:
        return target
    
def emu_(emu,action,action2):
    time.sleep(2)
    driver.find_element(By.XPATH,(f"//button[text()='{emu}']")).click()
    time.sleep(3)
    if (el:= get_element(driver,f"//button[text()='{action}']")) != False:
        el.click()
    time.sleep(3)
    if get_element(driver,f"//button[text()='{action2}']"):
        print(f"'{emu}'start_success")
        return True
    else:
        return False
    

driver = webdriver.Edge()
driver.minimize_window()
driver.get('http://192.168.21.190:23333')
time.sleep(2)
driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div/div/form/div[1]/div/input").send_keys('wind123www11')
time.sleep(2)
driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div/div/form/div[2]/button[1]").click()
with open('jobs/alas_only_start.txt', 'r', encoding='utf-8') as file:
    for line in file:
        emu_name = line.strip()  # 移除行末的换行符
        count = 0
        while(count <= 5):
            count+=1
            print(count)
            if emu_(emu_name,"启动","停止") == True:
                print("check_ok")
                break
        time.sleep(1)

time.sleep(1)
print("start finish")