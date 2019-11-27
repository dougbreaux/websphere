# Usage: wsadmin -f addSessionProperty.py server property value [description]
server = sys.argv[0]
property = sys.argv[1]
value = sys.argv[2]
if (len(sys.argv) == 4):
    descr = sys.argv[3]
else :
	descr = None

# Convert a list of items separated by linefeeds into an array
def getListArray(l):
    return l.splitlines()

# Obtain the "simple" server name
def getServerName(s):
    return AdminConfig.showAttribute(s, 'name')

# Add common attr list to specified Server's SessionManager
def addSessionManagerPropertiesToServer(s):
    sm = AdminConfig.list('SessionManager', s)

    # Look for existing property so we can replace it (by removing it first)
    currentProps = getListArray(AdminConfig.list("Property", sm))
    for prop in currentProps:
        if property == AdminConfig.showAttribute(prop, "name"):
            print "Removing existing property from Server %s" % getServerName(s)
            AdminConfig.remove(prop)

    # Store new property in 'properties' object
    print "Adding property to Server %s" % getServerName(s)
    AdminConfig.modify(sm,[['properties',attr]])

# Construct list with new property name and value
attr = []

if (descr is None):
    print "Adding property %s=%s" % (property,value)
    attr.append([['name',property],['value',value]])
else:
    print "Adding property %s=%s,%s" % (property,value,descr)
    attr.append([['name',property],['value',value],['description',descr]])

# Locate all Application Servers if server is 'all'
if (server == 'all'):
    servers = AdminConfig.list('Server')
    for aServer in getListArray(servers):
        type = AdminConfig.showAttribute(aServer,'serverType')
        if (type == 'APPLICATION_SERVER'):
            addSessionManagerPropertiesToServer(aServer)

# TODO: support comma-separated list of servers

else:
    # Locate specified Server and its JVM
    server = AdminConfig.getid('/Server:'+server+'/')
    addSessionManagerPropertiesToServer(server)

# Save changes
if (AdminConfig.hasChanges()):
    AdminConfig.save()
