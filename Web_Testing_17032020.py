import sys
import string
import random
import pandas as pd
from time import sleep
from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException , NoSuchElementException

# reload(sys)
# sys.setdefaultencoding("utf-8")

OWN_DATA,SYS_DATA = {} , {}
CONDITION = {}

def run_browser(browser):
    """
    主要針對給定搜尋引擎執行虛擬化，並登錄賬號
    """
    AS_WEBSITE_LINK = 'https://capi.geohealth.tw/'
    LOGIN_ID = 'scs10'
    LOGIN_PASS = 'ios0000'

    if browser == "ie":
        driver = webdriver.Ie()
    elif browser == "firefox":
        driver = webdriver.Firefox()
    elif browser == "chrome":
        driver = webdriver.Chrome()
    driver.get(AS_WEBSITE_LINK)

    try:
        input_id = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'username'))) # 登錄賬號
        input_pass = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'password'))) # 登錄密碼
        input_id.send_keys(LOGIN_ID)
        input_pass.send_keys(LOGIN_PASS+'\n')
        print('Login Successfully !')
        browser_project_opt(driver)
    except TimeoutException:
        return "NOTE[run_browser]: Loading took too much time !"

def import_condition():
    """
    針對不同問卷之標準進行條件匯入，需自訂輸入文件位置。
    """
    LOGIC_FILE_LOCATION = 'C:/Users/sefx5/Downloads/CAPI_test.csv'
    df = pd.read_csv( LOGIC_FILE_LOCATION ,encoding='utf-8',dtype = {'layer_2' : str})
    df['question_logic'] = df['question_logic'].fillna('')
    df['question'] = df['layer_1'].astype(str) + df['layer_2'] + df['layer_3'].fillna('')
    df.drop(df[df['question_logic'] == ''].index,axis = 0,inplace=True)

    for num,logic in zip(df['question'],df['question_logic']):
        CONDITION[num] = logic

def browser_project_opt(driver):
    """
    問卷測試可針對不同專案名字執行測試，只需修改 NO_PROJECT 為指定問卷位置順序。
    """
    NO_PROJECT = 1 # 問卷選擇（從1號開始）
    sleep(5)
    driver.implicitly_wait(3)
    try:
        driver.find_element_by_xpath('//*[@data-id="prj_select"]').click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#prj_select > option:nth-child({})'.format(str(NO_PROJECT+1))))).click() # 專案選擇
        driver.implicitly_wait(1)
        driver.find_element_by_id("prj_query").click()
        print('Select Project Successfully !')
        project_login(driver)
    except TimeoutException:
        return "NOTE[browser_project_opt]: Loading took too much time !"

def project_login(driver):
    """
    針對多綫程執行設定不同樣本編號，若修改問卷，也許提供該問卷樣本編號的第一順位號碼。
    """
    SAMPLE_NUMBER = 20200101+sample_add
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@name="{}"][1]'.format(str(SAMPLE_NUMBER))))).click() # 選擇樣本編號作答
        # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.NAME, str(SAMPLE_NUMBER)))).click() # 選擇樣本編號作答
        sleep(1)
        driver.find_element_by_class_name('btn.btn-blue').click()
        print("Project Login Successfully !")
        form_basic_info(driver)
    except NoSuchElementException:
        driver.find_element_by_xpath('//*[@id="case_in_prj_next"]/a').click() # 若不在此頁則Next再執行
        return project_login(driver)
    else:
        return "NOTE[project_login]: Loading took too much time !"


