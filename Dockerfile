FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip3 install -r docker_requirements.txt
EXPOSE 8501
CMD streamlit run app.py