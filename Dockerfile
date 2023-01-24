FROM python:3.11-slim
WORKDIR /APP
COPY . /APP
RUN python -m pip install -r requirements.txt && \
    rm -r requirements.txt && \
    mkdir music/youtube \

CMD ["python", "main.py"]