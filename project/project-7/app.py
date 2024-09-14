from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.utils
import json

app = Flask(__name__)

def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    
    # 获取过去3年的财务报表
    income_statement = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
    
    # 获取过去1年的股票价格
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    stock_price = stock.history(start=start_date, end=end_date)
    
    return income_statement, balance_sheet, cash_flow, stock_price

def create_stock_chart(stock_price):
    fig = go.Figure(data=[go.Candlestick(x=stock_price.index,
                open=stock_price['Open'],
                high=stock_price['High'],
                low=stock_price['Low'],
                close=stock_price['Close'])])
    fig.update_layout(title='过去一年的股票价格', xaxis_title='日期', yaxis_title='价格')
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
            error_message = f"获取数据时出错: {str(e)}"
            return render_template('index.html', error=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    
    app.run(debug=True)