def crossover_signal(df):
    if df is None or len(df) < 2:
        return None
    last = df.iloc[-1]
    prev = df.iloc[-2]
    if last.MA_SHORT > last.MA_LONG and prev.MA_SHORT <= prev.MA_LONG:
        return "BUY"
    if last.MA_SHORT < last.MA_LONG and prev.MA_SHORT >= prev.MA_LONG:
        return "SELL"
    return None

def trend_signal(df):
    if df is None or len(df) < 1:
        return None
    last = df.iloc[-1]
    if last.MA_SHORT > last.MA_LONG:
        return "BUY"
    elif last.MA_SHORT < last.MA_LONG:
        return "SELL"
    return None

def check_signal(df, strategy="trend_pullback"):
    if strategy == "crossover":
        return crossover_signal(df)
    elif strategy == "trend":
        return trend_signal(df)
    elif strategy == "trend_pullback":
        return trend_signal(df)  # simplificado por enquanto
    return None
