FROM python:3.14-slim
WORKDIR /python_data_loader
LABEL "author"="Cait"
LABEL "nuzlucke.dataloader.version"="1.0.0A"
LABEL "nuzlucke.release-date"="2026-02-18"
LABEL "description"="This is the dataloader for the Nuzlucke project. This is built using Python 3.14, and populates the database using data from PokeApi"

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["python", "Main.py"]