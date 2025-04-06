from agents.graph_state.graph import run_bitcoin_analysis

def run_chat(content: str):
    res = run_bitcoin_analysis(content=content)
    return res


# if __name__ == '__main__':
#     res = run_chat("Lakukan analisis Bitcoin dan berikan rekomendasi.")
#     print(res)