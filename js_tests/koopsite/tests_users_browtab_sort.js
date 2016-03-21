/*
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

//=============================================================================
QUnit.module( "users_browtab_sort document ready", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        columnsNumber = 8;
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'users_browtab_sort_document_ready_handler', function ( assert ) {
        expect( 7 );

        stub.appendOrderButtons                         = sinon.stub( window, "appendOrderButtons" );
        stub.changeOrderIcon                            = sinon.stub( window, "changeOrderIcon" );
        stub.set_users_browtab_sort_buttons_listeners  = sinon.stub( window, "set_users_browtab_sort_buttons_listeners" );

        var res = users_browtab_sort_document_ready_handler( );

        assert.ok( stub.appendOrderButtons.calledOnce, 'appendOrderButtons should be called once' );
        assert.ok( stub.appendOrderButtons.calledWithExactly( 1, columnsNumber ), 
                                                        'appendOrderButtons should be called with arg' );
        assert.ok( stub.changeOrderIcon.calledOnce, 'changeOrderIcon should be called once' );
        assert.ok( stub.changeOrderIcon.calledWithExactly( 1, 1, columnsNumber ), 
                                                        'changeOrderIcon should be called with arg' );
        assert.ok( stub.set_users_browtab_sort_buttons_listeners.calledOnce, 
                                                        'set_users_browtab_sort_buttons_listeners should be called once' );
        assert.ok( stub.set_users_browtab_sort_buttons_listeners.calledWithExactly( ), 
                                                        'set_users_browtab_sort_buttons_listeners should be called with arg' );

        assert.equal( res, undefined, 'users_browtab_sort_document_ready_handler should return undefined' );
    });
    QUnit.test( 'set_users_browtab_sort_buttons_listeners', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 35 );

        stub.off = sinon.spy( jQuery.prototype, "off" );
        stub.on  = sinon.spy( jQuery.prototype, "on" );

        var res = set_users_browtab_sort_buttons_listeners( );

        assert.equal( stub.off.callCount, columnsNumber, 'off should be called columnsNumber times' );
        assert.equal( stub.on.callCount, columnsNumber, 'on should be called columnsNumber times' );

        var col;
        for ( col=1 ; col<=columnsNumber ; col++ ){
            assert.deepEqual( stub.off.thisValues[col-1], $( "#button-sort-"+col ), 
                                                                        col+': off called as method of proper this' );
            assert.deepEqual( stub.on.thisValues[col-1], $( "#button-sort-"+col ), 
                                                                        col+': on called as method of proper this' );
            assert.ok( stub.off.getCall( col-1 ).calledWithExactly( "click" ), col+':on called with args' );
            assert.ok( stub.on.getCall( col-1 ).calledWith( "click"), col+': off called with proper args' );
        }
        assert.equal( res, undefined, 'set_users_browtab_sort_buttons_listeners should return false' );
    });
    QUnit.test( 'set_users_browtab_sort_buttons_listeners functional', function ( assert ) {
        expect( 9 );

        stub.ordering = sinon.stub( window, "ordering" );

        appendOrderButtons( 1, columnsNumber );
        set_users_browtab_sort_buttons_listeners( );

        var col, s;
        for ( col = 1 ; col <= columnsNumber ; col++ ){
            s = "#button-sort-" + col;
            $( s ).click();
        }

        assert.equal( stub.ordering.callCount, columnsNumber, 'ordering should be called columnsNumber times' );
        for ( col = 1 ; col <= columnsNumber ; col++ ){
            assert.deepEqual( stub.ordering.args[col-1], [ col ], 'ordering should be called with args' );
        }
    });
} );
//=============================================================================
QUnit.module( "users_browtab_sort functions", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'ordering', function ( assert ) {
        expect( 8 );

        var col = 1;
        columnsNumber = 8;
        var qsTRarr = [ 'qsTRarr' ];
        qs_TR_arr = [ 'qs_TR_arr' ];

        orderAsc        = [0, 0, 0, 0, 0];

        stub.changeOrderIcon    = sinon.stub( window, "changeOrderIcon" );
        stub.sort_table         = sinon.stub( window, "sort_table" ).returns( qsTRarr );
        stub.display_qs_TR_arr  = sinon.stub( window, "display_qs_TR_arr" );

        var res = ordering( col );

        assert.ok( stub.changeOrderIcon.calledOnce, 'changeOrderIcon should be called once' );
        assert.ok( stub.changeOrderIcon.calledWithExactly( col, 1, columnsNumber ), 
                                                                'changeOrderIcon should be called with arg' );
        assert.ok( stub.sort_table.calledOnce, 'sort_table should be called once' );
        assert.ok( stub.sort_table.calledWithExactly( [ 'qs_TR_arr' ], col, orderAsc[col] ), 
                                                        'sort_table should be called with arg' );
        assert.ok( stub.display_qs_TR_arr.calledOnce, 'display_qs_TR_arr should be called once' );
        assert.ok( stub.display_qs_TR_arr.calledWithExactly( ), 'display_qs_TR_arr should be called with arg' );

        assert.deepEqual( qs_TR_arr, qsTRarr, 'ordering should set proper value to global var' );

        assert.equal( res, undefined, 'ordering should return undefined' );
    });
    QUnit.test( 'parseFlatNo', function ( assert ) {
        expect( 8 );
        assert.equal( parseFlatNo( '' ), 0.0, 'parseFlatNo should return proper value' );
        assert.equal( parseFlatNo( '1' ), 1.0, 'parseFlatNo should return proper value' );
        assert.equal( parseFlatNo( '1a' ), 1.097, 'parseFlatNo should return proper value' );
        assert.equal( parseFlatNo( '1A' ), 1.097, 'parseFlatNo should return proper value' );
        assert.equal( parseFlatNo( 'z' ), 0.122, 'parseFlatNo should return proper value' );
        assert.equal( parseFlatNo( 'Z' ), 0.122, 'parseFlatNo should return proper value' );
        assert.equal( parseFlatNo( 'Zz' ), 0.122122, 'parseFlatNo should return proper value' );
        assert.equal( parseFlatNo( '1a1' ), 1.097049, 'parseFlatNo should return proper value' );
    });
    QUnit.test( 'parseBoolNull', function ( assert ) {
        expect( 4 );
        assert.equal( parseBoolNull( true ), 1, 'parseBoolNull should return proper value' );
        assert.equal( parseBoolNull( false ), -1, 'parseBoolNull should return proper value' );
        assert.equal( parseBoolNull( null ), 0, 'parseBoolNull should return proper value' );
        assert.equal( parseBoolNull( undefined ), -1, 'parseBoolNull should return proper value' );
    });
} );
//=============================================================================
QUnit.module( "users_browtab_sort sort_table", function( hooks ) { 
    var arr;
    hooks.beforeEach( function( assert ) {
        stub = {};
        arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true] 
        ];
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    //-----------------------------------------------------------------
    QUnit.test( 'col=1, asc=1', function ( assert ) {
        expect( 1 );
        var col     = 1;
        var asc     = 1;
        var expected_arr = [
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true] 
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=1, asc=-1', function ( assert ) {
        expect( 1 );
        var col     = 1;
        var asc     = -1;
        var expected_arr = [
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true], 
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( 'col=2, asc=1', function ( assert ) {
        expect( 1 );
        var col     = 2;
        var asc     = 1;
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true] 
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=2, asc=-1', function ( assert ) {
        expect( 1 );
        var col     = 2;
        var asc     = -1;
        var expected_arr = [
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true], 
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( 'col=3, asc=1', function ( assert ) {
        expect( 1 );
        var col     = 3;
        var asc     = 1;
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=3, asc=-1', function ( assert ) {
        expect( 1 );
        var col     = 3;
        var asc     = -1;
        var expected_arr = [
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true],
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( 'col=4, asc=1', function ( assert ) {
        expect( 1 );
        var col     = 4;
        var asc     = 1;
        var expected_arr = [
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true],
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=4, asc=-1', function ( assert ) {
        expect( 1 );
        var col     = 4;
        var asc     = -1;
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true] 
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( 'col=5, asc=1', function ( assert ) {
        expect( 1 );
        var col     = 5;
        var asc     = 1;
        var expected_arr = [
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=5, asc=-1', function ( assert ) {
        expect( 1 );
        var col     = 5;
        var asc     = -1;
        var expected_arr = [
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true],
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( 'col=6, asc=1', function ( assert ) {
        expect( 1 );
        var col     = 6;
        var asc     = 1;
        var expected_arr = [
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=6, asc=-1', function ( assert ) {
        expect( 1 );
        var col     = 6;
        var asc     = -1;
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( 'col=7, asc=1', function ( assert ) {
        expect( 1 );
        var col     = 7;
        var asc     = 1;
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true] 
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=7, asc=-1', function ( assert ) {
        expect( 1 );
        var col     = 7;
        var asc     = -1;
        var expected_arr = [
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true], 
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( 'col=8, asc=1', function ( assert ) {
        expect( 1 );
        var col     = 8;
        var asc     = 1;
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true] 
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=8, asc=-1', function ( assert ) {
        expect( 1 );
        var col     = 8;
        var asc     = -1;
        var expected_arr = [
                [{1:1},'Beta', 'bbc', '15','EeE', '2010', false,    false, true],
                [{3:3},'gama', 'bBc', '1a','BbB', '2016', true,     true,  true],
                [{0:0},'beta', 'abc', '1', 'eEe', '2012', true,     false, false],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011', null     ,true,  false]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
} );
