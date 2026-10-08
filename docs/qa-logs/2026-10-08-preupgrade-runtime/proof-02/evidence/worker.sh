#!/bin/bash
exec 9>/var/run/cloud_sync.lock
flock -n 9 || exit 75
echo $$ > /storage/qa519/followup/worker.pid
exec sleep 120
