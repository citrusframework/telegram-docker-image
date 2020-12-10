FROM python:3.8.1-slim-buster

ENV USER_UID=1001 \
    APP_DIR=/app

USER 0

RUN python3 -m pip install telethon && \
    python3 -c "import telethon; print(telethon.__version__)"

ADD *.py ${APP_DIR}/

RUN chgrp -R 0 ${APP_DIR} && \
    chmod -R g=u ${APP_DIR}

USER ${USER_UID}

CMD python3 ${APP_DIR}/send_message.py

