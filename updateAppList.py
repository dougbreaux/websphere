# add a new row/pair for each app you want to update
_apps = {
	'appName':'filePath',
}

def updateApp(appName, filePath):
    AdminApp.update(appName, 'app', ['-operation', 'update', '-contents', filePath])

for key in _apps.keys():
	updateApp(key, _apps[key])

# Save changes
if (AdminConfig.hasChanges()):
    print "Saving changes"
    AdminConfig.save()	
    AdminNodeManagement.syncActiveNodes()