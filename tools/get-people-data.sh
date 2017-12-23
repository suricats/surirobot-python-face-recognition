#!/usr/bin/env bash

. $(dirname "$0")/../.env

curl --user ${REMOTE_DATA_LOGIN}:${REMOTE_DATA_PASSWD} https://suri.customer.berdy.pro/people-face.tar.gz -o people-face.tar.gz
tar -xvf people-face.tar.gz && rm people-face.tar.gz
