import time
from datetime import datetime
from config import SYMBOL, STRATEGY_MODE, FAST_TIMEFRAME, CONFIRM_CHAIN, CONFIRM_POLICY, CSV_LOG, CSV_FILE
from mt5_connector import connect_mt5, disconnect_mt5, get_data, send_order
from indicators import moving_averages, rsi
from strategy import check_signal
import pandas as pd

if not connect_mt5():
    print("Não conectou ao MT5. Encerrando.")
    exit()

print(f"[INFO] Símbolo em uso: {SYMBOL} (auto=True)")
print(f"[INFO] Estratégia: {STRATEGY_MODE} | TF rápido: {FAST_TIMEFRAME} | Confirmação: {CONFIRM_CHAIN}({CONFIRM_POLICY})")
print("[INFO] RSI ON | period=14 | OB=80 | OS=30")

if CSV_LOG:
    pd.DataFrame(columns=["datetime","symbol","side","price","profit"]).to_csv(CSV_FILE, index=False)

last_side = None

while True:
    df = get_data()
    if df is None:
        time.sleep(60)
        continue

    df = moving_averages(df)
    df = rsi(df)
    signal = check_signal(df, STRATEGY_MODE)

    if signal and signal != last_side:
        result = send_order(signal)
        print(f"[{datetime.now()}] Ordem enviada ({signal}) | Resultado: {result}")
        last_side = signal
        if CSV_LOG:
            with open(CSV_FILE, "a") as f:
                f.write(f"{datetime.now()},{SYMBOL},{signal},{df.iloc[-1].close},0\n")
    else:
        print(f"[{datetime.now()}] Sem novo sinal.")

    time.sleep(60)
