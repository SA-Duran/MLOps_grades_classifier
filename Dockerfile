# 1. Choose a base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy your project files into the container
COPY . /app
# Up to date packages and AWS CLI package
RUN apt update -y && apt install awscli -y

# 4. Install dependencies dont save on cache
RUN pip install --no-cache-dir -r requirements.txt

# 6. Define the default command to run when the container starts
CMD ["python", "app.py"]