'''
Created on May 17, 2013

Very simple example that uses ctypes to call the ced event display
and the PyLCIO bindings to display TrackerHits and CalorimeterHits.

make sure pyLCIO and PyROOt are in your Python path, eg:

   export PYTHONPATH=${LCIO}/src/python/pyLCIO:${ROOTSYS}/lib

and that glced is running.

Note: CED (incl. glced) can be downloaded from:
 svn co https://svnsrv.desy.de/public/marlinreco/CED/trunk

@author: F.Gaede, DESY
'''

import os
from ctypes import *
import random
#import lcio

import sys

from pyLCIO.io.LcioReader import LcioReader
from pyLCIO.base.LCCollection import LCCollection


#---------------------------------------
# load CED library

pathToCED = ""
envTest = os.environ.get('CED')

if envTest != None: 
    pathToCED =  envTest

fname = pathToCED+"/lib/libCED.dylib"

if not( os.path.isfile(fname) ) :
    
    print "ERROR: cannot load CED library: ",  fname , 
    " - please set $CED to CED root directory ! " 
    exit(1) ;
    
    
ced = CDLL( fname )

#---------------------------------------


# --- wraper for ced function with float type conversion:
def pced_hit(ced, x,y,z,type,size,color):
    ced.ced_hit(   c_float(x) , c_float(y) , c_float(z) ,  type, size, color )


#-----------------------------------
def drawEvent(evt):
        
    hittypes =  { "TrackerHitPlane","TrackerHit","TrackerHitZCylinder",
                  #"SimTrackerHit","SimCalorimterHit",
                  "CalorimeterHit" }

    names = evt.getCollectionNames()
    
    for i in xrange(  names.size() ):
        
        col = evt.getCollection( names[i] )
        
        if col.getTypeName() in hittypes:
            drawHits( col )
            
#--------------------------------    
def drawHits( col ):

#    nhit = col.getNumberOfElements()
#    for i in xrange( nhit ):
#        hit=col.getElementAt(i)
#
    hits = LCCollection(col) 

    for hit in hits:
#        pos = hit.getPosition()
#        pced_hit( ced , pos[0], pos[1], pos[2] ,  0 , 1 ,  0xaaff22 )
        x,y,z=hit.getPositionVec()
        pced_hit( ced , x, y, z ,  0 , 1 ,  0xaaff22 )
        

################################################################################################


def drawEvents( fileName ):
    

#    ced.ced_new_event()
    
    ced.ced_register_elements();
    
    ced.ced_client_init("localhost",7286)
    
    rdr = LcioReader( fileName )
    
    
    event = rdr.nextEvent()
    while event:
#------------------------------------------
        ced.ced_new_event()
        
        drawEvent( event )

        ced.ced_send_event()
#-----------------------------------------
       
        text = "event " + str(event.getEventNumber()) + " " +  str(event.getRunNumber()) +" - hit enter to draw next - [q] to quit ..." 

        c = raw_input( text )
        if( c == 'q' ):
            break ;

        event = rdr.nextEvent()


################################################################################################



#-------------------------------------------------------------------------------------
def usage():
    print 'Usage:\n\tpython %s <fileName>' % ( os.path.split( sys.argv[0] )[1] )


if __name__ == "__main__":
    if len( sys.argv ) < 2:
        usage()
        sys.exit( 0 )
        
    # Read the file name from the command line input
    fileName = sys.argv[1]

    drawEvents( fileName )