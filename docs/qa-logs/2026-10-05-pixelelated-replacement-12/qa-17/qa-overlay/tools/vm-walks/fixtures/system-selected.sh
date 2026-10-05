#!/bin/sh
# QA guest observation only; installed by vm-qa before a manager walk.
printf '%s\n' "$1" > /storage/.cache/vm-qa-selected-system
