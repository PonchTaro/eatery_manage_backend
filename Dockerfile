FROM python:3.7
ADD /app
ADD ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir  -r /app/requirements.txt
EXPOSE 8000
ADD ./eatery_manage_backend/start.sh /start.sh
CMD ["/bin/bash", "/start.sh"]