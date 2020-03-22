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
    - [學習資源](https://www.youtube.com/watch?v=GGp-7VHgsKk)
    - 文件匯入指定格式：

        【 題號 / 題目類型 / 題目（數字）範圍 / 指定答案 】

        【 A2m / number / [1,12] , NaN】

    - 套件函數：
        - catch_no（主程式）
            - 説明：爬取csv檔内的題號欄位，在應用時可透過輸入題號來給出輸出。
            - 輸出：無，只是將csv檔内的内容存進字典裏。
        - fill
            - in
            - out
    - 思考
        - 如何分辨B3與B30？
        - 若匯入的csv之題號與問卷平臺題號match的情況下，如何偵測題目類型或題目範圍等等屬性是不符合的情況。
    - 允誠建議：

        ![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/68361a26-53dc-4365-a0cd-6619932d4efe/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/68361a26-53dc-4365-a0cd-6619932d4efe/Untitled.png)
