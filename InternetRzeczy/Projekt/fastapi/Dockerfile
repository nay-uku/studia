FROM odoku/scikitlearn

COPY . /app
WORKDIR /app

RUN pip3 install -r req.txt

EXPOSE 8000

CMD uvicorn main:app --reload --host 0.0.0.0