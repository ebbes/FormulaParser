#!/usr/bin/env python3

from Parser import Parser

if __name__ == "__main__":
    print("Logic parser, development version")
    print("Built-in commands:")
    print("    formula - print current formula")
    print("    vars    - print variables in formula")
    print("    table   - print truth table")
    print("    dnf     - generate equivalent formula in dnf from truth table")
    print("    exit    - exit")
    print()
    print("Initializing Parser...")
    parser = Parser()
    print("Done.")
    while True:
        inp = input(">>> ")
        
        try:
            if inp == "formula":
                print("Current formula:")
                print(str(parser.formula))
                continue
            if inp == "table":
                print("Truth table:")
                print(parser.truth_table())
                continue
            if inp == "dnf":
                print("Equivalent formula in DNF:")
                print("ψ =", parser.generate_dnf())
                continue
            if inp == "vars":
                print("Variables in current formula:")
                for var in parser.get_variables():
                    print(var)
                continue
            if inp == "exit":
                break
            if inp[0:6] == "parse ":
                inp = inp[6:]
            
            print()
            print("Formula parsed as:")
            print(parser.parse(inp))
            
        except Exception as ex:
            print("Error:", ex)
