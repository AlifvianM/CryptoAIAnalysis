import requests


def get_requests(question: str):
    url = "http://127.0.0.1:8000/api/chat"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "question": question
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

if __name__ == '__main__':
    res = get_requests("Lakukan analisis Bitcoin dan berikan rekomendasi.")
    print(res)