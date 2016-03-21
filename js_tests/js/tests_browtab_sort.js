/*
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

//=============================================================================
QUnit.module( "browtab_sort functions", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        stub.button = sinon.stub( jQuery.prototype, "button" );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'appendOrderButtons', function ( assert ) {
        expect( 11 );
        var ifirst = 1;
        var ilast  = 3;
        var col, s;

        var res = appendOrderButtons( ifirst, ilast );

        assert.equal( stub.button.callCount, 3, 'button should be called 3 times' );
        for ( col = ifirst ; col <= ilast ; col++ ){
            s = "#button-sort-" + col;
            assert.deepEqual( stub.button.thisValues[col-ifirst], $( s ), col+': button called as method of proper this' );
            assert.deepEqual( stub.button.args[col-ifirst], [], col+': button called with args' );
            assert.equal( orderAsc[col], 0, col+': appendOrderButtons should set proper values to global var' );
        }
        assert.equal( res, undefined, 'appendOrderButtons should return proper value' );
    });
    QUnit.test( 'clearOrderIcons', function ( assert ) {
        expect( 11 );
        var ifirst = 1;
        var ilast  = 3;
        var col, s;
        var img = "ui-icon-blank";
        
        var res = clearOrderIcons( ifirst, ilast );

        assert.equal( stub.button.callCount, 3, 'button should be called 3 times' );
        for ( col = ifirst ; col <= ilast ; col++ ){
            s = "#button-sort-" + col;
            assert.deepEqual( stub.button.thisValues[col-ifirst], $( s ), col+': button called as method of proper this' );
            assert.deepEqual( stub.button.args[col-ifirst], [ "option", "icons", { secondary: img } ], 
                                                                                            col+': button called with args' );
            assert.equal( orderAsc[col], 0, col+': clearOrderIcons should set proper values to global var' );
        }
        assert.equal( res, undefined, 'clearOrderIcons should return proper value' );
    });
    QUnit.test( 'changeOrderIcon asc==0', function ( assert ) {
        expect( 7 );
        var ifirst = 1;
        var ilast  = 3;
        var col = 2;
        var s = "#button-sort-" + col;
        orderAsc              = [ 0, 0, 0, 0];
        var expected_orderAsc = [ 0, 0, 1, 0];
        var img               = "ui-icon-carat-1-n";

        stub.clearOrderIcons = sinon.spy( window, "clearOrderIcons" );
        
        var res = changeOrderIcon( col, ifirst, ilast );

        assert.equal( stub.clearOrderIcons.callCount, 1, 'clearOrderIcons should be called 1 times' );
        assert.deepEqual( stub.clearOrderIcons.args[0], [ ifirst, ilast ], 'clearOrderIcons called with args' );

        assert.equal( stub.button.callCount, 4, 'button should be called 5 times' );
        assert.deepEqual( stub.button.thisValues[3], $( s ), 'button called as method of proper this' );
        assert.deepEqual( stub.button.args[3], [ "option", "icons", { secondary: img } ], 'button called with args' );
        assert.deepEqual( orderAsc, expected_orderAsc, 'changeOrderIcon should set proper values to global var' );

        assert.equal( res, undefined, 'changeOrderIcon should return proper value' );
    });
    QUnit.test( 'changeOrderIcon asc==1', function ( assert ) {
        expect( 7 );
        var ifirst = 1;
        var ilast  = 3;
        var col = 2;
        var s = "#button-sort-" + col;
        orderAsc              = [ 0, 0,  1, 0];
        var expected_orderAsc = [ 0, 0, -1, 0];
        var img               = "ui-icon-carat-1-s";

        stub.clearOrderIcons = sinon.spy( window, "clearOrderIcons" );
        
        var res = changeOrderIcon( col, ifirst, ilast );

        assert.equal( stub.clearOrderIcons.callCount, 1, 'clearOrderIcons should be called 1 times' );
        assert.deepEqual( stub.clearOrderIcons.args[0], [ ifirst, ilast ], 'clearOrderIcons called with args' );

        assert.equal( stub.button.callCount, 4, 'button should be called 5 times' );
        assert.deepEqual( stub.button.thisValues[3], $( s ), 'button called as method of proper this' );
        assert.deepEqual( stub.button.args[3], [ "option", "icons", { secondary: img } ], 'button called with args' );
        assert.deepEqual( orderAsc, expected_orderAsc, 'changeOrderIcon should set proper values to global var' );

        assert.equal( res, undefined, 'changeOrderIcon should return proper value' );
    });
    QUnit.test( 'changeOrderIcon asc==-1', function ( assert ) {
        expect( 7 );
        var ifirst = 1;
        var ilast  = 3;
        var col = 2;
        var s = "#button-sort-" + col;
        orderAsc              = [ 0, 0, -0, 0];
        var expected_orderAsc = [ 0, 0,  1, 0];
        var img               = "ui-icon-carat-1-n";

        stub.clearOrderIcons = sinon.spy( window, "clearOrderIcons" );
        
        var res = changeOrderIcon( col, ifirst, ilast );

        assert.equal( stub.clearOrderIcons.callCount, 1, 'clearOrderIcons should be called 1 times' );
        assert.deepEqual( stub.clearOrderIcons.args[0], [ ifirst, ilast ], 'clearOrderIcons called with args' );

        assert.equal( stub.button.callCount, 4, 'button should be called 5 times' );
        assert.deepEqual( stub.button.thisValues[3], $( s ), 'button called as method of proper this' );
        assert.deepEqual( stub.button.args[3], [ "option", "icons", { secondary: img } ], 'button called with args' );
        assert.deepEqual( orderAsc, expected_orderAsc, 'changeOrderIcon should set proper values to global var' );

        assert.equal( res, undefined, 'changeOrderIcon should return proper value' );
    });
    QUnit.test( 'changeOrderIcon asc==undefined', function ( assert ) {
        expect( 7 );
        var ifirst = 1;
        var ilast  = 3;
        var col = 2;
        var s = "#button-sort-" + col;
        orderAsc              = [ 0, 0, undefined, 0];
        var expected_orderAsc = [ 0, 0, NaN,       0];
        var img               = "ui-icon-blank";

        stub.clearOrderIcons = sinon.spy( window, "clearOrderIcons" );
        
        var res = changeOrderIcon( col, ifirst, ilast );

        assert.equal( stub.clearOrderIcons.callCount, 1, 'clearOrderIcons should be called 1 times' );
        assert.deepEqual( stub.clearOrderIcons.args[0], [ ifirst, ilast ], 'clearOrderIcons called with args' );

        assert.equal( stub.button.callCount, 4, 'button should be called 5 times' );
        assert.deepEqual( stub.button.thisValues[3], $( s ), 'button called as method of proper this' );
        assert.deepEqual( stub.button.args[3], [ "option", "icons", { secondary: img } ], 'button called with args' );
        assert.deepEqual( orderAsc, expected_orderAsc, 'changeOrderIcon should set proper values to global var' );

        assert.equal( res, undefined, 'changeOrderIcon should return proper value' );
    });
    QUnit.test( 'changeOrderGroupIcon true', function ( assert ) {
        expect( 5 );
        var col = 1;
        var s = "#button-sort-" + col;
        orderGroup              = true;
        var expected_orderGroup = false;
        var img                 = "ui-icon-shuffle";

        var res = changeOrderGroupIcon( col );

        assert.equal( stub.button.callCount, 1, 'button should be called 5 times' );
        assert.deepEqual( stub.button.thisValues[0], $( s ), 'button called as method of proper this' );
        assert.deepEqual( stub.button.args[0], [ "option", "icons", { secondary: img } ], 'button called with args' );
        assert.equal( orderGroup, expected_orderGroup, 'changeOrderGroupIcon should set proper values to global var' );

        assert.equal( res, undefined, 'changeOrderGroupIcon should return proper value' );
    });
    QUnit.test( 'changeOrderGroupIcon false', function ( assert ) {
        expect( 5 );
        var col = 1;
        var s = "#button-sort-" + col;
        orderGroup              = false;
        var expected_orderGroup = true;
        var img                 = "ui-icon-transfer-e-w";

        var res = changeOrderGroupIcon( col );

        assert.equal( stub.button.callCount, 1, 'button should be called 5 times' );
        assert.deepEqual( stub.button.thisValues[0], $( s ), 'button called as method of proper this' );
        assert.deepEqual( stub.button.args[0], [ "option", "icons", { secondary: img } ], 'button called with args' );
        assert.equal( orderGroup, expected_orderGroup, 'changeOrderGroupIcon should set proper values to global var' );

        assert.equal( res, undefined, 'changeOrderGroupIcon should return proper value' );
    });
    QUnit.test( 'changeOrderGroupIcon undefined', function ( assert ) {
        expect( 5 );
        var col = 1;
        var s = "#button-sort-" + col;
        orderGroup              = undefined;
        var expected_orderGroup = true;
        var img                 = "ui-icon-transfer-e-w";

        var res = changeOrderGroupIcon( col );

        assert.equal( stub.button.callCount, 1, 'button should be called 5 times' );
        assert.deepEqual( stub.button.thisValues[0], $( s ), 'button called as method of proper this' );
        assert.deepEqual( stub.button.args[0], [ "option", "icons", { secondary: img } ], 'button called with args' );
        assert.equal( orderGroup, expected_orderGroup, 'changeOrderGroupIcon should set proper values to global var' );

        assert.equal( res, undefined, 'changeOrderGroupIcon should return proper value' );
    });
    QUnit.test( 'get_ordered_col', function ( assert ) {
        expect( 10 );
        var arr = [
                [ 0, 0, 0, 0],
                [ 1, 0, 0, 0],
                [ 0, 1, 0, 0],
                [ 0, 0, 1, 0],
                [ 0, 0, 0, 1],
                [ -1, 0, 0, 0],
                [ 0, -1, 0, 0],
                [ 0, 0, -1, 0],
                [ 0, 0, 0, -1],
                [ 0, 1, 1, 0]
        ];
        var expected_cols = [ 0, 0, 1, 2, 3, 0, 1, 2, 3, 1 ];
        var res, i;
        for ( i = 0; i < 10; i++ ){
            orderAsc = arr[i];
            res = get_ordered_col( );
            assert.equal( res, expected_cols[i], 'get_ordered_col should return proper value' );
        };
    });
} );
//=============================================================================
