#!/bin/sh
SPATH="/etc/slackcurrent"

if [ ! -e $SPATH/blacklist ]
then
	mv $SPATH/blacklist.new $SPATH/blacklist 
fi

if [ ! -e $SPATH/mirrors ]
then
	mv $SPATH/mirrors.new $SPATH/mirrors
fi
