#!/usr/bin/env bash

PROGRAM_NAME=$1

chmod +x ./*/*/main.py

echo "Syncing files..."

/usr/bin/expect <<EOD
log_user 0
set timeout -1
spawn ssh robot@ev3dev.local "rm -rf programs"
expect "Password: "
send "maker\r"
expect eof

spawn scp -r ./programs robot@ev3dev.local:./programs
expect "Password: "
send "maker\r"
expect eof
EOD

echo "Done syncing files."
echo "Starting program '${PROGRAM_NAME}'."

/usr/bin/expect <<EOD
log_user 0
set timeout -1
spawn ssh robot@ev3dev.local "./programs/${PROGRAM_NAME}/main.py"
expect "Password: "
log_user 1
send "maker\r"
expect eof
EOD

echo ""
echo ""
echo "PROGRAM DONE"
