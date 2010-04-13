#include "SIO/RunEventMap.h"

//#include "EVENT/LCIO.h"

#include <iostream>


namespace SIO  {

  const int RunEventMap::NPos ;

  RunEventMap::RunEventMap() : 
    _nRun( 0 ) ,  
    _nEvt( 0 ) {
  }

  RunEventMap::~RunEventMap(){ }


  void RunEventMap::add(const RunEvent& re, long64 pos ) {

    std::pair< Map_IT, bool> p = 
      _map.insert( std::make_pair( long64( re )  , pos ) ) ; 

    if( p.second ) {  // if event/run exists don't count as new entry

      if( re.EvtNum > -1 ) 
	++ _nEvt ;
      else
	++ _nRun ;

    } else {    // overwrite with new entry
      
      p.first->second = pos ;

    }
  }

  long64  RunEventMap::getPosition( long64 re ) {
    
    Map_IT it = _map.find( re ) ;

    return ( it != _map.end() ? it->second  :  NPos ) ;
  } 
  


}
