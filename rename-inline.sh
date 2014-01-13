#!/bin/bash

original="$1"
replacement="$2"

if [ ! -z `which gsed` ]; then
    REPLACE=`which gsed`
else
    REPLACE=`which sed`
fi;

echo "Replacing $original with $replacement"
egrep -r $original * | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"
egrep -r $original .*.yml | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"
egrep -r $original .bower* | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"
egrep -r $original .gitignore | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"

if [ -z $3 ]; then
original=`echo $original | tr '[:lower:]' '[:upper:]'`
replacement=`echo $replacement | tr '[:lower:]' '[:upper:]'`
echo "Replacing $original with $replacement"
egrep -r $original * | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"
egrep -r $original .*.yml | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"
egrep -r $original .bower* | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"
egrep -r $original .gitignore | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"

original=`echo $original | tr '[:upper:]' '[:lower:]'`
replacement=`echo $replacement | tr '[:upper:]' '[:lower:]'`
echo "Replacing $original with $replacement"
egrep -r $original * | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"
egrep -r $original .*.yml | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"
egrep -r $original .bower* | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"
egrep -r $original .gitignore | cut -d: -f1 | uniq | xargs $REPLACE -i "s,$original,$replacement,g"
fi;
