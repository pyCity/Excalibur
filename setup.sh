#!/usr/bin/env bash

# If not run as root, rerun as root
if [ $(id -u) -ne 0 ]; then
    echo "Must run as root"
    sudo $0 && exit 1
fi

# Loop until requirements.txt and pip3 exist
while ! [ -e "requirements.txt" ] && [ -x "$(command -v pip3)" ]; do

    # Check for requirements.txt
    if ! [ -e "requirements.txt" ]; then
        echo "File not found. Creating requirements.txt"
        echo -e "pycryptodome==3.7.3\ntqdm==4.31.1\n" > requirements.txt
    fi

    # Check for pip3
    if ! [ -x "$(command -v pip3)" ]; then
        echo "Pip3 not detected. Installing pip3"
        apt-get update -y && apt-get -y install python3 python3-pip
    fi
done

echo "Found requirements.txt & pip3. Installing dependencies" && pip3 install -r requirements.txt