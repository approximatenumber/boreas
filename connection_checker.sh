#!/bin/bash

declare -a SERVERS
SERVERS=("8.8.8.8" "8.8.4.4", "1.1.1.1")
TIMEOUT=120
IFACE=ppp0

function logger {
    echo "$(date +"%H:%M:%S") $1"
}

while true; do
    SUCCESS=true
    for server in "${SERVERS[@]}"; do
	logger "Checking connection to $server..."
        ping -c10 -q -I $IFACE "$server" 2>&1 >/dev/null;
        if [ $? -ne 0 ]; then
	    logger "Server $server not available"
	    SUCCESS=false
	else
	    SUCCESS=true
	    break
	fi
    done
    if $SUCCESS; then
	logger "Network is okay"
    else
	logger "Network is down, restarting modem"
	wb-gsm restart_if_broken
	logger "Network restarted"
    fi
    logger "Sleeping ${TIMEOUT}s"
    sleep $TIMEOUT
done
