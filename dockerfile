# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /code
WORKDIR /code

# Install dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev  # or any other necessary dependencies

COPY requirement.txt /code/
RUN pip install --upgrade pip && pip install -r requirement.txt

# Copy the current directory contents into the container at /code
COPY . /code/



# Open port 8000 to the outside world
EXPOSE 8001


# Migrate the database
RUN python social_networking/manage.py makemigrations
RUN python social_networking/manage.py migrate




# Define the default command to run when the container starts
CMD ["gunicorn", "--bind", "localhost:8000", "social_networking.wsgi:application"]