def form_basic_info(driver):
    """
    人資料部分可自定義，初始為隨機作答，該頁面與問卷填答分開執行。
    """
    ran_cat = random.randint(1,6) # 隨機人數
    ran_tel = random.randint(1,4) # 隨機應門者回答
    ran_str_len = 100
    ran_str_fbi = ''.join(random.choice(string.ascii_letters) for length in range(ran_str_len))
    try:
        driver.find_element_by_xpath("//div[@id='household']/label["+str(ran_cat)+"]").click() # 選擇人數
        driver.find_element_by_name("target_name").send_keys(ran_str_fbi) # 填寫中選擇姓名
        driver.find_element_by_xpath("//div[@id='sample_info']/div[7]/div[2]/label["+str(ran_tel)+"]").click() # 選擇應門者
        if ran_tel in [2,4]: # 填寫手機號，只能擇一填寫
            if ran_tel//2 == 0:
                driver.find_element_by_name("target_tel").send_keys('0')
                driver.find_element_by_name("target_ext").send_keys('0')
                driver.find_element_by_name("target_mobile").send_keys('0905916241')
            else:
                driver.find_element_by_name("target_tel").send_keys('0905916241')
                driver.find_element_by_name("target_ext").send_keys('0')
                driver.find_element_by_name("target_mobile").send_keys('0')
        driver.find_element_by_xpath('//*[@id="SurveyStart"]').click()
        # driver.implicitly_wait(2)
        # temp = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="jconfirm-box93213"]/div')))
        # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[2]/div/div/div/div/div/div/div/div[4]/button[1]'))).click()
        # print(temp)
        # 【缺少半途登錄】
        print('Form Filled Successfully !')
        print(CONDITION) # 顯示匯入的條件
        random_form(driver)
    except:
        return "NOTE[form_basic_info]: Value Error !"

