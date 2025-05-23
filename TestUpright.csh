#!/bin/csh

set upright = "upright"

head -24 main.tex >! ${upright}.tex
echo "\setboolean{uprightparticles}{true} % CHANGED" >> ${upright}.tex
tail -n +26 main.tex >> ${upright}.tex

pdflatex $upright && pdflatex $upright && bibtex $upright && pdflatex $upright

evince upright.pdf &
