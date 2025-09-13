FROM python:3.9

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /code

EXPOSE 8123

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8123", "--reload"]