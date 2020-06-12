# Notes
# -----
# 1. Uses a debian based system, not Alpine
# 1. Assumes application is configurable via environment variables,
#    and that there is a single settings.py file
# 1. Assumes Django based application. For Flask, you will delete the collectstatic command. 
#    Also, the wsgi application name in the ENTRYPOINT will also differ slightly.
# 1. This installs Postgres *AND* MySQL in separate steps. 
#    Delete either one or both depending on your use case
# 1. We create a user without any permissions, not even write permissions. This means you cannot 
#    write logs or create directories. You should write logs to stdout / stderr instead.
#

# This base image uses Debian operating system

FROM python:3.7.4

# This forces python to not buffer output / error
ENV PYTHONUNBUFFERED 1

# This is where we will copy all our code
# Workdir creates the directory if it doesn't exist
WORKDIR /code

# This is needed later when we install libxml2
RUN set - ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends python-dev python3-dev python3-dev python3-lxml 


# Install libxml2 before installing the other dependencies
# libxml2 requires installing dev packages, and is usually slower
# So we cache it in a separate layer
# And also clean up APT when done.
RUN apt-get install -y aptitude
RUN aptitude install -y libxml2-dev libxml2 libxmlsec1-dev \
    && aptitude install -y libxslt1-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# RUN redis-server --daemonize yes

# ---------------------------------------------
# From here, the steps are application specific
# ---------------------------------------------

# These below take more time to install, so cache it.
RUN pip3 install --upgrade pip
RUN pip3 install setuptools --upgrade

# Now copy requirements.txt and install all dependencies
# As a best practice, you should pin down version numbers in requirements.txt
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the remaining code
# Avoid copying the current working directory,
# as that will have unnecessary files
COPY manage.py .

COPY apiservices apiservices
COPY settings.ini .

# Generate static files
# Note that we pass a dummy secret key
# This secret key is not used when the server is actually started
# RUN SECRET_KEY=ignore python3 manage.py collectstatic --noinput

# Switch to gunicorn user
# This makes our container a lot more secure
# USER gunicorn

# Declare some default values
# These can be overidden when the container is run
ENV PORT 8001
ENV NUM_WORKERS 4
ENV LOG_LEVEL ERROR
ENV DEBUG False

# Start gunicorn with the following configuration
# - Number of workers and port can be overridden via environment variables
# - All logs are to stdout / stderr
# - Access log format is modified to include %(L)s - which is the request time in decimal seconds

CMD rm -f db.sqlite3 && \
    # python3 manage.py collectstatic --no-input && \
    python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    python3 manage.py initadmin && \
    gunicorn -b 0.0.0.0:$PORT --workers $NUM_WORKERS \
    --name apiservices \
    --access-logfile '-' --error-logfile '-' --log-level $LOG_LEVEL \
    --access-logformat '%(h)s %(l)s %(u)s %(t)s %(L)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' \
    apiservices.wsgi



# FROM mongo:3.2.6

# ENV PORT 27017:27017
# # EXPOSE 27017:27017
# RUN sudo service mongod start
# RUN mongo
