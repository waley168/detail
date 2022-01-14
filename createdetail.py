from __future__ import print_function
import pickle
import os.path
from outputpdf import html2pdf
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import tkinter as tk  # 使用Tkinter前需要先匯入

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1p8Zpw7hLjbO3ECJqbYz3Zg2LN-CfMEHlqCxDxdFcylA'

# 第1步，例項化object，建立視窗window
window = tk.Tk()

# 第2步，給視窗的視覺化起名字
window.title('產生訂單明細')

# 第3步，設定視窗的大小(長 * 寬)
window.geometry('600x500')  # 這裡的乘是小x

# 第4步，在圖形介面上設定輸入框控制元件entry框並放置
e = tk.Entry(window, show=None, width=10, font=('Arial', 14))  # 顯示成明文形式
e.pack()


# 第5步，定義兩個觸發事件時的函式insert_point和insert_end（注意：因為Python的執行順序是從上往下，所以函式一定要放在按鈕的上面）

def appendtext(row):  # 將資料列為文件

    number = '** 輸入編號對應列表左邊的數字 **\n\n歡迎使用大玩家包車旅遊服務，您的訂單資訊如下：\n\n訂單編號:' + \
             row[0]

    return number


def insert_point():  # 在滑鼠焦點處插入輸入內容
    SAMPLE_RANGE_NAME = '2:2'
    var = e.get()
    if not var:
        print('列出第一筆')
    else:
        SAMPLE_RANGE_NAME = var + ':' + var

    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('./data/token/token.pickle'):
        with open('./data/token/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './data/token/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./data/token/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('找不到資料')
    else:
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)
        row[0] = row[0].replace('-', '').replace(':', '').replace(' ', '')
        if len(row[0]) < 14:
            row[0] = row[0][:8] + '0' + row[0][8:]
        totaltext = appendtext(row)
        t.insert('end', totaltext)
        html2pdf(row, optionmenu_event())
        print(totaltext)
def optionmenu_event(*args):
    from_text = var.get()
    mylabel['text'] = '來自 ' + from_text
    return from_text
optionList = ["夢玩家包車旅遊", "九賓商務租車", "天地玩家包車旅遊", "海山林玩家包車旅遊", "天地遊覽車"]
var = tk.StringVar()
var.set(optionList[0])
c1 = tk.OptionMenu(window, var, *optionList)
c1.pack()

mylabel = tk.Label(window, text='來自', height=2)
mylabel.pack()

#var.trace('w', lambda *args: print(var.get()))
var.trace("w", optionmenu_event)

# 第6步，建立並放置按鈕分別觸發兩種情況
b1 = tk.Button(window, text='產生明細', width=20,
               height=3, command=insert_point)
b1.pack()

# 第7步，建立並放置一個多行文字框text用以顯示，指定height=3為文字框是三個字元高度
t = tk.Text(window, height=30)
t.pack()

# 第8步，主視窗迴圈顯示
window.mainloop()
