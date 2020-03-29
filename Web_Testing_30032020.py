import string
import random
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException , NoSuchElementException

# 建立空的Dataframe
column_names = ["quest_no","quest_title","quest_ans","quest_others"] # 欄位名稱
OWN_DATA = pd.DataFrame(columns = column_names) # 建立 dataframe
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
        input_id = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'username'))) # 定位賬號
        input_pass = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'password'))) # 定位密碼
        input_id.send_keys(LOGIN_ID) # 輸入賬號
        input_pass.send_keys(LOGIN_PASS+'\n') # 輸入密碼
        print('STEP 1[run_browser]: Login Successfully !')
        browser_project_opt(driver)
    except:
        return "STEP 1[run_browser]: Loading took too much time !"

def browser_project_opt(driver):
    """
    問卷測試可針對不同專案名字執行測試，只需修改 NO_PROJECT 為指定問卷位置順序。
    """
    NO_PROJECT = 1 # 問卷選擇（從1號開始）
    sleep(5)
    try:
        driver.find_element_by_xpath('//*[@data-id="prj_select"]').click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select#prj_select > option:nth-child({})' \
            .format(str(NO_PROJECT+1))))).click() # 專案選擇
        driver.implicitly_wait(1)
        driver.find_element_by_id("prj_query").click() # 點擊確認專案
        print('STEP 2[browser_project_opt]: Select Project Successfully !')
        project_login(driver)
    except:
        return "STEP 2[browser_project_opt]: Loading took too much time !"

def project_login(driver):
    """
    針對多綫程執行設定不同樣本編號，若修改問卷，也許提供該問卷樣本編號的第一順位號碼。
    """
    SAMPLE_NUMBER = 20200101+sample_add
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@name="{}"][1]'
        .format(str(SAMPLE_NUMBER))))).click() # 選擇樣本編號作答
        sleep(1)
        driver.find_element_by_class_name('btn.btn-blue').click() # 點擊開始訪問
        print("STEP 3[project_login]: Project Login Successfully !")
        form_basic_info(driver)
    except NoSuchElementException:
        driver.find_element_by_xpath('//*[@id="case_in_prj_next"]/a').click() # 若搜尋不到樣本編號則尋找下一頁按鈕
        return project_login(driver)
    else:
        return "STEP 3[project_login]: Loading took too much time !"


def form_basic_info(driver):
    """
    人資料部分可自定義，初始為隨機作答，該頁面與問卷填答分開執行。
    """
    ran_cat = random.randint(1,6) # 隨機人數
    ran_tel = random.randint(1,4) # 隨機應門者回答
    ran_str_len = 10 # 輸出string的長度
    ran_str_fbi = ''.join(random.choice(string.ascii_letters) for length in range(ran_str_len)) # 按照條件生成一組 string
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
        driver.find_element_by_xpath('//*[@id="SurveyStart"]').click() # 點擊開始問卷
        print('STEP 4[form_basic_info]: Form Filled Successfully !')
        random_form(driver)
    except:
        return "STEP 4[form_basic_info]: Value Error !"

# TODO
# 1.中途登入功能 
# 2.所有隨機輸入待完成套件后修改

