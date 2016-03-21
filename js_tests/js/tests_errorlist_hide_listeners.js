console.log('start loading errorlist_hide_listeners.js');

var stub;   // common for all tests, is set to {} before and restored after each test

function set_dummy_error_row( row, input ){
	if ( input === undefined ) { input = 'input' }
    row.toggleClass( "error", true );
    var err = '<ul class="errorlist"><li>ERROR MESSAGE.</li></ul>';
    row.find( input ).before( err );    
}
//=============================================================================
QUnit.module( "errorlist_hide_listeners hide_error", function( hooks ) { 
	var $target;
	var expected_arg;
	var $expected_target;
    hooks.beforeEach( function( assert ) {
		var row = $( 'tr1' );
		set_dummy_error_row( row );
		$target = $( '#id_name1' );
		expected_arg = ".errorlist";
		$expected_target = $target.siblings( expected_arg );
        stub = {};
        stub.siblings 	= sinon.spy( jQuery.prototype, "siblings" );
        stub.hide 		= sinon.spy( jQuery.prototype, "hide" );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( "hide_error", function( assert ) {
        expect( 7 );
		
		var res = hide_error.apply( $target );
        
        assert.equal( stub.siblings.callCount, 1, 'siblings should be called 1 times' );
        assert.equal( stub.hide.callCount, 1, 'hide should be called 1 times' );

        assert.deepEqual( stub.siblings.thisValues[0], $target, 'siblings called as method of proper this' );
        assert.deepEqual( stub.hide.thisValues[0], $expected_target, 'hide called as method of proper this' );
        assert.ok( stub.siblings.getCall( 0 ).calledWithExactly( expected_arg ), 'siblings called with args' );
        assert.ok( stub.hide.getCall( 0 ).calledWithExactly( ), 'hide called with proper args' );

		assert.equal( res, undefined, 'hide_error should return undefined' );
    } );
} );
//=============================================================================
QUnit.module( "set_errorlist_hide_listeners", function( hooks ) { 
	var $targets;
	var args;
	var handlers;
    hooks.beforeEach( function( assert ) {
        stub = {};
        stub.off 		= sinon.spy( jQuery.prototype, "off" );
        stub.on  		= sinon.spy( jQuery.prototype, "on" );
		$targets = [
			$( 'input' ),
			$( 'select' ),
			$( 'input[type="file"]' )
		];
		args = [
			'keypress',
			'change',
			'click'
		];
        handlers = [
			hide_error,
			hide_error,
			hide_error
		];
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( "set_errorlist_hide_listeners", function( assert ) {
        expect( 15 );
		var $target = $( '#id_name' );
		var event = "keypress";
		
		var res = set_errorlist_hide_listeners();

		assert.equal( stub.off.callCount, 3, 'off should be called 3 times' );
        assert.equal( stub.on.callCount, 3, 'on should be called 3 times' );

        var i;
        for ( i=0 ; i<3 ; i++ ){
            assert.deepEqual( stub.off.thisValues[i], $targets[i], i+': off called as method of proper this' );
            assert.deepEqual( stub.off.args[i], [ args[i] ], i+': off called with proper args' );
            assert.deepEqual( stub.on.thisValues[i], $targets[i], i+': on called as method of proper this' );
            assert.deepEqual( stub.on.args[i], [ args[i], handlers[i] ], i+': on called with proper args' );
        }

        assert.equal( res, undefined, 'set_errorlist_hide_listeners should return undefined' );
    } );
} );
//=============================================================================
QUnit.module( "errorlist_hide_listeners keypress", function( hooks ) { 
	var row1;
	var row2;
	var $input;
	var event;
    hooks.beforeEach( function( assert ) {
		row1 = $( '#tr1' );
		row2 = $( '#tr2' );
		$input = $( '#id_name1' );
		event = 'keypress';
		set_errorlist_hide_listeners(); 
    } );
    hooks.afterEach( function( assert ) {
    } );
	QUnit.test( "error message should be hidden after keypress", function ( assert ) {
		expect( 4 );
		set_dummy_error_row( row1 );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), false );
		$input.trigger( event );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), false );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), false );
	});
	QUnit.test( "error message not be hidden on keypress in another field", function ( assert ) {
		expect( 2 );
		set_dummy_error_row( row1 );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
		$( 'tr' ).last().find( 'input' ).trigger( event );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
	});
	QUnit.test( "only proper error message should be hidden on keypress", function ( assert ) {
		expect( 4 );
		set_dummy_error_row( row1 );
		set_dummy_error_row( row2 );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), true );
		$input.trigger( event );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), false );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), true );
	});
} );
/* This test module pass well under Qunit, but error fired under Selenium => wrapped by comments.
//=============================================================================
QUnit.module( "errorlist_hide_listeners click button file", function( hooks ) { 
	var row1;
	var row2;
	var $input;
	var event;
    hooks.beforeEach( function( assert ) {
		row1 = $( '#trb1' );
		row2 = $( '#trb2' );
		$input = $( '#id_file1' );
		event = 'click';
		set_errorlist_hide_listeners(); 
		document.getElementById( '#id_file1' ).onchange = function() {
			// fire the upload here
		};
		document.getElementById( '#id_file2' ).onchange = function() {
			// fire the upload here
		};		
    } );
    hooks.afterEach( function( assert ) {
    } );
	QUnit.test( "error message should be hidden after click", function ( assert ) {
		expect( 4 );
		set_dummy_error_row( row1 );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), false );
		$input.trigger( event );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), false );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), false );
	});
	QUnit.test( "error message not be hidden on click in another field", function ( assert ) {
		expect( 2 );
		set_dummy_error_row( row1 );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
		$( 'tr' ).last().find( 'input' ).trigger( event );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
	});
	QUnit.test( "only proper error message should be hidden on click", function ( assert ) {
		expect( 4 );
		set_dummy_error_row( row1 );
		set_dummy_error_row( row2 );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), true );
		$input.trigger( event );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), false );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), true );
	});
} );
*/
//=============================================================================
QUnit.module( "errorlist_hide_listeners change select", function( hooks ) { 
	var row1;
	var row2;
	var $input;
	var event;
    hooks.beforeEach( function( assert ) {
		row1 = $( '#trs1' );
		row2 = $( '#trs2' );
		$input = $( '#id_flat1' );
		event = 'change';
		set_errorlist_hide_listeners(); 
    } );
    hooks.afterEach( function( assert ) {
    } );
	QUnit.test( "error message should be hidden after change", function ( assert ) {
		expect( 4 );
		set_dummy_error_row( row1, 'select' );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), false );
		$input.trigger( event );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), false );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), false );
	});
	QUnit.test( "error message not be hidden on change in another field", function ( assert ) {
		expect( 2 );
		set_dummy_error_row( row1, 'select' );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
		$( 'tr' ).last().find( 'input' ).trigger( event );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
	});
	QUnit.test( "only proper error message should be hidden on change", function ( assert ) {
		expect( 4 );
		set_dummy_error_row( row1, 'select' );
		set_dummy_error_row( row2, 'select' );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), true );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), true );
		$input.trigger( event );
		assert.equal( $( row1 ).find( '.errorlist' ).is( ':visible' ), false );
		assert.equal( $( row2 ).find( '.errorlist' ).is( ':visible' ), true );
	});
} );
//=============================================================================
