#!/bin/bash
setsid /storage/qa519/followup/worker.sh >/storage/qa519/followup/worker.log 2>&1 &
while :; do sleep 1; done
