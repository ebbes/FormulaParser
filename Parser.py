from collections import OrderedDict
from copy import copy
from Formula import Conjunction, Disjunction, Implication, Biimplication, \
                      Negation, Variable, Static, Formula
from Token import Token

class Parser:
    __digits    = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    __lowercase = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", \
                 "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    __uppercase = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", \
                 "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    __letters   = __lowercase + __uppercase

    __tokens = {'CONJUNCT':       '∧',
                'DISJUNCT':       '∨',
                'IMPLY':          '→',
                'BIIMPLY':        '↔',
                'NEGATE':         '¬',
                'FALSE':          '0',
                'TRUE':           '1',
                'PAREN_OPEN':     '(',
                'PAREN_CLOSE':    ')',
             }
    
    __current_token = None
    __formula_input = ""
    formula = None
    variables = OrderedDict()
    fulfilling = None
    dnf = ""
    
    def __get_compound_lexeme(self, inp, chars):
        """ Returns a lexeme compounded of chars in list or '' if no match found """
        
        if not inp[0:1] in chars:
            return ''
        else:
            return inp[0:1] + self.__get_compound_lexeme(inp[1:], chars)
    
    def __consume(self):
        """ Stores next token in __current_token """
        
        if self.__formula_input == '':
            self.__current_token = Token('END', '')
            return
        
        if self.__formula_input[0] == ' ':
            #skip whitespace
            self.__formula_input = self.__formula_input[1:]
            self.__consume()
            return
        
        for token_name in self.__tokens:
            token_character = self.__tokens[token_name]
            
            if self.__formula_input[0] == token_character:
                self.__current_token = Token(token_name, token_character)
                self.__formula_input = self.__formula_input[1:]
                return
            
        if self.__formula_input[0] in self.__letters:
            lexeme = self.__get_compound_lexeme(self.__formula_input, self.__letters + self.__digits)
            self.__formula_input = self.__formula_input[len(lexeme):]
            self.__current_token = Token("VARIABLE", lexeme)
            return
        
        self.__current_token = Token("UNKNOWN", self.__formula_input)
        self.__formula_input = ""

    def __expect_token(self, ttype):
        if self.__current_token.ttype == ttype:
            self.__consume()
        else:
            error = "Expected token of type '{}', but found '{}' with type '{}'." \
                .format(ttype, self.__current_token.tvalue, ttype)
            raise SyntaxError(error)

    def parse(self, alstring):
        """ Parses a formula """
        
        #replace ASCII representations by actual symbols
        alstring = alstring.replace("~",   "¬")
        alstring = alstring.replace("!",   "¬")
        alstring = alstring.replace("/\\", "∧")
        alstring = alstring.replace("&&",  "∧")
        alstring = alstring.replace("\\/", "∨")
        alstring = alstring.replace("||",  "∨")
        alstring = alstring.replace("<->", "↔")
        alstring = alstring.replace("->",  "→")
        
        self.__formula_input = alstring
        
        #fill __current_token with initial value
        self.__consume()
        
        self.variables = OrderedDict()
        self.dnf = ""
        self.fulfilling = []
        
        self.formula = self.__parse_formula()
        
        if self.__current_token.ttype != "END":
            raise SyntaxError("Expected END, but found " + self.__current_token.ttype)
        
        return str(self.formula)
    
    def __parse_formula(self):
        if self.__current_token.ttype == "NEGATE":
            self.__consume()
            return Negation(self.__parse_formula())
        
        if self.__current_token.ttype == "PAREN_OPEN":
            #__consume PAREN_OPEN
            self.__consume()
            left_formula = self.__parse_formula()
            
            junctor = self.__current_token.ttype
            self.__consume()
            
            right_formula = self.__parse_formula()
            
            self.__expect_token("PAREN_CLOSE")
            
            if junctor == "CONJUNCT":
                return Conjunction(left_formula, right_formula)
            if junctor == "DISJUNCT":
                return Disjunction(left_formula, right_formula)
            if junctor == "IMPLY":
                return Implication(left_formula, right_formula)
            if junctor == "BIIMPLY":
                return Biimplication(left_formula, right_formula)
            
            error = "Invalid junctor: {}".format(junctor)
            raise SyntaxError(error)
        
        if self.__current_token.ttype == "FALSE":
            self.__consume()
            return Static("0")
        
        if self.__current_token.ttype == "TRUE":
            self.__consume()
            return Static("1")
        
        if self.__current_token.ttype == "VARIABLE":
            variable = self.__current_token.tvalue
            self.__consume()
            self.variables[variable] = "0"
            return Variable(variable)
        
        if self.__current_token.ttype == "END":
            return
        
        error = "Invalid token: {} with type {}"\
            .format(self.__current_token.tvalue, self.__current_token.ttype)
        raise SyntaxError(error)
    
    def get_variables(self):
        if not isinstance(self.formula, Formula):
            raise ValueError("No (valid) formula parsed yet!")
        
        return list(self.variables)
    
    def evaluate(self):
        if not isinstance(self.formula, Formula):
            raise ValueError("No (valid) formula parsed yet!")
        
        return self.formula.evaluate(self.variables)
    
    def truth_table(self):
        if not isinstance(self.formula, Formula):
            raise ValueError("No (valid) formula parsed yet!")
        
        table = ""
        
        if len(self.variables) == 0:
            value = "0"
            if self.formula.evaluate(self.variables):
                value = "1"
            
            table = "Current formula is equivalent to {}.\n".format(value)
            return table
        
        self.fulfilling = []

        #get number to variable name mapping using list
        variables = list(self.variables)
        numvars = len(variables)
        header1 = ""
        header2 = ""
        row = ""
        for variable in variables:
            header1 += " {} |".format(variable)
            header2 += (len(variable) + 2) * "–" + "┼"
            row += " {}" + len(variable) * " " + "|"
        
        header1 += " φ \n"
        header2 += "–––\n"
        row += " {}\n"

        table += header1
        table += header2
        
        for i in range(0, 2 ** numvars):
            binary = bin(i)[2:]
            binary = "0" * (numvars - len(binary)) + binary
            for j in range(0, len(binary)):
                self.variables[variables[j]] = binary[j]
            
            value = "0"
            if self.formula.evaluate(self.variables):
                value = "1"
                self.fulfilling.append(copy(self.variables))
            table += row.format(*(list(self.variables.values()) + [value]))
        
        return table
    
    def generate_dnf(self):
        if not isinstance(self.fulfilling, list):
            raise ValueError("Truth table has to be generated first!")
        
        if len(self.variables) == 0:
            value = "0"
            if self.formula.evaluate(self.variables):
                value = "1"
            
            self.dnf = value
            return value
        
        dnf = ""
        
        for fulfilling in self.fulfilling:
            first_conjunctive = len(dnf) == 0
            
            if not first_conjunctive:
                dnf = "({}∨".format(dnf)
            
            conjunctive = ""
            for value in fulfilling:
                first_var = len(conjunctive) == 0
                
                if not first_var:
                    conjunctive = "({}∧".format(conjunctive)
                
                if fulfilling[value] != "1":
                    conjunctive += "¬"
                conjunctive += value
                
                if not first_var:
                    conjunctive += ")"
            
            dnf += conjunctive
            
            if not first_conjunctive:
                dnf += ")"
        
        self.dnf = dnf
        return dnf
