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
    
def emu_(emu,action):
    time.sleep(1)
    driver.find_element(By.XPATH,(f"//button[text()='{emu}']")).click()
    time.sleep(2)
    if (el:= get_element(driver,f"//button[text()='{action}']")) != False:
        el.click()
        print(f"'{emu}'stop_success")

driver = webdriver.Edge()
driver.minimize_window()
driver.get('http://192.168.21.190:23333')
time.sleep(1)
driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div/div/form/div[1]/div/input").send_keys('wind123www11')
driver.find_element(By.XPATH,"/html/body/div/div[2]/div/div/div/form/div[2]/button[1]").click()
with open('jobs/emu_list.txt', 'r', encoding='utf-8') as file:
    for line in file:
        emu_name = line.strip()  # 移除行末的换行符
        emu_(emu_name,"停止")
        time.sleep(1)
time.sleep(60)
with open('jobs/emu_list.txt', 'r', encoding='utf-8') as file:
    for line in file:
        emu_name = line.strip()  # 移除行末的换行符
        emu_id = emu_name[4:] 
        os.system(f"\"C:/Program Files/Netease/MuMuPlayer-12.0/shell/MuMuManager.exe\" api -v {emu_id} shutdown_player")
        time.sleep(2)
time.sleep(1)
print("stop finish")