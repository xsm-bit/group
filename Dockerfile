From python
WORKDIR /APP
COPY . /APP
RUN pip install update
RUN pip install -r requirements.txt

ENV TLG_ACCESS_TOKEN=6850550531:AAHhGfjWBXulL7P-54cHqsU1t38qDv-6XGU
ENV REDIS_HOST=redis-12507.c252.ap-southeast-1-1.ec2.cloud.redislabs.com
ENV REDIS_PASSWORD=qTvZ7L7a5yAhEhj0RxABL6QD76TL7UAo
ENV REDIS_PORT=12507
ENV GPT_TOKEN=cbe5baf8-6d92-4f91-ab74-f14624611242

CMD python chatbot.py

