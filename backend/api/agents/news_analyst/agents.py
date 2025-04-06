from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from agents.news_analyst.search_news import search_news

from agents.llm import LLM
from agents import AgentState



def generate_keyword(user_input: str):
    SYSTEM_MESSAGE = """
        Kamu adalah pengumpul berita yang sangat handal mencari berita. Carilah berita yang sekiranya relevan dalam bahasa inggris atau indonesia dari pertanyaan yang diajukan oleh user. 
        User merupakan orang yang bekerja dalam bidang analisa bitcoin yang dimana dia akan bertanya tentang bagaimana perkembangan coin yang ingin di analisa. Dari pertanyaan yang dilempar oleh user, buat search keyword sesuai yang dimaksud user agar dapat dicari beritanya di browser.
        Berikan tambahan keterangan waktu tahun sekarang agar berita yang dicari nanti lebih update.
        
        Berikut contoh yang dapat membantumu

        human : Lakukan analisis Bitcoin dan berikan rekomendasi
        system : bitcoin market growth in 2025

        human : Lakukan analisis Bitcoin dan berikan rekomendasi
        system : bagaimana trend market bitcoin pada tahun 2025
    """
    news_prompt = ChatPromptTemplate(
        [
            ("system", SYSTEM_MESSAGE),
            ("human", "{user_input}"),
        ]
    )

    chain_news = news_prompt | LLM | StrOutputParser()
    res = chain_news.invoke(user_input)
    return res, user_input

def search_agent(state: AgentState) -> AgentState:
    last_chat = generate_keyword(state["messages"][0]['content'])[0]
    user_input = generate_keyword(state["messages"][0]['content'])[1]

    news = search_news(keyword=last_chat)
    # print(news)

    prompt = f"""Pilihlah kombinasi sentiment yang merepresentasikan tentang berita yang telah didapat:

            ```
            {news}
            ```

            Setiap artikel dipisahkan oleh `-----`.

            Pilih angka untuk sentiment antara 0 sampai 100 yang dimana:

            - 0 adalah sangat negatif (bearish)
            - 100 adalah sangat positif (bullish)

            Balas hanya dengan sentimen dan penjelasan singkat (1-2 kalimat) tentang alasannya.

            Saat membuat jawaban, fokuslah untuk menjawab pertanyaan pengguna:
            {user_input}
    """

    response = LLM.invoke([HumanMessage(prompt)])

    reporter_message = {
        "role": "assistant",
        "content": f'Saya telah mendapatkan berita tentang {user_input} analisis Bitcoin berdasarkan data dan analisis teknikal.'
    }
    
    # Update state
    new_messages = state["messages"] + [reporter_message]

    return {
        "messages": new_messages,
        "news_data": state.get("news_data", new_messages),
        "news_analysis_report":response.content
    }
