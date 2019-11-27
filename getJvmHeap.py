# Usage: wsadmin -f getJvmHeap.py server 
server = AdminConfig.getid('/Server:'+sys.argv[0]+'/')
jvm = AdminConfig.list('JavaVirtualMachine', server)

print 'initialHeapSize: ' + AdminConfig.showAttribute(jvm, 'initialHeapSize')
print 'maximumHeapSize: ' + AdminConfig.showAttribute(jvm, 'maximumHeapSize')
