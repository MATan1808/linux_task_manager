#!/bin/bash
export DISPLAY="${DISPLAY:-:0}"
export XAUTHORITY="${XAUTHORITY:-$HOME/.Xauthority}"
exec /usr/bin/python3 /media/tanma/DATA/terminal/task_manager_gui.py
