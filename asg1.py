rules = {}

def is_number(x):
    try:
        float(x)
        return True
    except:
        return False

def make_rule(tokens):
    if len(tokens) < 3 or not is_number(tokens[0]) or float(tokens[0]) < 0:
        raise ValueError()
    num = float(tokens[0])
    rhs = tokens[1]
    lhs = tokens[2:]
    x = rules.get(rhs, []);
    x.append((num, lhs))
    rules[rhs] = x

def read_file(file):
    f = open(file, 'r')
    for i, line in enumerate(f):
        # ignore comments
        line = line.partition('#')[0]

        tokens = line.split()

        # skip blank lines
        if len(tokens) == 0:
            continue

        # skip ill-formatted lines
        try:
            make_rule(tokens)
        except ValueError:
            print 'Invalid format on line ' + str(i) + '. Skipping line.'
            continue

read_file('grammar.txt')
for x, y in sorted(rules.iteritems()):
    for z in y:
        print x + ' -> ' + str(z[0]) + ' '  +  ' '.join(z[1])
