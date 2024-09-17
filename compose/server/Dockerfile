FROM python:3.10-slim-buster

# These environment values help with watching for file changes
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system-level dependencies.
RUN apt-get update && apt-get install -y \ 
    build-essential gcc libpq-dev libjpeg-dev zlib1g-dev python3-pip cura

ENV CURA_ENGINE_SEARCH_PATH=/usr/share/cura/resources/definitions

# Set the name of the working directory inside the docker container
WORKDIR /app

# Install pipenv and create a virtual environment with it.
COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

# Install Python packages from the Pipfile at the system level,
# since virtual environments are not needed in containers.
RUN pip3 install pipenv \
    && pipenv install  --dev --system --deploy --ignore-pipfile

# Move the 'start' shell script to the root
# and alter line endings for compatibility.
COPY ./compose/server/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
