# Use public python 3.8 image
FROM python:3.8

# Add our code into the /app dir inside the container
ADD src/ /app

# Set our working directory to the new /app folder
WORKDIR /app

# Install pip requirements
RUN pip install -r requirements.txt

# command to run on container start
CMD [ "python", "./main.py" ]