import yfinance as y
import pandas as p
import plotly.graph_objects as g
import datetime
import pandas_market_calendars as Macl

class Stock_Search:
    def __init__(self, number: int, date: str, Candlestick: int):
        self.number = number  # 代號
        self.date = date  # 日
        self.Candlestick = Candlestick  # 分K

    def Out_Stock(self):
        twse = Macl.get_calendar("XTAI")
        today = datetime.datetime.now().date()
        start_date = (today - datetime.timedelta(days=self.date)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')

        # 將 start_date 和 end_date 字串轉換成 datetime.datetime 物件
        start_datetime = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_datetime = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        if self.Candlestick > 60:
            self.Candlestick = "1d"
        else:
            self.Candlestick = str(self.Candlestick) + "m"

        self.number = str(self.number) + ".tw"
        self.date = str(self.date) + "d"

        for date in twse.schedule(start_date=start_date, end_date=end_date).index:
            market_open_time = twse.schedule(start_date=date, end_date=date)['market_open'][0]
            market_close_time = twse.schedule(start_date=date, end_date=date)['market_close'][0]

            # 取得開市和收市時間
            start_time = datetime.datetime.combine(date, market_open_time.time())
            end_time = datetime.datetime.combine(date, market_close_time.time())

            # 判斷是否在限制的時間範圍內，如果是則下載資料
            if start_time >= start_datetime and end_time <= end_datetime:
                # 建立下載的時間範圍
                download_start = datetime.datetime.combine(date, datetime.time(hour=9, minute=0))
                download_end = datetime.datetime.combine(date, datetime.time(hour=13, minute=30))

                if download_start >= start_datetime and download_end <= end_datetime:
                    stock = y.download(self.number, start=download_start, end=download_end, interval=self.Candlestick)

                    # 上市改上櫃 錯誤則不執行
                    if stock.empty:
                        self.number = str(self.number).replace(".tw", ".two")  # 上櫃
                        print(self.number)
                        stock = y.download(self.number, period=self.date, interval=self.Candlestick)  # 再次運行
                        if stock.empty:
                            return False

                data = stock.reset_index()
                data.columns = ['現在時間', '開盤價', '最高價', '最低價', '收盤價', '調整後收盤價', '成交量']  # 改名
                data['現在時間'] = p.to_datetime(data['現在時間'], format='%Y-%m-%d %H:%M:%S')
                data['成交量'] //= 1000

                fig = g.Figure()

                # 成交量的圖
                fig.add_trace(
                    g.Bar(
                        name='成交量',
                        x=data['現在時間'],
                        y=data['成交量'],
                        yaxis='y2',
                        marker_color='#999900'
                    )

                )

                # k線圖
                fig.add_trace(
                    g.Candlestick(
                        name='',
                        x=data['現在時間'],
                        open=data['開盤價'],
                        high=data['最高價'],
                        low=data['最低價'],
                        close=data['收盤價'],
                        increasing_line_color='#fd5047',  # 上漲顏色(線)
                        increasing_fillcolor='#f29696',  # 上漲顏色
                        decreasing_line_color='#3d9970',  # 下跌顏色(線)
                        decreasing_fillcolor='#91c2b3'  # 下跌顏色
                    )
                )

                fig.update_layout(
                    title=str(self.number),
                    hovermode='x unified',  # 滑鼠停在圖上的時候會有資訊

                    yaxis=dict(
                        title='股價'
                    ),

                    yaxis2=dict(
                        overlaying='y',
                        side='right',
                        position=0.98,
                        title='成交量 (千股)',
                        tickfont=dict(color='#999900')
                    ),

                    font=dict(
                        size=20
                    )
                )

                fig.show()
