
const class State() {
  constructor( options = {} ) {
    this.options = options;
    this.events = {}
  }
  add( componentState ) {
    this[ componentState.ID ] = componentState
    if ( this.options.dispatchOnAdd ) {
      this.dispatch( componentState );
    }
  }
  filter( criteria ) {
    return Object.keys( this ).map(key => this[key] )
          .filter( obj => {
            const key = Object.keys(criteria)[0];
            const value = Object.values(criteria)[0];

            return obj[key] === value;
          } );
  }
  subscribe( eventName, callback ) {
    this.events[eventName] = this.events[eventName] || [];
    this.events[eventName].push( callback );
  }
  dispatch( eventName ) {
    this.events[eventName] = this.events[eventName] || [];
    for ( var i = 0, len = this[eventName].length; i < len; i++ ) {
      this.events[eventName][i].apply( this, arguments );
    }
  }
};

module.exports = { STATE };
