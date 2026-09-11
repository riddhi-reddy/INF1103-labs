FROM python:3.12-slim

WORKDIR /usr/src/app

COPY auditor.py .

CMD ["python", "auditor.py"]
