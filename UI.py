import tkinter as tk
from Stock import Stock_Search as St

window = tk.Tk()
window.title("My Stock")#標題
window.geometry("300x150")#大小設定
window.resizable(False, False)

def On_button_click():
    def Load_num():
        try:
            Stock_unm = int(enter.get())
            Stock_date = int(enter2.get())
            Stock_time = int(enter3.get())
            return Stock_unm, Stock_date, Stock_time
        except:
            label = tk.Label(window, text="錯誤請輸入數字")
            label.grid(row=3,column=0,sticky="NW")
    Load_num()
    Stock_unm, Stock_date, Stock_time = Load_num()
    stock_search = St(Stock_unm, Stock_date, Stock_time)
    #print(Load_num())  測試用
    stock_search.Out_Stock()
def Wrong_num():
    label = tk.Label(window, text="輸入正確代碼")
    label.grid(row=3,column=0,sticky="NW")



button_text = tk.Label(window,text="代號")
button_text.grid(row=0,column=0,sticky="NW")

button_text2 = tk.Label(window,text="天數")
button_text2.grid(row=1,column=0,sticky="W")

button_text3 = tk.Label(window,text="分K")
button_text3.grid(row=2,column=0,sticky="W")

enter = tk.Entry(window, width=20)
enter.grid(row=0,column=1,sticky="NW")

enter2 = tk.Entry(window, width=20)
enter2.grid(row=1,column=1,sticky="W")

enter3 = tk.Entry(window, width=20)
enter3.grid(row=2,column=1,sticky="W")

button = tk.Button(window, text="確定", command=On_button_click)
button.place(x=100, y=100)

window.mainloop() #主程式循環