import datetime
import socket

serverName = socket.gethostname()

# processList is a generic processing function for any type of list
def processList(objects, getAttributesFunc, parentPath, objectType):
    parentId = AdminConfig.getid(parentPath)
    for key in objects.keys():
        attributes = getAttributesFunc(key, objects[key])
        objectPath = parentPath + objectType + ':' + key + '/' 
        objectId = AdminConfig.getid(objectPath )
        if objectId:
            print "Modifying: " + objectPath
            AdminConfig.modify(objectId, attributes)
        else:
            print "Creating:  " + objectPath
            AdminConfig.create(objectType, parentId, attributes)

def processObject(name, attributes, parentPath, objectType):
    objectPath = parentPath + objectType + ':' + name + '/'
    objectId = AdminConfig.getid( objectPath )
    if objectId:
        print 'Modifying: ' + objectPath
        AdminConfig.modify(objectId, attributes)
    elif name:
        print 'Creating:  ' + objectPath
        parentId = AdminConfig.getid(parentPath)
        AdminConfig.create(objectType, parentId, attributes)
    else:
        print 'Not found: ' + objectPath
       
	
# retrieve cert
def retrieveSignerCert(host, port, baseAlias):
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    alias = baseAlias + '-' + ts
    args = '[-host ' + host + ' -port ' + port + ' -keyStoreName NodeDefaultTrustStore -certificateAlias ' + alias + ' ]'
    try:
        AdminTask.retrieveSignerFromPort(args);
        print alias + ': retrieved'
    except:
        print alias + ': not retrieved'

# Namespace bindings functions
# https://www.ibm.com/docs/en/was/9.0.5?topic=SSEQTP_9.0.5/com.ibm.websphere.nd.multiplatform.doc/ae/txml_namespacebinding.html

def getBindingAttibutesBase(key, value, prefix):
    return [['name', key], ['nameInNameSpace', prefix + key], ['stringToBind', value]]
    
def getBindingAttibutesString(key, value):
    return getBindingAttibutesBase(key, value, 'string/')
    
def getBindingAttibutesNoPrefix(key, value):
    return getBindingAttibutesBase(key, value, '')

def processBindingsList(bindings):
    processList(bindings, getBindingAttibutesString, '/Cell:/Node:/Server:/', 'StringNameSpaceBinding')
	
def processBindingsListNoPrefix(bindings):
    processList(bindings, getBindingAttibutesNoPrefix, '/Cell:/Node:/Server:/', 'StringNameSpaceBinding')
	
# URL functions
def getURLAttributes(key, value):
    return [['name', key], ['jndiName', 'url/' + key], ['spec', value], ['description', value]]
    
def processUrlList(_urls):
    processList(_urls, getURLAttributes, '/Cell:/URLProvider:/', 'URL')

	
# MQ functions
def createConnectionFactory(name, attibutes):
	processObject(name, attibutes, '/Cell:/JMSProvider:/', 'MQConnectionFactory')
	
def createQueue(name, queueName):
    queueAttributes = [
        ['name', name], 
        ['jndiName', name], 
        ['baseQueueName', queueName], 
        ['description', queueName]
    ]
    processObject(name, queueAttributes, '/Cell:/JMSProvider:/', 'MQQueue')