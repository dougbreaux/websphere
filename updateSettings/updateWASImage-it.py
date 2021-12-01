###########################################################################################
# "import" custom functions using "execfile".  
# using actual "import" command makes the wsadmin functions unavailable to the imported file
###########################################################################################
execfile('baseFunctions.py')

###########################################################################################
# Server settings
###########################################################################################

#
# serverName JVM custom property
#
name = 'serverName'
objectType = 'Property'
path = '/Cell:/Node:/Server:/JavaProcessDef:/JavaVirtualMachine:/'
attributes = [  ['name', 'serverName'], 
                ['value', serverName] ] # serverName defined in baseFunctions.py
processObject(name, attributes, path, objectType)

# # JVM heap size limits
# name = '' #default
# objectType = 'JavaVirtualMachine'
# path = '/Cell:/Node:/Server:/JavaProcessDef:/'
# attributes = [  ['initialHeapSize', '512'], 
                # ['maximumHeapSize', '2048'] ]
# processObject(name, attributes, path, objectType)

# # HttpSessionIdReuse = true
# name = 'HttpSessionIdReuse'
# objectType = 'Property'
# path = '/Cell:/Node:/Server:/ApplicationServer:/WebContainer:/SessionManager:/'
# attributes = [ ['value', 'true'] ]
# processObject(name, attributes, path, objectType)

# # CookieSameSite = None
# name = 'CookieSameSite'
# objectType = 'Property'
# path = '/Cell:/Node:/Server:/ApplicationServer:/WebContainer:/SessionManager:/'
# attributes = [ ['value', 'None'] ]
# processObject(name, attributes, path, objectType)

# # Cookie settings (secure=true and httpOnly=true)
# name = '' #default
# objectType = 'Cookie'
# path = '/Cell:/Node:/Server:/ApplicationServer:/WebContainer:/SessionManager:/'
# attributes = [ ['secure', 'true'], 
               # ['httpOnly', 'true'] ]
# processObject(name, attributes, path, objectType)

###########################################################################################
# hosts/base URLs
###########################################################################################

web_url = 'https://wsi2it.dmv.ca.gov'
gateway_url = 'http://wsi2esbiz01i.dmv.ca.gov:7800/DMVGateway/'
static_content_url = 'http://wsi2imagez01i.dmv.ca.gov:8080'
edl_url = 'https://slingshot.edl-test.dmv.ca.gov'
design_url = 'https://cdn.uat.dmv.ca.gov/dmv-design-system/it/'
converge_url = 'https://demo.convergepay.com/hosted-payments/'

hostname = serverName + '.dmv.ca.gov' # serverName defined in baseFunctions.py
_urls = {
    'convergePaymentPageUrl':converge_url,
    'convergeTokenUrl':converge_url + 'transaction_token',
    'edlAmazonLocation':edl_url,
    'portalContentLocation':static_content_url + '/dmv_branding/',
    'scLoginUrl':'http://' + hostname + ':9080',
    'ShoppingCartServiceLocation':gateway_url + 'ShoppingCartServicePortType',
    'siteDesignSystem':design_url,
    'siteHostNameSSL':web_url,
}
processUrlList(_urls )

###########################################################################################
# custom namespace bindings
###########################################################################################

_bindingsString = {
    'convergeCcGetTokenPin':'6BTBRJYZE4PZ9382PYCE80NPGLWLXAUSBAGFJOT3VDA53T5Z0BFSFAJNXPXOTSRQ',
    #'convergeProcessXmlTimeout':'60',
    #'sslMerchantId':'001514',
    #'sslUserId':'CAAPI',
}
_bindingsNoPrefix = {
    'EGOV_ENV':'integration',
}
processBindingsList(_bindingsString)
processBindingsListNoPrefix(_bindingsNoPrefix)

###########################################################################################
# MQ settings - edit as needed
###########################################################################################

host = '134.187.202.234'
port = '1414'
channel = 'SCART.INT.CLIENT'
queueManager = 'IIBINT01'

connectionFactoryName = 'iibMqConnectionFactory'
connectionFactoryAttributes = [
        ['name', connectionFactoryName], 
        ['jndiName', 'QueueConnectionFactory'], 
        ['XAEnabled', 'true'], 
        ['host', host], 
        ['port', port], 
        ['transportType', 'CLIENT'], 
        ['channel', channel], 
        ['queueManager', queueManager]
    ]
    
# create connection factory
createConnectionFactory(connectionFactoryName, connectionFactoryAttributes)

# # create queue (should already be in an image)
# createQueue('AuditLoggingQ', 'AUDIT.A.LOG.OUT')
# createQueue('JournalingQ.LogApplication', 'JOURNAL.A.APP.OUT')
# createQueue('JournalingQ.LogTransaction', 'JOURNAL.A.TRANS.OUT')
# createQueue('JournalingQ.LogUserEvents', 'JOURNAL.A.EVENT.OUT')

###########################################################################################
# update Certs in Trust store
###########################################################################################

retrieveSignerCert('demo.convergepay.com', '443', 'convergepay')
retrieveSignerCert('slingshot.edl-test.dmv.ca.gov', '443', 'slingshot')

# IIB certs required for UAT and Prod which use https to connect to IIB
# tries twice since two certs are used in cluster, 
# but twice may not be enough since certs are received randomly

#retrieveSignerCert('134.187.202.209', '7700', 'uatiib')
#retrieveSignerCert('134.187.202.209', '7700', 'uatiib2')

###########################################################################################
# Save changes
###########################################################################################

if AdminConfig.hasChanges():
    print 'Saving changes'
    AdminConfig.save()
