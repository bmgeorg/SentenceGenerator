import sys
import random

# Should be constructed with CfgBuilder
class Cfg:
    # public interface
    def sentence(self):
        return self.reduce('ROOT')

    # private interface
    class Rule:
        weight = 0.0
        rhs = []
        def __init__(self, weight, rhs):
            self.weight = weight
            self.rhs = rhs

    # maps lhs -> [Rule]
    rules = {}
    
    def reduce(self, lhs):
        if not self.is_nonterminal(lhs):
            return lhs + ' '

        lhs_rules = self.rules.get(lhs)
        # pick random rule
        i = random.randint(0, len(lhs_rules)-1)

        rhs = lhs_rules[i].rhs

        result = ''
        for x in rhs:
            result += self.reduce(x)

        return result     

    def print_out(self):
        for lhs, x in sorted(self.rules.iteritems()):
            for rhs in x:
                print lhs + ' -> ' + str(rhs[0]) + ' '  +  ' '.join(rhs[1])

    def is_nonterminal(self, lhs):
        return self.rules.get(lhs) is not None

class CfgBuilder:
    # maps lhs -> [Rule]
    rules = {}

    def add_rule(self, lhs, rhs, weight):
        lhs_rules = self.rules.get(lhs, [])
        lhs_rules.append(Cfg.Rule(weight, rhs))
        self.rules[lhs] = lhs_rules

    def build(self):
        cfg = Cfg()
        cfg.rules = self.rules
        if not cfg.is_nonterminal('ROOT'):
            raise ValueError('No ROOT nonterminal')

        self.rules = {}
        return cfg

def is_number(x):
    try:
        float(x)
        return True
    except:
        return False

def read_grammar(file):
    builder = CfgBuilder()
    f = open(file, 'r')
    for i, line in enumerate(f):
        # ignore comments
        line = line.partition('#')[0]

        tokens = line.split()

        # skip blank lines
        if len(tokens) == 0:
            continue

        # skip ill-formatted lines
        if len(tokens) < 3 or not is_number(tokens[0]) or float(tokens[0]) <= 0:
            print 'Invalid format on line ' + str(i) + '. Skipping line.'
            continue
        
        builder.add_rule(tokens[1], tokens[2:], tokens[0])

    return builder.build()

cfg = read_grammar(sys.argv[1])
n = 1
if len(sys.argv) >= 3:
    n = int(sys.argv[2])
for i in range(0, n):
    print cfg.sentence()
