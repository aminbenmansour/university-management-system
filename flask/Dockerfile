FROM python:3.9.4-buster

WORKDIR /app


ADD . /app


RUN python -m pip install pip==21.0.1 \
    && pip install -r requirements.txt
# RUN pip3 install pipenv \
#     && pipenv install --system --deploy

# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
# RUN chmod +x /wait

# CMD /wait ; uwsgi app.ini
CMD [ "uwsgi", "app.ini" ]