#!/usr/bin/env bash
# Prints the first 11 columns from 'ps aux'
ps aux | awk '{for(i=12; i<=NF; i++) $i=""; print $0}'
