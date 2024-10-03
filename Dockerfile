FROM python:3.10.15-bookworm

WORKDIR app/

COPY ./app .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt



EXPOSE 8501
CMD ["streamlit", "run", "main.py"]