from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException,NoSuchFrameException,ElementClickInterceptedException
import time

'不同的网页流程各不相同，还是以def完成全部流程，class意义不大'
'do not use IE for its slowness which only waste your time and lifespan'
# edge 
#browser = webdriver.Edge()
'edge has updated to chrome-based edge, edge driver needs update'

gmail = 'chidunxu@gmail.com'
phone = '15901857132'
common_password = 'XuMinJie19961127'

load = {
    'huaweicloud':{
        'url':'https://www.huaweicloud.com/HDC.Cloud.html',
        'user_name':phone,
        'password':common_password
    },
    'bianhuaho':{
        'url':'https://bianhuaho.com/auth/login',
        'user_name':gmail,
        'password':common_password
    },
}

def huaweicloud():
    task = 'huaweicloud'
    print(f'\n--------------------------------{task.upper()}--------------------------------\n')

    # chrome
    options = webdriver.ChromeOptions()
    for arg in ['lang=zh_CN.UTF-8','headless']:
        options.add_argument(arg)
    browser = webdriver.Chrome(chrome_options = options)
    wait = WebDriverWait(browser,30)

    browser.get(load[task]['url'])
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'hdc-count')))
    print(browser.title)
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'hdc-count'))).click()

    browser.switch_to.window(browser.window_handles[-1])
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'tiny-input-text')))
    print(browser.title)
    browser.find_elements_by_class_name('tiny-input-text')[0].send_keys(Keys.CONTROL,'a')
    browser.find_elements_by_class_name('tiny-input-text')[0].send_keys(load[task]['user_name'])
    browser.find_elements_by_class_name('tiny-input-text')[1].send_keys(load[task]['password'])
    wait.until(EC.element_to_be_clickable((By.ID,'btn_submit'))).click()
    

    browser.switch_to.window(browser.window_handles[-1])
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'button-content'))) # wait还是很有必要的
    print(browser.title)
    if browser.find_elements_by_class_name('button-content')[0].text == '已签到':
        print('signed\n')
    else:
        wait.until(EC.presence_of_element_located((By.ID,'homeheader-signin')))   
        wait.until(EC.element_to_be_clickable((By.ID,'homeheader-signin'))).click() #need change
        print(f'{task} daily bouns achieved!\n')
    browser.refresh()
    wait.until(EC.presence_of_element_located((By.ID,'homeheader-coins')))
    t = f'%Y-%m-%d %H:%M:%S'
    coins = browser.find_element_by_id('homeheader-coins').text
    print(f'{time.strftime(t,time.localtime(time.time()))} | My coins {coins}\n')

    browser.quit()

def bianhuaho():
    task = 'bianhuaho'
    print(f'\n--------------------------------{task.upper()}--------------------------------\n')

    ### problem here:
    ###        if no proxy, it needs too much time, casuing timeout error
    ###        the v2ray be using, how to setting proxy
    # chrome
    browser = common_chrome()
    wait = WebDriverWait(browser,30)

    browser.get(load[task]['url'])
    time.sleep(5)
    browser.refresh()
    wait.until(EC.presence_of_element_located((By.ID,'email')))
    print(browser.title)
    browser.find_element_by_id('email').send_keys(Keys.CONTROL,'a')
    browser.find_element_by_id('email').send_keys(load[task]['user_name'])
    browser.find_element_by_id('password').send_keys(load[task]['password'])
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'btn btn-primary btn-lg btn-block login'))).click()

    browser.switch_to.window(browser.window_handles[-1])
    wait.until(EC.presence_of_element_located((By.ID,'checkin-div')))
    browser.find_element_by_id('checkin-div').click()

def common_chrome():
    options = webdriver.ChromeOptions()
    for arg in ['lang=zh_CN.UTF-8','head-less']:
        options.add_argument(arg)
    browser = webdriver.Chrome(options = options)
    return browser

def log(content):
    with open('log.txt','a') as a:
        a.write(f'[{time.asctime(time.localtime(time.time()))}] {content} ')
    a.close() 

if __name__ == "__main__":
    huaweicloud()
    #bianhuaho()