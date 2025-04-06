import requests
headers = {
    # 'User-Agent': 'Mozilla/5.0',
    'accept': 'application/json',
    'Content-Type': 'application/json'
}


def get_requests(question: str):
    payload = {
        'question':f'{question}',
    }
    url = "http://127.0.0.1:8000/api/chat"
    response = requests.post(
        url, 
        headers=headers, 
        data=payload
    )

    print('Response :', response)
    return response