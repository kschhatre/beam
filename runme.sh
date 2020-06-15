#!/bin/bash

file="/home/ubuntu/beam/instanceconfpath.txt"

conf_file=$(cat "$file")

./gradlew :run -PappArgs="['--config', '$conf_file']"





