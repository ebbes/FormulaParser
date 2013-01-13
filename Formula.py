class Formula:
    formula1 = None
    formula2 = None
    
    def __init__(self):
        raise NotImplementedError
    
    def __repr__(self):
        return str(self.formula1)
    
    def evaluate(self, variables):
        raise NotImplementedError

class Conjunction(Formula):
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2
    
    def __repr__(self):
        return "({}∧{})".format(str(self.formula1), str(self.formula2))
    
    def evaluate(self, variables):
        return self.formula1.evaluate(variables) and self.formula2.evaluate(variables)

class Disjunction(Conjunction):
    def __repr__(self):
        return "({}∨{})".format(str(self.formula1), str(self.formula2))

    def evaluate(self, variables):
        return self.formula1.evaluate(variables) or self.formula2.evaluate(variables)

class Implication(Conjunction):
    def __repr__(self):
        return "({}→{})".format(str(self.formula1), str(self.formula2))
        
    def evaluate(self, variables):
        return not self.formula1.evaluate(variables) or self.formula2.evaluate(variables)

class Biimplication(Conjunction):
    def __repr__(self):
        return "({}↔{})".format(str(self.formula1), str(self.formula2))

    def evaluate(self, variables):
        return self.formula1.evaluate(variables) == self.formula2.evaluate(variables)

class Negation(Formula):
    def __init__(self, formula):
        self.formula1 = formula
    
    def __repr__(self):
        return "¬{}".format(str(self.formula1))
        
    def evaluate(self, variables):
        return not self.formula1.evaluate(variables)

class Variable(Formula):
    def __init__(self, variable):
        self.formula1 = variable
    
    def evaluate(self, variables):
        return variables[self.formula1] == "1"

class Static(Formula):
    def __init__(self, value):
        self.formula1 = value
    
    def evaluate(self, variables):
        return self.formula1 == "1"
