# borrow useful functions from: 
# https://github.com/wsadminlib/wsadminlib
execfile('wsadminlib.py')

_nodeName = "myNode"
_serverName = "myServer"

_jvmProperties = [
    ['initialHeapSize', 128],
    ['maximumHeapSize', 512]
]

_properties = {
    'myProperty1':'myValue1',
}

_environmentEntries = {
    'TZ':'UTC'
}

# create server
print createServer(_nodeName, _serverName)

# TODO initial/max heap. These steps must not have worked
#jvm = AdminControl.completeObjectName('WebSphere:type=JVM,process=' + _serverName + ',*')
#AdminControl.setAttributes(jvm, _jvmProperties)

# custom properties
for prop in _properties.keys():
    print createJvmProperty(_nodeName, _serverName, prop, _properties[prop])
    
# environment
for env in _environmentEntries.keys():
    print createJvmEnvEntry(_nodeName, _serverName, env, _environmentEntries[env])

# process execution
setJvmExecutionUserGroup(_nodeName, _serverName, 'wasusr', 'wasgrp')

# TODO umask

# Save changes
if (AdminConfig.hasChanges()):
    print "Saving changes"
    AdminConfig.save()
