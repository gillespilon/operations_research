#! /usr/bin/env python3

import pprint


pp = pprint.PrettyPrinter(indent=2, depth=2, sort_dicts=False)
stuff1 = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
pp.pprint(stuff1)
stuff2 = ['mo', 'larry', 'curly', 'shemp', 'curly joe']
pp.pprint(stuff2)
