# Tipe data untuk state
from typing import TypedDict, List, Dict, Any, Annotated, Literal
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    # next: str
    bitcoin_data: Dict
    news_data: str
    technical_analysis: Dict
    news_analysis_report: str
    report: str

# Fungsi untuk memformat pesan ke format yang dapat diproses oleh model
def format_messages(state):
    return {"messages": state["messages"]}