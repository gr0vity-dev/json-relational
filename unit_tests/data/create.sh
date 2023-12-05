#!/bin/bash

# Loop from 1 to 10
for i in {1..10}
do
    # Create {i}_data.txt
    touch "${i}_data.txt"

    # Create {i}_data.json
    echo "{}" > "${i}_data.json"  # Creates an empty JSON object in the file

    # Create {i}_expected.json
    echo "{}" > "${i}_expected.json"  # Creates an empty JSON object in the file
done
