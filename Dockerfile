FROM python:3.8

RUN pip install pillow

# Copy your Python script 
COPY image_processing /app/

WORKDIR /app/

# Specify the command to run your script
CMD ["python", "image_processing.py"]
