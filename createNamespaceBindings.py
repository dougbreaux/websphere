# currently default Server scope, Strings only, uses JNDI name string/name
# TODO support Cell, Node scopes
# TODO support other types
# TODO support with/without JNDI name prefixes?

# add a new row/pair for each to add
_bindings = {
    'binding1':'value1',
}

# https://www.ibm.com/docs/en/was/9.0.5?topic=SSEQTP_9.0.5/com.ibm.websphere.nd.multiplatform.doc/ae/txml_namespacebinding.html
def createBinding(scope, key, value):

    name = ['name', key]

    # same JNDI name with string/ prefix added
    jndiName = ['nameInNameSpace', 'string/' + key]

    binding = ['stringToBind', value]
    print AdminConfig.create('StringNameSpaceBinding', scope, [name, jndiName, binding])

# default Cell, default Node, default Server
server = AdminConfig.getid('/Cell:/Node:/Server:/')

for key in _bindings.keys():
    createBinding(server, key, _bindings[key])

# Save changes
if (AdminConfig.hasChanges()):
    print "Saving changes"
    AdminConfig.save()