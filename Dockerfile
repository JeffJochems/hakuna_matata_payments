FROM python:3-alpine

# Set environment variables
ENV HAKUNA_MATATA_PATH=/opt/hakuna_matata \
    HAKUNA_MATATA_APP_PATH=/opt/hakuna_matata/payments_app 

# Install dependencies
RUN apk update && \
      apk add git && \
      apk add curl openrc nano 

# Create directory structures
RUN mkdir -p $HAKUNA_MATATA_PATH $HAKUNA_MATATA_APP_PATH

# Copy source code to the application directory
COPY . $HAKUNA_MATATA_APP_PATH

# Install dependencies from the requirements.txt
RUN cd $HAKUNA_MATATA_APP_PATH && \
    pip install -r requirements.txt

# Set the production working directory to the application directory
WORKDIR $HAKUNA_MATATA_APP_PATH/src

# Setup crontab
RUN crontab crontab
RUN touch /var/log/cron.log

CMD crond -f -l 2