def quest_multi_label(driver,class_name,cur_quest,num): # 多選題函數
    print('Answering【'+str(cur_quest)+'】: Multi Label Question...')
    ans_option = driver.find_elements_by_xpath('//*[@id="div_{}"]//div[@class="panel-body"][{}]//*[@class="{}"]'
        .format(str(cur_quest),str(num+1),class_name)) # 定位作答區域
    num_selection = len(ans_option) # 獲取答題的選項總數
    option_selected = random.sample([num+1 for num in range(num_selection)],k = num_selection // 2) # 隨機生成需選擇的選項
    for tick in option_selected: # 用迴圈進行回答動作
        if num_selection == tick: # 若點擊最後一項，則停止選擇，因爲將取消之前的選擇，留下最後的選項
            ans_option[tick-1].click()
            break
        ans_option[tick-1].click()
    check_extend = driver.find_elements_by_xpath('//*[@id="div_{}"]//input[@style="display: block;"]'.format(str(cur_quest)))
    if check_extend: # 檢查是否有任何輸入欄位彈出
        for blank in check_extend:
            type_blank = blank.get_attribute('type') # 抓取填空的類型
            blank.send_keys(judge_type(type_blank)) # 進行回答

def quest_single_label(driver,class_name,cur_quest,num): # 單選題函數
    print('Answering【'+str(cur_quest)+'】: Single Label Question...')
    num_selection = len(driver.find_elements_by_xpath('//*[@id="div_{}"]/div[{}]//*[@class="{}"]'
        .format(str(cur_quest),str(num+2),class_name))) # 獲取答題的選項總數
    if num_selection > 30: # 由於問卷規律問題， 因此暫時設定此限制
        num_selection = 27
    driver.find_element_by_xpath('//*[@id="div_{}"]/div[{}]//label[@class="{}"]/input[@value="{}"]/parent::*'
        .format(str(cur_quest),str(num+2),class_name,str(random.randint(1,num_selection-1)))).click() # 進行回答
    check_extend = driver.find_elements_by_xpath('//*[@id="div_{}"]/div[{}]//input[@style="width: 50%; display: block; margin-top: 1em; margin-left: 0em;"]'
        .format(str(cur_quest),str(num+2)))
    if check_extend: # 檢查是否有任何輸入欄位彈出
        for blank in check_extend:
            type_blank = blank.get_attribute('type') # 抓取填空的類型
            blank.send_keys(judge_type(type_blank)) # 進行回答

def quest_input(driver,class_name,cur_quest,num): # 填答題函數
    print('Answering【'+str(cur_quest)+'】: Input Question...')
    ans_area = driver.find_elements_by_xpath('//*[@id="div_{}"]/div[{}]//*[@class="{}"]'
        .format(str(cur_quest),str(num+2),class_name)) # 定位作答區域
    num_selection = len(ans_area) # 獲取答題的選項總數
    for blank in range(num_selection):
        type_blank = ans_area[blank].get_attribute('type') # 抓取填空的類型
        if type_blank != None:
            ans_area[blank].send_keys(judge_type(type_blank)) # 進行回答

def quest_dropdown(driver,class_name,cur_quest,num): # 下拉式題函數
    print('Answering【'+str(cur_quest)+'】: Dropdown Question...')
    ans_option = driver.find_elements_by_xpath('//*[@id="div_{}"]//select[@class="selectpicker InOrOut"]/option'
        .format(str(cur_quest))) # 定位作答區域
    num_selection = len(ans_option) # 獲取答題的選項總數
    driver.find_element_by_xpath('//*[@id="div_{}"]//select[@class="selectpicker InOrOut"]/parent::div'
        .format(str(cur_quest))).click() # 點擊讓 option 選項渲染
    driver.find_element_by_xpath('//*[@id="div_{}"]//select[@class="selectpicker InOrOut"]/option[{}]'
        .format(str(cur_quest),random.randint(2,num_selection))).click() # 進行回答
    condition_extend = ["height: 2.5em; width: 30em;","padding-left: 0px;"] # 條件列表，判斷衍生題目
    for condition in condition_extend:
        check_extend = driver.find_elements_by_xpath('//*[@id="div_{}"]//*[@style="{}"]'.format(str(cur_quest),str(condition)))
        if check_extend: # 判斷衍生層是否存在
            if check_extend[0].get_attribute('style') == condition_extend[0]: # 填空題
                type_blank = check_extend[0].get_attribute('type') # 抓取填空的類型
                check_extend[0].send_keys(judge_type(type_blank)) # 進行回答
            if check_extend[0].get_attribute('style') == condition_extend[1]: # 下拉式題
                quest_to_opt = driver.find_elements_by_xpath('//*[@id="div_{}"]//*[@class="col-sm-12 stv"]//select'
                    .format(str(cur_quest))) # 定位回答區域
                for quest_num in range(len(quest_to_opt)): # 用迴圈進行回答
                    driver.find_element_by_xpath('//*[@id="div_{}"]//*[@class="col-sm-12 stv"]/div[{}]'
                        .format(str(cur_quest),str(quest_num+1))).click() # 點擊讓 option 選項渲染
                    num_option = len(driver.find_elements_by_xpath('//*[@id="div_{}"]//*[@class="col-sm-12 stv"]/div[{}]//option'
                        .format(str(cur_quest),str(quest_num+1)))) # 獲取答題的選項總數
                    driver.find_element_by_xpath('//*[@id="div_{}"]//*[@class="col-sm-12 stv"]/div[{}]//option[{}]'
                        .format(str(cur_quest),str(quest_num+1),str(random.randint(2,num_option)))).click() # 進行回答

def quest_multi_single_label(driver,class_name,cur_quest,num): # 多選中的單選題函數
    print('Answering【'+str(cur_quest)+'】: Multi of Single Label Question...')
    ans_option = driver.find_elements_by_xpath('//div[@id="div_{}"]/div[@class="panel-body"][{}]/div/div[contains(@style,"display: inline")]'
        .format(str(cur_quest),str(num+1))) # 定位作答區域
    num_selection = len(driver.find_elements_by_xpath('//div[@id="div_{}"]/div[@class="panel-body"][{}]/div/div[contains(@style,"display: inline")][1]//label'
        .format(str(cur_quest),str(num+1)))) # 獲取需回答的區域數量
    # 用 class name 判斷題目類型
    if class_name == 'col-sm-3 btn-group dynamic_display': # 單選題
        for opt_num in range(len(ans_option)):
            driver.find_element_by_xpath('//div[@id="div_{}"]/div[@class="panel-body"][{}]/div/div[contains(@style,"display: inline")][{}]//input[@value="{}"]/parent::label'
                .format(str(cur_quest),str(num+1),str(opt_num+1),str(random.randint(1,num_selection)))).click()
    if class_name == 'form-control ValidateNumber dynamic_display': # 填空題
        for opt_num in range(len(ans_option)):
            type_blank = driver.find_element_by_xpath('//div[@id="div_{}"]/div[@class="panel-body"][{}]/div/div[contains(@style,"display: inline")][{}]/input'
                .format(str(cur_quest),str(num+1),str(opt_num+1))).get_attribute('type') # 抓取填空的類型
            driver.find_element_by_xpath('//div[@id="div_{}"]/div[@class="panel-body"][{}]/div/div[contains(@style,"display: inline")][{}]/input'
                .format(str(cur_quest),str(num+1),str(opt_num+1))).send_keys(judge_type(type_blank)) # 進行回答
    check_extend = driver.find_elements_by_xpath('//div[@id="div_{}"]/div[@class="panel-body"][{}]//input[@style="width: 100%; display: block;"]'
        .format(str(cur_quest),str(num+1)))
    if check_extend: # 判斷衍生層是否存在
        for blank in check_extend:
            type_blank = blank.get_attribute('type') # 抓取填空的類型
            blank.send_keys(judge_type(type_blank)) # 進行回答

def random_form(driver): # 回答主程式
    """
    主要測試函數，透過迴圈把不同題目類型的題目進行填答。
    """
    driver.implicitly_wait(2)
    TOTAL_ANS = len(driver.find_elements_by_class_name('panel.panel-primary.page')) # 問卷總題數
    CUR_QUEST = 1 # 起始題號

    while(int(CUR_QUEST) < TOTAL_ANS):
        if CUR_QUEST != 1: # 由於第一講不顯示 display:block，故設定此條件
            CUR_QUEST = driver.find_element_by_css_selector('.panel.panel-primary.page[style="display: block;"]') \
            .get_property('id').split('_')[1] # 抓取當前題號
        page_quest_to_ans = len(driver.find_elements_by_css_selector('#div_{} > .panel-body'
            .format(str(CUR_QUEST)))) # 該頁需回答的題目數量
        print('Question ['+str(CUR_QUEST)+'] : Number question to answer ' + str(page_quest_to_ans))
        for num in range(page_quest_to_ans): # 利用迴圈，依據標簽之class屬性辨識題目類型，並進行回答
            target_quest = driver.find_element_by_css_selector('#div_{} > .panel-body:nth-child({})'
                .format(str(CUR_QUEST),str(num+2))) # 標記目前需回答的小題，從第1個panel-body開始
            type_option_by_class = [class_list.get_attribute('class') for class_list in target_quest
                .find_elements_by_xpath('//*[@id="div_{}"]//*[@class="panel-body"][{}]//*[@class]'
                .format(str(CUR_QUEST),str(num+1)))] # 檢測panel-body底下所有class的名稱 # 【需再優化所爬取的class内容】
            type_compare_by_class = ['checkbox_lbl col-sm-12','btn btn-default radio_lbl','form-control ValidateNumber',
                'form-control','dropdown bootstrap-select InOrOut','selectpicker InOrOut',"col-sm-3 btn-group dynamic_display",
                "form-control ValidateNumber dynamic_display"] # 所有題目類型的可能class名稱
            type_result = [option for option in type_option_by_class if option in type_compare_by_class] # 交叉比對題目類型，取得共同點，即爲題目類型之class
            if type_result[0] in ['checkbox_lbl col-sm-12']: # 多選題特徵
                quest_multi_label(driver,type_result[0],CUR_QUEST,num)
            elif type_result[0] in ['btn btn-default radio_lbl']: # 單選題
                quest_single_label(driver,type_result[0],CUR_QUEST,num)
            elif type_result[0] in ['form-control ValidateNumber','form-control']: # 填空題
                quest_input(driver,type_result[0],CUR_QUEST,num)
            elif type_result[0] in ['dropdown bootstrap-select InOrOut','selectpicker InOrOut']: # 下拉式題
                quest_dropdown(driver,type_result[0],CUR_QUEST,num)
            elif type_result[0] in ["col-sm-3 btn-group dynamic_display","form-control ValidateNumber dynamic_display"]: # 多選中的單選題
                quest_multi_single_label(driver,type_result[0],CUR_QUEST,num)
            else:
                return "STEP 5[random_form]: Can't find the class name of " + str(type_result[0]) + "in Question " + str(CUR_QUEST) + "!" 
        driver.find_element_by_css_selector('#btn_next_{}'.format(str(CUR_QUEST))).click() # 點擊下一題
        check_caution = driver.find_elements_by_xpath('//*[@class="jconfirm-buttons"]')
        if check_caution: # 檢查是否有任何警示訊息，若有重新回答該題
            driver.find_element_by_xpath('//div[@class="jconfirm-buttons"]/button').click()
            sleep(1)
        if CUR_QUEST == 1: # 同上 display:block 而增設設定
            CUR_QUEST+=1
    if int(CUR_QUEST) == TOTAL_ANS: # 確認完成訪問后，點擊上傳
        driver.find_element_by_id('btn_finish').click() # 點擊完成回答
        sleep(1)
        driver.find_element_by_class_name('btn btn-blue confirm testtest').click() # 確認上傳
        # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn btn-blue confirm testtest'))).click() # 確認上傳

# --------------------功能函數-------------------------- #
def import_condition():
    """
    針對不同問卷之標準進行條件匯入，需自訂輸入文件位置。
    """
    LOGIC_FILE_LOCATION = 'C:/Users/sefx5/Downloads/CAPI_test.csv' # 自訂文件位置
    df = pd.read_csv(LOGIC_FILE_LOCATION ,encoding='utf-8',dtype = {'layer_2' : str}) # 匯入條件 csv 檔案
    df['question_logic'] = df['question_logic'].fillna('') # 將空的欄位值輸入空元素
    df['question'] = df['layer_1'].astype(str) + df['layer_2'] + df['layer_3'].fillna('') # 將欄位中的條件内容合并
    df.drop(df[df['question_logic'] == ''].index,axis = 0,inplace=True) # 空的邏輯欄位去除，留下需進行判斷的小題

    # 將小題内容與條件以 dict 形式存取
    for num,logic in zip(df['question'],df['question_logic']): 
        CONDITION[num] = logic

def data_append(quest_no,quest_title,quest_ans,quest_others):
    # 將每題回答内容輸入至 dataframe
    OWN_DATA.append({
    "quest_no" : quest_no,
    "quest_title" :quest_title,
    "quest_ans" : quest_ans,
    "quest_others" : quest_others
    })
    
    print(OWN_DATA)
    print(CONDITION)

def judge_type(_type):
    if _type == 'text' or _type == 'password':
        return _type # return 套件text
    elif _type == 'number':
        return 4 # return 套件number
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

# TODO
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
# --------------------功能函數-------------------------- #

# -----------------啓動自動化測試------------------------ #
if __name__ == '__main__' :
    for sample_add in range(1):
        run_browser('chrome')