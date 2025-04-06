from datetime import datetime, timedelta
from typing import Dict
from agents import AgentState

import requests

# 1. RESEARCHER / DATA ENGINEER AGENT
# Bertanggung jawab untuk mengambil data dari CoinGecko
def fetch_bitcoin_data() -> Dict:
    """Mengambil data Bitcoin dari CoinGecko API"""
    # Endpoint untuk data historis Bitcoin
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    
    # Parameter untuk data 30 hari terakhir
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    params = {
        "vs_currency": "usd",
        "days": "30",
        "interval": "daily"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Proses data untuk dibuat lebih terstruktur
        prices = data.get("prices", [])
        volumes = data.get("total_volumes", [])
        market_caps = data.get("market_caps", [])
        
        processed_data = []
        for i in range(len(prices)):
            timestamp = prices[i][0]
            date = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d')
            price = prices[i][1]
            volume = volumes[i][1] if i < len(volumes) else None
            market_cap = market_caps[i][1] if i < len(market_caps) else None
            
            processed_data.append({
                "date": date,
                "price": price,
                "volume": volume,
                "market_cap": market_cap
            })
        
        return {
            "data": processed_data,
            "status": "success",
            "message": f"Berhasil mengambil data Bitcoin untuk {len(processed_data)} hari terakhir"
        }
    except Exception as e:
        return {
            "data": [],
            "status": "error",
            "message": f"Gagal mengambil data: {str(e)}"
        }

def researcher_agent(state: AgentState) -> AgentState:
    """Agent yang bertugas mengambil dan menyiapkan data Bitcoin"""
    # Mengambil data dari CoinGecko
    bitcoin_data = fetch_bitcoin_data()
    
    # Mempersiapkan pesan untuk agent berikutnya
    if bitcoin_data["status"] == "success":
        researcher_message = {
            "role": "assistant",
            "content": f"Saya telah mengambil data Bitcoin dari CoinGecko. {bitcoin_data['message']}. Data siap untuk dianalisis."
        }
    else:
        researcher_message = {
            "role": "assistant",
            "content": f"Terjadi kesalahan saat mengambil data: {bitcoin_data['message']}"
        }
    
    # Update state
    new_messages = state["messages"] + [researcher_message]
    
    return {
        "messages": new_messages,
        # "next": "analyst" if bitcoin_data["status"] == "success" else END,
        "bitcoin_data": bitcoin_data,
        # "technical_analysis": state.get("technical_analysis", {}),
        # "report": state.get("report", "")
    }

