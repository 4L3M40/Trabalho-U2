import pandas as pd
import numpy as np

def moving_averages(df: pd.DataFrame, short: int = 9, long: int = 21) -> pd.DataFrame:
    df = df.copy()
    df["MA_SHORT"] = df["close"].rolling(window=short, min_periods=short).mean()
    df["MA_LONG"]  = df["close"].rolling(window=long,  min_periods=long).mean()
    return df

def rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Adiciona a coluna 'RSI' com suavização de Wilder (EMA alpha=1/period)."""
    df = df.copy()
    close = df["close"].astype(float)
    delta = close.diff()

    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)

    gain = pd.Series(gain, index=df.index)
    loss = pd.Series(loss, index=df.index)

    # Wilder's smoothing (RSI clássico)
    avg_gain = gain.ewm(alpha=1/period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1/period, adjust=False, min_periods=period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))

    # Se avg_loss == 0 (sem perdas), define RSI=100; limita entre 0 e 100
    rsi = rsi.fillna(100.0).clip(0, 100)

    df["RSI"] = rsi
    return df
