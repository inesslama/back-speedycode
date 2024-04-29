FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
EXPOSE 8088
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8088","--reload"]