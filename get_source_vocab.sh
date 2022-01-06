#! /bin/bash

mkdir -p sourcedata/

LANGUAGE="ger"
LEVELS="1 2 3 4 5 6"

for level in ${LEVELS}
do
    wget "https://wohok.com/mandarin/hsk_test/hsk${level}/${LANGUAGE}/vocabulary.html" -O "sourcedata/hsk_${level}_${LANGUAGE}.txt"
done

echo "FINISHED"
