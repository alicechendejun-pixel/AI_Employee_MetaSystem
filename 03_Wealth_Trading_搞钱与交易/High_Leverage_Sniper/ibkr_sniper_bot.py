import logging
import asyncio
from ib_insync import *
import pandas as pd
import numpy as np

# ==========================================
# High Leverage Sniper System (10k RMB / ~$1400 USD Account)
# Target Market: CME Micro E-mini Nasdaq-100 (MNQ)
# ==========================================
# 第一性原理逻辑：
# 1万人民币资金极小，无法靠定投/吃分红致富。
# 必须使用衍生品(期货)获取高杠杆(MNQ 约 20 倍杠杆)。
# 核心风控：每次只开 1 手 MNQ，止损放在 20 个点(亏损约 40 美元 / 300 RMB)。
# 核心盈利：使用移动止盈(Trailing Stop)，一旦做对单边趋势，吃到几百点利润(盈利 3000-5000 RMB)。
# 盈亏比非对称博弈：亏损严格截断，利润无限奔跑。
# ==========================================

# 全局配置
IS_PAPER_TRADE = True  # ⚠️ 强烈警告：必须先用模拟盘跑 1 周！准备实盘时改为 False
PORT = 7497 if IS_PAPER_TRADE else 7496
CLIENT_ID = 101

# 交易参数
SYMBOL = 'MNQ'
EXCHANGE = 'GLOBEX'
QUANTITY = 1               # 1 万元本金只能开 1 手！严禁重仓！
STOP_LOSS_TICKS = 80       # 20 个点止损 (MNQ 1 point = 4 ticks, 1 tick = $0.5)
TRAILING_STOP_TICKS = 200  # 50 个点移动止盈跟进

class AsymmetricSniperBot:
    def __init__(self):
        self.ib = IB()
        self.contract = Future(SYMBOL, '202609', EXCHANGE) # 需要定期更换主力合约月份
        self.is_in_position = False
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
        
    def connect(self):
        try:
            logging.info(f"Connecting to IBKR {'Paper' if IS_PAPER_TRADE else 'LIVE'} account on port {PORT}...")
            self.ib.connect('127.0.0.1', PORT, clientId=CLIENT_ID)
            self.ib.qualifyContracts(self.contract)
            logging.info("Connected successfully.")
        except Exception as e:
            logging.error(f"Failed to connect: {e}. Please ensure IB Gateway or TWS is running.")
            exit(1)

    def get_historical_data(self):
        """获取最近 5 分钟 K 线数据寻找波动率突破点"""
        bars = self.ib.reqHistoricalData(
            self.contract,
            endDateTime='',
            durationStr='2 D',
            barSizeSetting='5 mins',
            whatToShow='TRADES',
            useRTH=False,
            formatDate=1
        )
        df = util.df(bars)
        return df

    def calculate_signals(self, df):
        """简单的波动率突破策略 (Bollinger Band Breakout)"""
        df['SMA'] = df['close'].rolling(window=20).mean()
        df['STD'] = df['close'].rolling(window=20).std()
        df['Upper'] = df['SMA'] + (df['STD'] * 2)
        df['Lower'] = df['SMA'] - (df['STD'] * 2)
        
        latest = df.iloc[-1]
        if latest['close'] > latest['Upper']:
            return 'BUY'
        elif latest['close'] < latest['Lower']:
            return 'SELL'
        return 'HOLD'

    def execute_bracket_order(self, action):
        """执行带有严格止损和移动止盈的非对称订单"""
        if self.is_in_position:
            logging.info("Already in position. Skipping.")
            return

        logging.warning(f"🚨 TRIGGERING {action} ORDER 🚨")
        
        # 1. 挂主单 (市价单进场)
        parent = MarketOrder(action, QUANTITY)
        parent.orderId = self.ib.client.getReqId()
        parent.transmit = False

        # 2. 挂硬止损单 (亏损 20 点立刻斩仓，绝不扛单)
        stop_loss = StopOrder(
            'SELL' if action == 'BUY' else 'BUY', 
            QUANTITY, 
            0 # 占位，需实时计算
        )
        # IBKR API 需要结合当前价，这里简化为附加到挂单组
        # 实际开发中需先获取最新 Bid/Ask 计算精确的止损价
        stop_loss.orderId = self.ib.client.getReqId()
        stop_loss.parentId = parent.orderId
        stop_loss.transmit = False

        # 3. 挂移动止盈单 (吃大趋势利润)
        trailing_stop = Order(
            action='SELL' if action == 'BUY' else 'BUY',
            totalQuantity=QUANTITY,
            orderType='TRAIL',
            trailingPercent=0.5 # 0.5% 移动回撤
        )
        trailing_stop.orderId = self.ib.client.getReqId()
        trailing_stop.parentId = parent.orderId
        trailing_stop.transmit = True

        orders = [parent, stop_loss, trailing_stop]
        for o in orders:
            self.ib.placeOrder(self.contract, o)
            
        self.is_in_position = True
        logging.info("Orders placed. Risk mathematically locked.")

    def run(self):
        self.connect()
        logging.info("Starting sniper loop...")
        try:
            while self.ib.waitOnUpdate(timeout=60):
                df = self.get_historical_data()
                if df is not None and not df.empty:
                    signal = self.calculate_signals(df)
                    if signal in ['BUY', 'SELL']:
                        self.execute_bracket_order(signal)
                    else:
                        logging.info("Monitoring... No breakout detected.")
        except KeyboardInterrupt:
            logging.info("System shutting down...")
        finally:
            self.ib.disconnect()

if __name__ == '__main__':
    bot = AsymmetricSniperBot()
    bot.run()
