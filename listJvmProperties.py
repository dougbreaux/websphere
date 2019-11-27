# Usage: wsadmin -f listJvmProperties.py server
server = sys.argv[0]

# Convert a list of items separated by linefeeds into an array
def getListArray(l):
    return l.splitlines()

# Obtain the "simple" server name
def getServerName(s):
    return AdminConfig.showAttribute(s, 'name')

# Add common attr list to specified Server's JVM
def listPropertiesForServer(s):
    jvm = AdminConfig.list('JavaVirtualMachine', s)

    currentProps = getListArray(AdminConfig.list("Property", jvm))
    for prop in currentProps:
		propName = AdminConfig.showAttribute(prop, "name")
		propValue = AdminConfig.showAttribute(prop, "value")
		print "%s=%s" % (propName, propValue)

# Locate specified Server and its JVM
server = AdminConfig.getid('/Server:'+server+'/')
listPropertiesForServer(server)