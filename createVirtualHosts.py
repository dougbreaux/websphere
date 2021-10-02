# borrow useful functions from: 
# https://github.com/wsadminlib/wsadminlib
execfile('wsadminlib.py')

_hosts = {
    'host1':'host-alias1',
}

for key in _hosts.keys():
    if not getVirtualHostByName(key):
        print createVirtualHost(key)
        ensureHostAlias(key, _hosts[key], 80)

# Save changes
if (AdminConfig.hasChanges()):
    print "Saving changes"
    AdminConfig.save()
