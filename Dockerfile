# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

FROM alpine:3.18
ENV gemini_api_key=AIzaSyB560cWsxSu4h7xpL2-KUAl3kemuSh0isI
ENV host=72.52.176.216


# Install Python and other dependencies
RUN apk add --no-cache python3 py3-pip gcc musl-dev python3-dev libffi-dev openssl-dev



# Set the working directory
WORKDIR /app

# Copy the application code to the working directory
COPY . .

# Ensure requirements.txt is present
RUN ls -l /app

# Install the required Python packages
RUN pip3 install --no-cache-dir -r requirements.txt
# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
CMD chainlit run --host 0.0.0.0 --port 3000 app.py -w
