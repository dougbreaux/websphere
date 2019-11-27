#-------------------------------------------------------------------------------
# Name: updateApp
# Role: Trivial wsadmin script that can be used to update an existing
#       WebSphere Application Server application
#-------------------------------------------------------------------------------
'''
Command: %(cmdName)s\n
Purpose: Trivial wsadmin script that can be used to update an existing WebSphere
         Application Server application\n
Authors: Doug Breaux
         Robert A. (Bob) Gibson\n
  Usage: wsadmin -f %(cmdName)s.py appName filePath [nosync]\n
  Where: appName  = The name of an existing Enterprise Application.
         filePath = The fully qualified path to the application EAR file.
         nosync   = Optional parameter to indicate that synchronization should
                    not take place after the update.\n
Example: ./wsadmin.sh -f %(cmdName)s.py Test /temp/Test.ear nosync
'''

import os, sys

#-------------------------------------------------------------------------------
# Name: fixFileName()
# Role: Unfortunately, an ugly "wart" exists when dealing with Windows
#       fileNames.  Specifically, some Windows fileNames, when passed into a
#       wsadmin script can inadvertently cause "correct" filename characters to
#       be misinterpreted as special Jython "escape" characters.  This occurs
#       when the filename, or directory name character that occur immediately
#       after a directory delimiter (i.e., '\\') happen to be one of the
#       "special" Jython escape characters.  Instead of correctly identifying
#       the directory delimiter as '\\', and leaving the subsequent character
#       alone, the directory delimiter and the character that follows are
#       interpreted as one of these "special" Jython escape character.  So, the
#       purpose of this routine is to correct that interpretation error.
# Note: This routine is equivalent to:
#       def fixFileName( fileName ) :
#         result = fileName.replace( '\a', r'\a' )
#         result = result.replace( '\b', r'\b' )
#         result = result.replace( '\f', r'\f' )
#         result = result.replace( '\n', r'\n' )
#         result = result.replace( '\r', r'\r' )
#         result = result.replace( '\t', r'\t' )
#         result = result.replace( '\v', r'\v' )
#         return result
#-------------------------------------------------------------------------------
def fixFileName( fileName ) :
    'fixFileName( filename ) - Return the specified string with selected escape characters unescaped.'
    return fileName.replace(
      '\a', r'\a' ).replace(
      '\b', r'\b' ).replace(
      '\f', r'\f' ).replace(
      '\n', r'\n' ).replace(
      '\r', r'\r' ).replace(
      '\t', r'\t' ).replace(
      '\v', r'\v' )

#-------------------------------------------------------------------------------
# Name: process
# Role: Perform the requested operation - i.e., updating of the application EAR
#-------------------------------------------------------------------------------
def process( appName, filePath, nosync = None ) :
    # Verify optional "nosync" parameter value, if one was provided
    if nosync and nosync != 'nosync' :
        print '\n  Error: Unrecognized parameter:', nosync
        Usage()

    # Verify application name
    apps = AdminApp.list().splitlines()
    if appName not in apps :
        print '\n  Error: Unrecognized application name: %s\n' % appName
        print 'Installed Applications:\n ', '\n  '.join( apps )
        sys.exit()

    # Verify that the filePath is valid
    if os.path.exists( filePath ) :
        if os.path.isfile( filePath ) :
            try :
                AdminApp.update( appName, 'app', [ '-operation', 'update', '-contents', filePath ] )
                AdminConfig.save()
            except :
                Type, value = sys.exc_info()[ :2 ]
                print '\nError: updateApp failed.'
                print str( value )
        else :
            print '\n  Error: Invalid file specified:', fixFileName( filePath )
            Usage()
    else :
        print '\n  Error: Invalid path specified:', fixFileName( filePath )
        Usage()

    #---------------------------------------------------------------------------
    # Is synchronization requested & possible?
    # Note: this only makes sense when connected to a Deployment Manager
    #---------------------------------------------------------------------------
    if nosync != 'nosync' :
        try :
            dm = AdminControl.queryNames( 'type=DeploymentManager,*' )
            print 'dm: "%s"' % dm
            #-------------------------------------------------------------------
            # dm != '' only when we're connected to the DM
            #-------------------------------------------------------------------
            if dm :
                print 'Synchronizing with the active nodes.'
                result = AdminControl.invoke( dm, 'syncActiveNodes', 'true' )
        except :
            Type, value = sys.exc_info()[ :2 ]
            Type, value = str( Type ), str( value )
            if value.endswith( 'AdminControl service not available' ) :
                print '\nError: Synchronization failed -', value.split( ':', 1 )[ 1 ]
            else :
                print '\nError:', str( Type )
                print 'value:', str( value )

#-------------------------------------------------------------------------------
# Name: Usage
# Role: Display the script "docstring" (aka Usage information)
#-------------------------------------------------------------------------------
def Usage( cmdName = None ) :
    if not cmdName :
        cmdName = 'updateApp'

    print __doc__ % locals()
    sys.exit()

#-------------------------------------------------------------------------------
# Name: anonymous
# Role: Verify that the script was executed, and not imported
# Note: Apparent starting place for script execution
#-------------------------------------------------------------------------------
if __name__ == '__main__' :
    try :
        argc = len( sys.argv )
        if 1 < argc < 4 :
            process( *sys.argv )
        else :
            print '\n  Error: Unexpected number of arguments specified:', argc
            Usage()
    except :
        Type, value = sys.exc_info()[ :2 ]
        Type, value = str( Type ), str( value )
        if not Type.endswith( 'SystemExit' ) :
            print 'Error:', str( Type )
            print 'value:', str( value )
else :
    print '\n  Error: This script should be executed, not imported.'
    Usage( __name__ )
