#!/usr/bin/env bash
vmstat | awk 'NR > 1'
