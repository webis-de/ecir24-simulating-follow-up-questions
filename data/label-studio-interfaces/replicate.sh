#!/bin/bash

max=31

cat question-assessment-head.txt > question-assessment.xml
for num in $(seq 0 $max);do
  cat question-assessment-unit.xml \
    | sed 's/{{NUM}}/'$num'/g'
done >> question-assessment.xml
cat question-assessment-foot.txt >> question-assessment.xml

