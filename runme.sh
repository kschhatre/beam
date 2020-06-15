#!/bin/bash

file="/home/ubuntu/calibration_stage1/beam/instanceconfpath.txt"

conf_file=$(cat "$file")

./gradlew :run -PappArgs="['--config', '$conf_file']"





