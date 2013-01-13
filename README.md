FormulaParser
=============

Simple logical formula parser written in Python

Parses logical formulas based on the following rules:

Variables starting with letter, then letters and/or numbers are formulas
If A is a formula, then ¬A is a formula
If A and B are formulas, then
 - (A&&B) is a formula
 - (A||B) is a formula
 - (A->B) is a formula
 - (A<->B) is a formula
 
Program has the ability to create truth tables.

Since this was a small one-day-project started because I was bored, it has not much comments, but the code should be pretty simple.
