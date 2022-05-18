# Use the official image as a parent image.
FROM photon:3.0

# Set the working directory.
WORKDIR /usr/src/app

RUN tdnf install -y python3 python3-pip

# Copy the rest of your app's source code from your host to your image filesystem.
COPY requirements.txt .

RUN pip3 install -r requirements.txt

# Copy the rest of your app's source code from your host to your image filesystem.
COPY . .

ENV USER=root

# ENV HTTP_PROXY=http://proxy.vmware.com:3128
# ENV HTTPS_PROXY=http://proxy.vmware.com:3128

EXPOSE 80/tcp

CMD  ["python3", "server.py"]
