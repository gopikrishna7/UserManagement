FROM python
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
ENV FLASK_APP=usermanagement.py
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--access-logfile", "-", "--error-logfile", "-", "usermanagement:app"]
