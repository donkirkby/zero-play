#!/usr/bin/env bash
# This script is designed to reproduce the Travis CI build on your local
# workstation. You'll probably need to run it with sudo.
# Any new files get written by the user id 2000.
# Based on https://stackoverflow.com/a/49019950/4794
# The instance id at the top of the Travis log doesn't exactly match the docker
# tag. For example, this instance id:
#     travis-ci-ubuntu-1804-1593521679-ca42795e
# matches this docker tag:
#     travisci/ci-ubuntu-1804:packer-1593521720-ca42795e
#                                    timestamp^  git id^
# The timestamps should be similar, and the git commit ids should be the same.
# More info:
# https://github.com/travis-ci/packer-templates/blob/master/ci-ubuntu-1804.yml
# If your install steps are slow, commit the finished installation to a new
# docker tag like this:
#     sudo docker ps
#     sudo docker commit <container id> zero-play:test
# Then you can shortcut the install steps by launching this script with the new
# docker tag:
#     sudo ./travis-local.sh zero-play:test

set -e
DOCKER_TAG=${1:-travisci/ci-ubuntu-1804:packer-1593521720-ca42795e}
docker run --rm --name travis-build -dit \
  --mount type=bind,source=`pwd`,target=/home/travis/zero-play \
  $DOCKER_TAG /sbin/init

echo "Now run 'su - travis' and activate the virtualenv at ~/virtualenv/python3.8."
echo "Then follow all the steps from your Travis CI script."
echo "The project is mounted in /home/travis/zero-play."
docker exec -it travis-build bash -l
docker stop travis-build
