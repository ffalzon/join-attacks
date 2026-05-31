FROM python:3.12-trixie

RUN apt update && apt install -y tmux
RUN pip3 install faker

# Create group and user to avoid permissions issues with local user/group
# when editing files in and out of docker container.
# Note: GNU/Linux systems assign the default 1000 User Identifier (UID) and
# Group Identifier (GID) to the first account created during installation. It is
# possible that your local UID and GID on your machine may be different, in that
# case you should edit the values in the commands below.
# You can see your UID and GID(s) by executing: `id`
RUN addgroup --gid 1000 artifact
RUN adduser --disabled-password --gecos "" --uid 1000 --gid 1000 artifact
ENV HOME=/home/artifact
USER artifact