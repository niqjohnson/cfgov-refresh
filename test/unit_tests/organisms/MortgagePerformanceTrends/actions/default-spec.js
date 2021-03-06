const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const mockery = require( 'mockery' );
const sinon = require( 'sinon' );
const expect = chai.expect;

// Disable the AJAX library used by the action creator
const noop = () => ( {} );
mockery.enable( {
  warnOnReplace: false,
  warnOnUnregistered: false
} );
mockery.registerMock( 'xdr', noop );

mockery.registerMock( '../utils', {
  getNonMetroData: cb => {
    const nonMetros = [
      {
        valid: true,
        fips: '12345',
        name: 'Acme metro',
        abbr: 'AL'
      }
    ];
    cb( nonMetros );
  }
} );

const actions = require(
  BASE_JS_PATH + 'organisms/MortgagePerformanceTrends/actions/default.js'
)();

describe( 'Mortgage Performance default action creators', () => {

  it( 'should create an action to set a geo', () => {
    const action = actions.setGeo( 12345, 'Alabama', 'state' );
    expect( action ).to.deep.equal( {
      type: 'SET_GEO',
      geo: {
        type: 'state',
        id: 12345,
        name: 'Alabama'
      }
    } );
  } );

  it( 'should create an action to clear geos', () => {
    const action = actions.clearGeo();
    expect( action ).to.deep.equal( {
      type: 'CLEAR_GEO'
    } );
  } );

  it( 'should create actions to update charts', () => {
    let action = actions.updateChart( 12345, 'Alabama', 'state', false );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_CHART',
      geo: {
        type: 'state',
        id: 12345,
        name: 'Alabama'
      },
      includeComparison: false
    } );
    action = actions.updateChart( null, null, null, false );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_CHART',
      geo: {
        id: null,
        name: null
      },
      includeComparison: false
    } );
  } );

  it( 'should create an action to update the national comparison', () => {
    const action = actions.updateNational( false );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_CHART',
      includeComparison: false
    } );
  } );

  it( 'should create an action to update the date', () => {
    const action = actions.updateDate( '2010-01' );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_DATE',
      date: '2010-01'
    } );
  } );

  it( 'should create an action to request counties', () => {
    const action = actions.requestCounties();
    expect( action ).to.deep.equal( {
      type: 'REQUEST_COUNTIES',
      isLoadingCounties: true
    } );
  } );

  it( 'should create an action to request metros', () => {
    const action = actions.requestMetros();
    expect( action ).to.deep.equal( {
      type: 'REQUEST_METROS',
      isLoadingMetros: true
    } );
  } );

  it( 'should create an action to request non-metros', () => {
    const action = actions.requestNonMetros();
    expect( action ).to.deep.equal( {
      type: 'REQUEST_NON_METROS',
      isLoadingNonMetros: true
    } );
  } );

  it( 'should dispatch actions to fetch non-metros', () => {
    const dispatch = sinon.spy();
    actions.fetchNonMetros( 'AL', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 4 );
    actions.fetchNonMetros( 'CA', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 8 );
  } );

  it( 'should fail on bad non-metro state abbr', () => {
    expect( actions.fetchNonMetros( 'bloop', true ) ).to.throw();
  } );

  it( 'should create an action to set metros', () => {
    const action = actions.setMetros( [ { name: 'Akron, OH' } ] );
    expect( action ).to.deep.equal( {
      type: 'SET_METROS',
      metros: [ { name: 'Akron, OH' } ]
    } );
  } );

  it( 'should create an action to set non-metros', () => {
    const action = actions.setNonMetros( [ { name: 'Tampa, FL' } ] );
    expect( action ).to.deep.equal( {
      type: 'SET_NON_METROS',
      nonMetros: [ { name: 'Tampa, FL' } ]
    } );
  } );

  it( 'should create an action to set counties', () => {
    const action = actions.setCounties( [ { name: 'Acme County' } ] );
    expect( action ).to.deep.equal( {
      type: 'SET_COUNTIES',
      counties: [ { name: 'Acme County' } ]
    } );
  } );

  it( 'should create an action to start loading', () => {
    const action = actions.startLoading();
    expect( action ).to.deep.equal( {
      type: 'START_LOADING',
      isLoading: true
    } );
  } );

  it( 'should create an action to stop loading', () => {
    const action = actions.stopLoading();
    expect( action ).to.deep.equal( {
      type: 'STOP_LOADING',
      isLoading: false
    } );
  } );

} );
