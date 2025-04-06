from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

from agents import AgentState
from agents.llm import LLM

import json

# 3. REPORTER AGENT
def create_report_prompt():
    """Membuat prompt untuk reporter agent"""
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", """
        Anda adalah reporter keuangan profesional yang ahli dalam menyusun laporan analisis cryptocurrency.
        Tugas Anda adalah membuat laporan komprehensif berdasarkan data dan analisis yang diberikan.
        Laporan harus berisi:
        1. Ringkasan eksekutif dengan rekomendasi jelas
        2. Analisis harga dan tren Bitcoin terkini
        3. Penjelasan indikator teknikal (RSI, MACD, EMA)
        4. Penjelasan dari hasil yang didapat dari berita.
        5. Kesimpulan dan saran investasi
        
        Gunakan bahasa yang profesional namun mudah dipahami. Sertakan data-data penting untuk mendukung rekomendasi.
        """),
        MessagesPlaceholder(variable_name="history"),
        ("human", """
        Buatlah laporan analisis Bitcoin berdasarkan data dan analisis teknikal berikut:
        
        Data Bitcoin: {bitcoin_data}
        
        Analisis Teknikal: {technical_analysis}
         
        Analysis Berita: {news_analysis_report}
        
        Format laporan harus profesional dan mudah dibaca.
        """)
    ])
    return prompt_template

def reporter_agent(state: AgentState) -> AgentState:
    """Agent yang bertugas membuat laporan analisis Bitcoin"""
    
    # Mengambil data dari state
    bitcoin_data = state["bitcoin_data"]
    technical_analysis = state["technical_analysis"]
    
    # Membuat model LLM
    # llm = ChatAnthropic(model="claude-3-haiku-20240307")
    
    # Membuat prompt untuk reporter
    reporter_prompt = create_report_prompt()
    
    # Menyiapkan input untuk prompt
    prompt_input = {
        "history": state["messages"],
        "bitcoin_data": json.dumps(bitcoin_data, indent=2),
        "technical_analysis": json.dumps(technical_analysis, indent=2),
        "news_analysis_report":state['news_analysis_report']
    }
    
    # Menjalankan chain untuk generate laporan
    chain = reporter_prompt | LLM | StrOutputParser()
    report = chain.invoke(prompt_input)
    
    # Membuat pesan reporter
    reporter_message = {
        "role": "assistant",
        "content": "Saya telah menyusun laporan lengkap analisis Bitcoin berdasarkan data dan analisis teknikal."
    }
    
    # Update state
    new_messages = state["messages"] + [reporter_message]
    
    return {
        "messages": new_messages,
        # "next": END,
        "bitcoin_data": bitcoin_data,
        # "technical_analysis": technical_analysis,
        "report": report
    }