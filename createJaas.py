# borrow useful functions from: 
# https://github.com/wsadminlib/wsadminlib
execfile('wsadminlib.py')

# list of aliases. edit as needed before running
# IDEA pull from external file. Not sure the advantage, though
# IDEA since prompting for password, might as well prompt for user too until, say, "end"?
# IDEA prompt for password twice to ensure it matches?
_aliases = [
    'alias1',
]

# read list of aliases and loop through, prompting for passwords
for alias in _aliases:
    password = raw_input("Password for " + alias + ": ")
    # don't set or change if empty
    if (password):
        print createJAAS(alias, alias, password)

# Save changes
if (AdminConfig.hasChanges()):
    print "Saving changes"
    AdminConfig.save()

