#!/bin/bash

#list='"algorithms" "assembly" "arch" "cp1" "cp2" "cp3" "cp4" "foundations" "os" "opl" "ai" "compiler" "cg2" "cg1" "cv"
#"cybercrime" "dc1" "dc2" "gui1" gui2" "ml" "mobileapp2" "mobilerobotics1" "mobilerobotics2" "nlp" "selected" "se1" "se2"
#"special"'

list='algorithms assembly arch cp1 cp2 cp3 cp4 foundations os opl ai compiler cg2 cg1 cv
cybercrime dc1 dc2 gui1 gui2 ml mobileapp2 mobilerobotics1 mobilerobotics2 nlp selected se1 se2
special'
for i in $list; do
   python scrapeterms.py "Fall 2000" "Spring 2017" $i "./results/cp1.txt"

done