def quest_multi_label(driver,class_name,cur_quest,num):
    print('quest_multi_label')
    ans_option = driver.find_elements_by_xpath('//*[@id="div_{}"]//div[@class="panel-body"][{}]//*[@class="{}"]'.format(str(cur_quest),str(num+1),class_name))
    num_selection = len(ans_option)
    option_selected = random.sample([num+1 for num in range(num_selection)],k = num_selection // 2)
    for tick in option_selected:
        if num_selection == tick:
            ans_option[tick-1].click()
            break
        ans_option[tick-1].click()
    check_extend = driver.find_elements_by_xpath('//*[@id="div_{}"]//input[@style="display: block;"]'.format(str(cur_quest)))
    if check_extend:
        for num in range(len(check_extend)):
            driver.find_element_by_xpath('//*[@id="div_{}"]//div[@class="panel-body"][{}]//input[@style="display: block;"]'.format(str(cur_quest),str(num+1))).send_keys(''.join(random.choice(string.ascii_letters) for length in range(10))) 

def quest_single_label(driver,class_name,cur_quest,num):
    print('quest_single_label')
    num_selection = len(driver.find_elements_by_xpath('//*[@id="div_{}"]/div[{}]//*[@class="{}"]'.format(str(cur_quest),str(num+2),class_name))) # 檢測小題選項數量
    driver.find_element_by_xpath('//*[@id="div_{}"]/div[{}]//label[@class="{}"]/input[@value="{}"]/parent::*'.format(str(cur_quest),str(num+2),class_name,str(random.randint(1,num_selection)))).click()
    check_extend = driver.find_elements_by_xpath('//*[@id="div_{}"]/div[{}]//*[@style="width: 50%; display: block; margin-top: 1em; margin-left: 0em;"]'.format(str(cur_quest),str(num+2))) # 檢查是否有任何輸入欄位彈出
    if check_extend:
        for num in range(len(check_extend)):
            driver.find_element_by_xpath('//*[@id="div_{}"]/div[{}]//*[@style="width: 50%; display: block; margin-top: 1em; margin-left: 0em;"]'.format(str(cur_quest),str(num+2))).send_keys(''.join(random.choice(string.ascii_letters) for length in range(10))) # 【輸入的字數及格式】【可能出現兩個以上的input】

def quest_input(driver,class_name,cur_quest,num):
    print('quest_input')
    ans_area = driver.find_elements_by_xpath('//*[@id="div_{}"]/div[{}]//*[@class="{}"]'.format(str(cur_quest),str(num+2),class_name)) 
    num_selection = len(ans_area) # 檢測小題選項數量
    for blank in range(num_selection):
        type_blank = ans_area[blank].get_attribute('type')
        # link = driver.find.find_element_by_xpath('//*[@id="div_{}"]//div[@class="panel-body"]//input[@class="{}"]'.format(cur_quest,class_name)) # 【缺少specific題序】【若有兩額填空或以上，還未找到其代碼】
        # type_blank = link.get_attribute('type')
        if type_blank != None:
            ans_area[blank].send_keys(judge_type(type_blank)) # 【待套件完成後輸入】

def quest_dropdown(driver,class_name,cur_quest,num):
    print('quest_dropdown')
    ans_option = driver.find_elements_by_xpath('//*[@id="div_{}"]//select[@class="selectpicker InOrOut"]/option'.format(str(cur_quest)))
    num_selection = len(ans_option)
    driver.find_element_by_xpath('//*[@id="div_{}"]//select[@class="selectpicker InOrOut"]/parent::div'.format(str(cur_quest))).click()
    driver.find_element_by_xpath('//*[@id="div_{}"]//select[@class="selectpicker InOrOut"]/option[{}]'.format(str(cur_quest),random.randint(2,num_selection))).click()
    condition_extend = ["height: 2.5em; width: 30em;","padding-left: 0px;"]
    for condition in condition_extend:
        check_extend = driver.find_elements_by_xpath('//*[@id="div_{}"]//*[@style="{}"]'.format(str(cur_quest),str(condition)))
        if check_extend:
            if check_extend[0].get_attribute('style') == condition_extend[0]:
                type_blank = check_extend[0].get_attribute('type')
                check_extend[0].send_keys(judge_type(type_blank))
            if check_extend[0].get_attribute('style') == condition_extend[1]:
                quest_to_opt = driver.find_elements_by_xpath('//*[@id="div_{}"]//*[@class="col-sm-12 stv"]//select'.format(str(cur_quest)))
                for quest_num in range(len(quest_to_opt)):
                    driver.find_element_by_xpath('//*[@id="div_{}"]//*[@class="col-sm-12 stv"]/div[{}]'.format(str(cur_quest),str(quest_num+1))).click()
                    num_option = len(driver.find_elements_by_xpath('//*[@id="div_{}"]//*[@class="col-sm-12 stv"]/div[{}]//option'.format(str(cur_quest),str(quest_num+1))))
                    driver.find_element_by_xpath('//*[@id="div_{}"]//*[@class="col-sm-12 stv"]/div[{}]//option[{}]'.format(str(cur_quest),str(quest_num+1),str(random.randint(2,num_option)))).click()

def quest_multi_single_label(driver,class_name,cur_quest,num):
    print('quest_nulti_single_label')
    ans_option = driver.find_elements_by_xpath()
    num_selection = len(ans_option)
    for num in range(num_selection):
        ans_option[num].find_elements_by_xpath().click()

def judge_type(_type):
    if _type == 'text' or _type == 'password':
        return _type # return 套件text
    elif _type == 'number':
        return 12 # return 套件number
    elif _type == 'checkbox':
        return _type # return 套件multi label
    elif _type == 'date':
        return _type # return 套件時間
    elif _type == 'email':
        return _type # return 套件email使用
    elif _type == 'radio':
        return _type # return 單選題類型
    elif _type == 'telephone':
        return _type # return 手機格式 get pattern
    else:
        return "NOTE[judge_type]:"+_type+' is developing !'
    
##########
### TO-DEVELOP-TYPE
# datetime-local 選擇日期及時間
# color 選擇顔色
# submit 上傳文件檔案
# hidden 待輸入上傳後輸出
# image 標簽以image的形式呈現
# month 輸入年月
# range 範圍區間選擇
# reset 重置設定
# search 搜尋功能
# time 選擇時間
# url 鏈接輸入
# week 選擇年份及周數
##########

def random_form(driver):
    """
    主要測試函數，透過迴圈把不同題目類型的題目進行填答。
    """
    driver.implicitly_wait(2)
    TOTAL_ANS = len(driver.find_elements_by_class_name('panel.panel-primary.page')) # 問卷總題數
    # QUESTION_BEGIN = 1 # 初始題號
    CUR_QUEST = 1 # 目前所在題號

    while(int(CUR_QUEST) < TOTAL_ANS):
        # CUR_QUEST = int(driver.find_element_by_xpath('//*[@id="div_{}"]/div[1]'.format(QUESTION_BEGIN)).text.split('大題')[0][1:]) # 截取目前題號
        if CUR_QUEST != 1:
            CUR_QUEST = driver.find_element_by_css_selector('.panel.panel-primary.page[style="display: block;"]').get_property('id').split('_')[1] #  > div.panel-body > div.btn-group.col-sm-12
            print(CUR_QUEST)
        page_quest_to_ans = len(driver.find_elements_by_css_selector('#div_{} > .panel-body'.format(str(CUR_QUEST)))) # 該頁需回答的題目數量
        print(page_quest_to_ans)
        for num in range(page_quest_to_ans): # 利用迴圈，依據標簽之class屬性辨識題目類型，並進行回答
            target_quest = driver.find_element_by_css_selector('#div_{} > .panel-body:nth-child({})'.format(str(CUR_QUEST),str(num+2))) # 標記目前需回答的小題，從第1個panel-body開始
            type_option_by_class = [class_list.get_attribute('class') for class_list in target_quest.find_elements_by_xpath('//*[@id="div_{}"]//*[@class="panel-body"][{}]//*[@class]'.format(str(CUR_QUEST),str(num+1)))] # 檢測panel-body底下所有class的名稱 # 【需再優化所爬取的class内容】
            type_compare_by_class = ['checkbox_lbl col-sm-12','btn btn-default radio_lbl','form-control ValidateNumber','form-control','dropdown bootstrap-select InOrOut','selectpicker InOrOut'] # 所有題目類型的可能class名稱
            type_result = [option for option in type_option_by_class if option in type_compare_by_class] # 交叉比對題目類型，取得共同點，即爲題目類型之class
            if type_result[0] in ['checkbox_lbl col-sm-12']: # quest_multi_label
                quest_multi_label(driver,type_result[0],CUR_QUEST,num)
            elif type_result[0] in ['btn btn-default radio_lbl']: # quest_single_label
                quest_single_label(driver,type_result[0],CUR_QUEST,num)
            elif type_result[0] in ['form-control ValidateNumber','form-control']: # quest_input
                quest_input(driver,type_result[0],CUR_QUEST,num)
            elif type_result[0] in ['dropdown bootstrap-select InOrOut','selectpicker InOrOut']: # quest_dropdown
                quest_dropdown(driver,type_result[0],CUR_QUEST,num)
            # else:
            #     print("NOE[random_form]:"+str(CUR_QUEST)+":"+type_result[0])
        driver.find_element_by_css_selector('#btn_next_{}'.format(str(CUR_QUEST))).click() # 點擊下一題
        if CUR_QUEST == 1:
            CUR_QUEST+=1
        check_caution = driver.find_elements_by_xpath('//*[@class="jconfirm-buttons"]')
        if check_caution:
            driver.find_element_by_xpath('//div[@class="jconfirm-buttons"]/button').click()
            sleep(1)
            continue
    if CUR_QUEST == TOTAL_ANS: # 確認完成訪問后，點擊上傳
        driver.find_element_by_id('btn_finish').click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div[2]/div/div/div/div/div/div/div/div[4]/button[1]'))).click() # 確認上傳
        # /html/body/div[6]/div[2]/div/div/div/div/div/div/div/div[4]/button[2] 取消路

if __name__ == '__main__' :
    for sample_add in range(1):
        run_browser('chrome')