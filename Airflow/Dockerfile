FROM apache/airflow:3.1.6

# Switch to root to install system dependencies (if needed)
USER root
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

# Switch back to airflow user to install python packages
USER airflow

# Copy requirements file
COPY requirements.txt /requirements.txt

# Install dbt-trino (this automatically installs dbt-core)
RUN pip install --no-cache-dir -r /requirements.txt