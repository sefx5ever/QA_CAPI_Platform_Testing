## 專案簡介
本專案利用中研院社會所CAPI問卷平臺進行壓力測試及基礎架構測試，使用Python語言及selenium套件模擬使用者行爲進行表單填寫測試，并在完成測試後輸出csv進行驗證。

目前專案所使用之文件如下：

- CAPI_test（邏輯文件csv檔）
- Web_Testing_日期（主程式碼py檔）
- Final_Result_日期_版本（最終選項輸出csv檔）
- autofill（套件py檔）
- Full_Run_Fill_Form（完整填答問卷mp4檔）
- [Github](https://github.com/sefx5ever/Web_Testing)

## 專案目標
以多綫程檢測試問卷網頁之架構、格式限制、頁面跳轉及最終輸出紀錄是否符合原有問卷設計架構以及方向。

## 測試順序
1. 測試題目及選項文字是否完全正確，並沒有遺漏
2. 不同答題類型的檢查項目
3. 跳題 （取消回答 / 强制停止 / 中途進入 ）
4. 問卷作答以及資料庫輸出内容是否一致
5. 完成訪問記錄的（訪員）問卷
6. 完成問卷后是否有出現（檢測）預過錄

## 作答方式
- **多選題**
- **單選題**
- **填空題**
- **下拉式題**
- **跳題 / 邏輯關係 / 取消回答 / 强制停止**
- **問題**

## 套件建立
- 隨機輸入（autofill）
    - [學習資源：創建套件](https://www.youtube.com/watch?v=GGp-7VHgsKk)
    - 文件匯入指定格式：

        【 quest_no/ quest_type / quest_condition / quest_force_ans 】

        【 A2m / number / [1,12] , NaN】

    - 文件題目類型規範：
        - 單選題（string）
            - 若在選擇後，出現填空的部分，則在 quest_type 輸入填空類型，quest_condition 中輸入對應輸入的值（若不輸入則輸出 type_blank 中的内容）。
            - 範例1：[text,faodbkfjsjknv,4]
            - 範例2：[,,2]
            - 範例3：[]
            - 範例中為輸入須符合 text 類別，所輸入值為 faodbkfjsjknv，在選擇時點擊第 4 項選項。
        - 多選題（list【string，number】）
            - 若需指定答案，則以 list 形式儲存。若在選擇後，出現填空的部分，則在 quest_type 輸入填空類型，quest_condition 中輸入對應輸入的值（若不輸入則輸出 type_blank 中的内容）。
            - 範例1：[,,[2,3,4]]
            - 範例2：[text,faodbkfjsjknv,[1,3,5]]
            - 若輸入值都爲空值，則用總選項除半（n），然後用 random 套件輸出（n）個答案。
        - 下拉式（string【list】）
            - 在 dropdown 題型中，以 list of list形式儲存，第一層 list 之第 0 項則是下拉式中選擇的項目，則第二層 list 可儲存string（填空狀態） 或則 int（下拉式選擇）。
            - 範例1：[,,[2,[1,3]]]
            - 範例2：[text,vdjfnvgjkdf,[1,['string']]]
            - 若在選擇後，出現填空的部分，則在 quest_type 輸入填空類型，quest_condition 中輸入對應輸入的值（若不輸入則輸出 type_blank 中的内容）。
        - 填空題（string，number）
            - 若有輸入值，則進行 return，不輸入則隨機輸出。若輸入類型為 number，則用 random 套件，把給定區間輸入 random.randint 中進行隨機生成。
            - 範例1：[text,,sdflsdf]
            - 範例2：[number,[1,4],]
    - 套件函數：
        - read_csv
            - 説明：在初始化時，讀取給定路徑並以 dataframe 形式開啓且儲存在變數 file_reader 中。
            - 輸出：dataframe
        - catch
            - 説明：將給定的小題文字在 dataframe 中搜尋，若有結果（以 len 為判斷標準），則進入 fill 函數。
            - 輸出：list / int / string
        - fill
            - 説明：進入此函數也代表著有指定條件需要進行操作。詳細内容，可參考【文件題目類型規範】。
            - 輸出：可參考【文件題目類型規範】
    - 思考
        - 如何分辨B3與B30？
        - 若匯入的csv之題號與問卷平臺題號match的情況下，如何偵測題目類型或題目範圍等等屬性是不符合的情況。
