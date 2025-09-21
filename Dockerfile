FROM python:3.12.3-alpine3.20
ENV MAIN app/
WORKDIR $MAIN
COPY requirements.txt .
COPY yamscrolb.py .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["yamscrolb.py"]