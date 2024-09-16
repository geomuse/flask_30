from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.utils
import json

app = Flask(__name__)

# 财务术语翻译字典
financial_terms = {
    'Total Revenue': '总收入',
    'Gross Profit': '毛利',
    'Operating Income': '营业收入',
    'Net Income': '净收入',
    'Total Assets': '总资产',
    'Total Liabilities': '总负债',
    'Total Equity': '总权益',
    'Cash': '现金',
    'Total Current Assets': '流动资产合计',
    'Total Current Liabilities': '流动负债合计',
    'Operating Cash Flow': '经营活动现金流',
    'Investing Cash Flow': '投资活动现金流',
    'Financing Cash Flow': '筹资活动现金流',
    'Tax Effect Of Unusual Items' : '不寻常物品的税收影响' ,
    'Tax Rate For Calcs' : '计算税率' ,
    'Normalized EBITDA' : '标准化 EBITDA' ,
    'Total Unusual Items' : '异常物品总数' ,
    'Total Unusual Items Excluding Goodwill' : '不包括商誉的异常项目总数' ,
    'Net Income From Continuing Operation Net Minority Interest' : '持续经营净利润 少数股东权益净额' ,
    'Reconciled Depreciation' : '调节折旧' ,
    'Reconciled Cost Of Revenue' : '经调节的收入成本/经调节的收入成本' ,
    'EBITDA' : '息税折旧摊销前利润' ,
    'EBIT' : '负债' ,
    'Net Interest Income' : '净利息收入',
    'Interest Expense' : '利息支出' ,
    'Interest Income' : '利息收入',
    'Normalized Income' : '标准化收入',
    'Net Income From Continuing And Discontinued Operation' : '持续经营和终止经营净利润',
    'Total Expenses' : '总费用',
    'Total Operating Income As Reported' : '报告的总营业收入',
    'Diluted Average Shares' : '稀释平均股数' ,
    # 添加更多术语翻译...
}

def translate_index(df):
    df.index = [f"{term} / {financial_terms.get(term, term)}" for term in df.index]
    return df

def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    
    # 获取过去3年的财务报表
    income_statement = translate_index(stock.financials).drop('2019-12-31',axis=1)
    balance_sheet = translate_index(stock.balance_sheet).drop('2019-12-31',axis=1)
    cash_flow = translate_index(stock.cashflow).drop('2019-12-31',axis=1)
    
    # 获取过去1年的股票价格
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*3)
    stock_price = stock.history(start=start_date, end=end_date)
    
    return income_statement, balance_sheet, cash_flow, stock_price

def create_stock_chart(stock_price):
    fig = go.Figure(data=[go.Candlestick(x=stock_price.index,
                open=stock_price['Open'],
                high=stock_price['High'],
                low=stock_price['Low'],
                close=stock_price['Close'])])
    fig.update_layout(title='Stock Price Over the Past Year / 过去三年的股票价格',
                      xaxis_title='Date / 日期',
                      yaxis_title='Price / 价格')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form['ticker']
        try:
            income_statement, balance_sheet, cash_flow, stock_price = get_financial_data(ticker)
            # 将DataFrame转换为HTML表格
            income_html = income_statement.to_html(classes='table table-striped')
            balance_html = balance_sheet.to_html(classes='table table-striped')
            cash_flow_html = cash_flow.to_html(classes='table table-striped')
            
            # 创建股票价格图表
            stock_chart = create_stock_chart(stock_price)
            
            return render_template('result.html', 
                                   ticker=ticker,
                                   income_statement=income_html,
                                   balance_sheet=balance_html,
                                   cash_flow=cash_flow_html,
                                   stock_chart=stock_chart)
        except Exception as e:
            error_message = f"Error fetching data / 获取数据时出错: {str(e)}"
            return render_template('index.html', error=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    
    app.run(debug=True)