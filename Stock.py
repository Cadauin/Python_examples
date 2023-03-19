import yfinance as y
import pandas as p
import plotly.graph_objects as g



class Stock_Search:
    def __init__(self, number: int, date: str, Candlestick: int):
        self.number = number  # 代號
        self.date = date  # 日
        self.Candlestick = Candlestick  # 分K

    def Out_Stock(self):

        if self.Candlestick > 60:
            self.Candlestick = "1d"#天
        else:
            self.Candlestick = str(self.Candlestick) + "m"#分鐘

        self.number=str(self.number)+".tw"#臺股
        self.date=str(self.date)+"d"#回推日期

        stock = y.download(self.number, period=self.date, interval=self.Candlestick)
        #錯誤股票代碼
        if stock.empty:
            return


        data = stock.reset_index()
        data.columns = ['現在時間', '開盤價', '最高價', '最低價', '收盤價', '調整後收盤價', '成交量']  # 改名
        data['現在時間'] = p.to_datetime(data['現在時間'], format='%Y-%m-%d %H:%M:%S')
        data['成交量'] //= 1000

        result = g.Figure()

        # 成交量的圖
        result.add_trace(
            g.Bar(
                name='成交量',
                x=data['現在時間'],
                y=data['成交量'],
                yaxis='y2',
                marker_color='#999900'
            )
        )

        # k線圖
        result.add_trace(
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

        result.update_layout(
            title=str(self.number),
            hovermode='x unified',  # 滑鼠停在圖上的時候會有資訊

            yaxis=dict(
                title='股價'
            ),

            yaxis2=dict(
                overlaying='y',
                visible=False
            ),

            font=dict(
                size=20
            )
        )

        result.show()