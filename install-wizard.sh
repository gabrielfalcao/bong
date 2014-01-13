#!/bin/bash

if [ -z $VIRTUAL_ENV ]; then
    echo "Please run this script inside of a virtual env with the future name of your application"
    exit 1
fi;

printf "Welcome to \033[1;32mBong\033[0m, \n"
printf "the best kinda Flask you could "
printf "\033[1;37mever\033[0m expect."

echo
printf "\033[33mFirst of all, type in the name of the \n"
printf "application you want to create:\033[0m\n"
read ApplicationName

echo "Alright, so I'm gonna customize the application modules "
printf "replacing \033[1;32mBong\033[0m with \033[1;33m$ApplicationName\033[0m\n"
echo
echo "Looks good?"
yesno=""

while [ "$yesno" != "y" ]; do
    echo "[y/n]?"
    read yesno

    if [ $yesno == "n" ]; then
        exit 1
    fi;
done

easy_install curdling
curd install -r development.txt

./rename-inline.sh Bong $ApplicationName
mv bong `printf $ApplicationName | tr '[:upper:]' '[:lower:]'`
git add `printf $ApplicationName | tr '[:upper:]' '[:lower:]'`

rm -f screenshot.png
rm -f install-wizard.sh
rm -f rename-inline.sh
rm -rf .git
git init
git add .
git commit -am "Creating $ApplicationName with Bong <http://github.com/weedlabs/bong>"


printf "Cool, now try running \033[1;32mmake unit\033[0m or "
printf "\033[1;32mmake functional\033[0m\n"
