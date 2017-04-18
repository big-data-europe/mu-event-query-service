#!/bin/bash

docker run --rm -it \
           -v "$PWD"/src:/app \
           -p 1234:80 \
           --link etmsplatform_db_1:database \
           --network etmsplatform_default \
           --name mu-docker-event-query \
           -e MODE=development \
           mu-docker-event-query

