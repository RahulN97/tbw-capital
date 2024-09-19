#!/bin/bash

echo "Starting redis server"

redis-server redis.conf --dir ${HOME}/tbw-capital/store
