#!/bin/bash

file="/home/ubuntu/kiran_thesis/beam/instanceconfpath.txt"

conf_file=$(cat "$file")

./gradlew :run -PappArgs="['--config', '$conf_file']"





