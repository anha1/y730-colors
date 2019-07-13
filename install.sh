#!/bin/sh
# TODO: this is a garbage, need to add a sane installer
set -e
sudo cp /home/user/projects/y730-colors/y730-colors.service /usr/lib/systemd/system/y730-colors.service
sudo systemctl enable y730-colors
sudo systemctl start y730-colors
sudo systemctl status y730-colors
