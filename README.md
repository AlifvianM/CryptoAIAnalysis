# Crypto AI Assistant

This is a repo for Crypto AI Analysis for assisting user that wanna buy crypto. With the power Langchain we creating multi agents AI to create a chatbot where user can ask what coin that he want to buy. For analysis go check `crypto_analysis/main_analysis.ipynb` and for dev go check `frontend` and `backend`.

## Dont Forget
* You need to have 1 `api_key` that related with OpenAI to get chatgpt LLM model power source. Save it in your `.env` file.
* on `backend/api/agents/llm.py` it has param called `api_key`. after you set your key on your .env file, delete the params. 
