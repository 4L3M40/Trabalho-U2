# ================= CONFIGURAÇÕES =================

# Conta / Conexão
ACCOUNT = {
    "49057967": None,  # definido pelo terminal
    "password": None,  # use variável de ambiente MT5_PASSWORD
    "HFMarketsGlobal-Demo": None,  # definido pelo terminal
    "path": None,  # caminho opcional do terminal
}

# Símbolo
SYMBOL = "XAUUSD"
LOT = 0.10
DEVIATION = 20
MAGIC = 234000

# Estratégia
STRATEGY_MODE = "trend_pullback"   # opções: crossover, trend, trend_pullback

# Timeframes
FAST_TIMEFRAME = "M5"
CONFIRM_CHAIN = ["M15", "M30"]
CONFIRM_POLICY = "weighted"  # "all", "any", "weighted"

# Regras de reentrada
REENTER_COOLDOWN_BARS = 3
CLOSE_ON_OPPOSITE = True

# RSI
RSI_ON = True
RSI_PERIOD = 14
RSI_OVERBOUGHT = 80
RSI_OVERSOLD = 30

# Stops e Alvos
STOP_LOSS_POINTS = 200
TAKE_PROFIT_POINTS = 200

# Multi-TP
MULTI_TP = True
TP_FRACTIONS = [0.4, 0.35, 0.25]
TP_POINTS = [150, 200, 250]

# CSV Log
CSV_LOG = True
CSV_FILE = "trades_log.csv"
