#!/bin/bash
set -e

source env/bin/activate

#set env variables here (requirements.txt?)

#restore SHELL env for cron
SHELL=/bin/bash
exec /bin/bash --norc '$@'