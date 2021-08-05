# pass in MAX env on command-line
env = sys.argv[0]
#env = 'QA'
print "Setting max.environment to " + env

# all apps
apps = AdminApp.list()
for app in apps.splitlines():

    # resource environment refs for current app, each formatted like:
    # Module:  Vehicle Registration Renewal
    # Bean:
    # URI:  VehicleRegistration.war,WEB-INF/web.xml
    # Resource Reference:  max.environment
    # Resource type:  java.lang.String
    # Target Resource JNDI Name:  max.environment.UAT
 
    #print AdminApp.view(app, '[ -MapResEnvRefToRes ]')
    refs = AdminApp.view(app, '[ -MapResEnvRefToRes ]')
    for ref in refs.splitlines():

        # get Module name
        if ref.find("Module:  ") != -1:
            module = ref[9:]
        
        elif ref.find("URI:  ") != -1:
            uri = ref[6:]

        elif ref.find("Resource Reference:  max.environment") != -1:
            #print app
            #print ref
            envString = '[ -MapResEnvRefToRes [[ "' + module + '" "" ' + uri + ' max.environment java.lang.String max.environment.' + env + ' ]]]'
            #print envString
            AdminApp.edit(app, envString)

# Save changes
if (AdminConfig.hasChanges()):
    print "Saving changes"
    AdminConfig.save()
