_urls = {
	'dougTest2':'http://joe.schmoe.me',
}

def createUrl(provider, name, spec):
	name = ['name', key]
	# same JNDI name with url/ prefix added
	jndiName = ['jndiName', 'url/' + key]
	spec = ['spec', _urls[key]]
	urlAttrs = [name, jndiName, spec]
	print AdminConfig.create('URL', provider, urlAttrs)	

# default Cell, default URLProvider
defaultCellUrlProvider = AdminConfig.getid('/Cell:/URLProvider:/')

for key in _urls.keys():
	createUrl(defaultCellUrlProvider, key, _urls[key])

# Save changes
if (AdminConfig.hasChanges()):
    print "Saving changes"
    AdminConfig.save()