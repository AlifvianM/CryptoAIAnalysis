from datetime import datetime, timedelta
from agents import AgentState
import pandas as pd

# 2. ANALYST AGENT
# Bertanggung jawab untuk menganalisa indikator teknikal
def calculate_technical_indicators(data):
    """Menghitung indikator teknikal RSI, EMA, dan MACD"""
    df = pd.DataFrame(data)
    
    # Konversi kolom price ke numeric
    df['price'] = pd.to_numeric(df['price'])
    
    # Menghitung RSI (Relative Strength Index)
    delta = df['price'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # Menghitung EMA (Exponential Moving Average)
    df['EMA_12'] = df['price'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['price'].ewm(span=26, adjust=False).mean()
    
    # Menghitung MACD (Moving Average Convergence Divergence)
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal_Line'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
    
    # Menghapus baris dengan NaN values
    df = df.dropna()
    
    # Mengambil data terbaru untuk analisis
    latest_data = df.iloc[-1]
    previous_data = df.iloc[-2]
    
    # Analisis RSI
    rsi_value = latest_data['RSI']
    rsi_status = "Oversold" if rsi_value < 30 else "Overbought" if rsi_value > 70 else "Neutral"
    
    # Analisis MACD
    macd_value = latest_data['MACD']
    signal_value = latest_data['Signal_Line']
    macd_status = "Bullish" if macd_value > signal_value else "Bearish"
    
    # Analisis EMA
    ema_12 = latest_data['EMA_12']
    ema_26 = latest_data['EMA_26']
    ema_status = "Bullish" if ema_12 > ema_26 else "Bearish"
    
    # Keputusan rekomendasi
    bullish_signals = 0
    total_signals = 3
    
    if rsi_status == "Oversold":
        bullish_signals += 1
    elif rsi_status == "Overbought":
        bullish_signals -= 1
        
    if macd_status == "Bullish":
        bullish_signals += 1
        
    if ema_status == "Bullish":
        bullish_signals += 1
    
    recommendation = ""
    if bullish_signals >= 2:
        recommendation = "BELI"
    elif bullish_signals <= -1:
        recommendation = "JUAL"
    else:
        recommendation = "TAHAN"
    
    return {
        "data": df.to_dict(orient='records'),
        "indicators": {
            "price": latest_data['price'],
            "rsi": {
                "value": round(rsi_value, 2),
                "status": rsi_status
            },
            "macd": {
                "value": round(macd_value, 4),
                "signal": round(signal_value, 4),
                "status": macd_status
            },
            "ema": {
                "ema_12": round(ema_12, 2),
                "ema_26": round(ema_26, 2),
                "status": ema_status
            }
        },
        "recommendation": recommendation,
        "analysis_date": datetime.now().strftime('%Y-%m-%d')
    }

def analyst_agent(state: AgentState) -> AgentState:
    """Agent yang bertugas melakukan analisis teknikal pada data Bitcoin"""
    
    # Mengambil data dari state
    bitcoin_data = state["bitcoin_data"]
    
    if bitcoin_data["status"] == "success":
        # Melakukan analisis teknikal
        analysis_result = calculate_technical_indicators(bitcoin_data["data"])
        
        # Membuat pesan analisis
        recommendation = analysis_result["recommendation"]
        indicators = analysis_result["indicators"]
        
        analyst_message = {
            "role": "assistant",
            "content": f"""
Saya telah menganalisis data Bitcoin dan berikut hasilnya:

1. Harga terakhir: ${indicators['price']:.2f}
2. RSI: {indicators['rsi']['value']} ({indicators['rsi']['status']})
3. MACD: {indicators['macd']['value']} dengan Signal Line: {indicators['macd']['signal']} ({indicators['macd']['status']})
4. EMA 12 vs 26: {indicators['ema']['ema_12']} vs {indicators['ema']['ema_26']} ({indicators['ema']['status']})

Berdasarkan analisis teknikal, rekomendasi saat ini adalah: {recommendation}
            """
        }
    else:
        analyst_message = {
            "role": "assistant",
            "content": "Tidak dapat melakukan analisis karena data tidak tersedia."
        }
    
    # Update state
    new_messages = state["messages"] + [analyst_message]
    
    return {
        "messages": new_messages,
        # "next": "reporter" if bitcoin_data["status"] == "success" else END,
        # "bitcoin_data": bitcoin_data,
        "technical_analysis": analysis_result if bitcoin_data["status"] == "success" else {},
        # "report": state.get("report", "")
    }