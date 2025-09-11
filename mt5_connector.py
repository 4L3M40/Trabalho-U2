# mt5_connector.py (atualizado)
import MetaTrader5 as mt5
from datetime import datetime
import math
import pandas as pd

from config import (
    SYMBOL, LOT, DEVIATION, MAGIC,
    STOP_LOSS_POINTS, MULTI_TP, TP_FRACTIONS, TP_POINTS
)

# ------------------------
# Utilidades
# ------------------------
def _normalize_price(symbol, price: float) -> float:
    info = mt5.symbol_info(symbol)
    digits = info.digits if info else 2
    factor = 10 ** digits
    return math.floor(price * factor) / factor

def _ensure_symbol(symbol: str) -> bool:
    info = mt5.symbol_info(symbol)
    if info is None:
        print(f"[ERRO] Símbolo {symbol} não encontrado no terminal.")
        return False
    if not info.visible:
        mt5.symbol_select(symbol, True)
    return True

def _broker_filling(symbol: str):
    """
    Decide o type_filling compatível com a corretora/símbolo:
    0=FOK, 1=IOC, 2=RETURN.
    """
    info = mt5.symbol_info(symbol)
    if not info:
        # fallback seguro
        return mt5.ORDER_FILLING_FOK
    # info.filling_mode: 0=FOK, 1=IOC, 2=RETURN
    if info.filling_mode == 1:
        return mt5.ORDER_FILLING_IOC
    elif info.filling_mode == 0:
        return mt5.ORDER_FILLING_FOK
    else:
        return mt5.ORDER_FILLING_RETURN

def _retry_fillings(request: dict):
    """
    Envia a ordem tentando preenchimentos na sequência:
    [filling do broker] -> IOC -> FOK -> RETURN.
    Volta o primeiro sucesso.
    """
    tried = []
    # primeira tentativa com o filling escolhido
    first = request.get("type_filling")
    order = mt5.order_send(request)
    tried.append((first, order))

    # Se inválido, tenta outras opções
    if order and hasattr(order, "retcode") and order.retcode in (10030, getattr(mt5, "TRADE_RETCODE_INVALID_FILL", 10030)):
        for candidate in [mt5.ORDER_FILLING_IOC, mt5.ORDER_FILLING_FOK, mt5.ORDER_FILLING_RETURN]:
            if candidate == first:
                continue
            request["type_filling"] = candidate
            order2 = mt5.order_send(request)
            tried.append((candidate, order2))
            if order2 and hasattr(order2, "retcode") and order2.retcode == getattr(mt5, "TRADE_RETCODE_DONE", 10009):
                # sucesso
                print(f"[{datetime.now()}] Retry filling OK -> {candidate}")
                return order2

    # retorna o último/primeiro resultado
    return tried[-1][1] if tried else order

# ------------------------
# Conexão / Dados
# ------------------------
def connect_mt5():
    if not mt5.initialize():
        print("Falha ao inicializar MT5:", mt5.last_error())
        return False
    return True

def disconnect_mt5():
    mt5.shutdown()

def get_data(timeframe=mt5.TIMEFRAME_M5, n=200):
    if not _ensure_symbol(SYMBOL):
        return None
    rates = mt5.copy_rates_from_pos(SYMBOL, timeframe, 0, n)
    if rates is None:
        return None
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df

# ------------------------
# Execução de ordens
# ------------------------
def _build_request(side: str, volume: float, price: float, sl: float, tp: float, filling=None):
    return {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY if side == "BUY" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": DEVIATION,
        "magic": MAGIC,
        "comment": "Python Bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": filling if filling is not None else _broker_filling(SYMBOL),
    }

def send_order(side: str):
    if not _ensure_symbol(SYMBOL):
        return None

    info = mt5.symbol_info(SYMBOL)
    tick = mt5.symbol_info_tick(SYMBOL)
    if not tick or not info:
        print("[ERRO] Sem tick/info do símbolo.")
        return None

    point = info.point
    price = tick.ask if side == "BUY" else tick.bid
    price = _normalize_price(SYMBOL, price)

    sl = price - STOP_LOSS_POINTS * point if side == "BUY" else price + STOP_LOSS_POINTS * point
    tp = price + TP_POINTS[0] * point    if side == "BUY" else price - TP_POINTS[0] * point

    sl = _normalize_price(SYMBOL, sl)
    tp = _normalize_price(SYMBOL, tp)

    request = _build_request(side, LOT, price, sl, tp)
    result = _retry_fillings(request)
    return result


def send_order_multi_tp(side: str):
    if not _ensure_symbol(SYMBOL):
        return None

    info = mt5.symbol_info(SYMBOL)
    tick = mt5.symbol_info_tick(SYMBOL)
    if not tick or not info:
        print("[ERRO] Sem tick/info do símbolo.")
        return None

    point = info.point
    price = tick.ask if side == "BUY" else tick.bid
    price = _normalize_price(SYMBOL, price)

    results = []
    for frac, tp_pts in zip(TP_FRACTIONS, TP_POINTS):
        vol = round(LOT * frac, 2)
        sl = price - STOP_LOSS_POINTS * point if side == "BUY" else price + STOP_LOSS_POINTS * point
        sl = _normalize_price(SYMBOL, sl)

        if tp_pts:
            tp = price + tp_pts * point if side == "BUY" else price - tp_pts * point
            tp = _normalize_price(SYMBOL, tp)
        else:
            tp = 0.0

        req = _build_request(side, vol, price, sl, tp)
        res = _retry_fillings(req)
        results.append(res)

    return results
