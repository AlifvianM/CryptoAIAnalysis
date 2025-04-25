FROM python:3.9

WORKDIR /frontend_app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "mainApp.py"]