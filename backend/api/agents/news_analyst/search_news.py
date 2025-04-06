import pandas as pd

from duckduckgo_search import DDGS


def search_news(keyword: str, max_results: int = 15) -> pd.DataFrame:
    """
    Mencari berita berdasarkan keyword dan mengembalikan hasil dalam bentuk pandas DataFrame.
    
    Args:
        keyword (str): Kata kunci pencarian berita
        max_results (int, optional): Jumlah maksimum hasil yang diinginkan. Default: 100
    
    Returns:
        pd.DataFrame: DataFrame berisi hasil pencarian yang sudah diurutkan berdasarkan tanggal
    """
    search_tool = DDGS()
    results = search_tool.news(
        keywords=keyword, 
        safesearch="off", 
        timelimit="m", 
        max_results=max_results
    )
    text = ""
    
    # Konversi hasil ke DataFrame
    df = pd.DataFrame.from_records(results)
    
    
    # Pastikan kolom date ada sebelum mengonversi
    if 'date' in df.columns and not df.empty:

        df["date"] = pd.to_datetime(df.date)
        df = df.sort_values(by="date", ascending=False)

        for date, row in list(df.set_index("date").iterrows()):
            text += f"{date}\n{row.title}\n{row.body}\n-----\n"
        return text
    
    elif not df.empty:
        # Jika tidak ada kolom date, kembalikan DataFrame tanpa date
        for id, row in list(df.set_index("date").iterrows()):
            text += f"{row.title}\n{row.body}\n-----\n"
        return text
        
    else:
        # Jika tidak ada hasil, kembalikan DataFrame kosong
        return "Tidak menemukan berita yang sesuai. "