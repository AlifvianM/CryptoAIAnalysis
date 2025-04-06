from langgraph.graph import StateGraph, END, START

# from state.state import AgentState
from agents.news_analyst.agents import search_agent
from agents.price_analyst.analyst import analyst_agent
from agents.price_analyst.price import researcher_agent
from agents.reporter.agents import reporter_agent

from agents import AgentState

## Fungsi untuk mengatur alur antar agen
# def router(state: AgentState) -> str:
#     """Router untuk menentukan agen berikutnya"""
#     return state["next"]

# Membangun graph
def build_bitcoin_analysis_graph():
    # Membuat state graph
    workflow = StateGraph(AgentState)
    
    # workflow.add_node("search", execute_search)
    # workflow.add_edge(START,"search")
    # workflow.add_edge("search",END)

    # Menambahkan node untuk setiap agen
    workflow.add_node("researcher", researcher_agent)
    workflow.add_node("analyst", analyst_agent)
    workflow.add_node("reporter", reporter_agent)
    workflow.add_node("search_agent", search_agent)
    
    # # Menambahkan edge (connection) antar node
    workflow.add_edge(START,"researcher")
    workflow.add_edge(START,"search_agent")
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("search_agent", "reporter")
    workflow.add_edge("analyst", "reporter")
    # workflow.add_edge("reporter", END)
    
    # # Mengatur start node dan conditionals
    # workflow.set_entry_point(START)
    # workflow.set_finish_point(END)
    # workflow.add_conditional_edges("researcher", router)
    # workflow.add_conditional_edges("analyst", router)
    # workflow.add_conditional_edges("reporter", router)
    
    # Compile graph
    return workflow.compile()

# Fungsi utama untuk menjalankan sistem
def run_bitcoin_analysis(content: str):
    # Membangun graph
    graph = build_bitcoin_analysis_graph()


    # display(Image(graph.get_graph().draw_mermaid_png()))
    
    # State awal
    initial_state = {
        "messages": [
            {
                "role": "human",
                "content": f"{content}" #Lakukan analisis Bitcoin dan berikan rekomendasi.
            }
        ],
        # "next": "researcher",
        "bitcoin_data": {},
        "technical_analysis": {},
        "report": ""
    }
    
    # Menjalankan graph
    for output in graph.stream(initial_state):
        for key, value in output.items():
            node = key[0]
            state = value
            
            # Cetak output dari setiap agen
            if node != "__end__":
                last_message = state["messages"][-1]["content"]
                print(f"\n=== {node.upper()} ===")
                print(last_message)
    
    # Menampilkan laporan akhir
    # print("Last Output :", output)
    final_state = output['reporter']['report']
    # print("\n=== LAPORAN LENGKAP ===")
    # display(Markdown(final_state))
    
    return final_state