#!/usr/bin/env bash

dir="$(pwd)/api-playground"

# Loop through day1*, day2*, day3* only
for day_dir in "$dir"/day{1..3}*; do
    # Check if it's actually a directory
    if [ -d "$day_dir" ]; then
        echo "Found directory: $day_dir"

        # Check if Dockerfile exists, create if missing
        if [ ! -f "$day_dir/Dockerfile" ]; then
            echo "Creating Dockerfile in $day_dir"
            echo "FROM python:3.11" > "$day_dir/Dockerfile"
        else
            echo "Dockerfile already exists in $day_dir, skipping."
        fi
    fi
done
