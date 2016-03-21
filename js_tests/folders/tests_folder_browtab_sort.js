/*
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

//=============================================================================
QUnit.module( "folder_browtab_sort document ready", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        columnsNumber = 4;
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'folder_browtab_sort_document_ready_handler', function ( assert ) {
        expect( 9 );

        stub.appendOrderButtons                         = sinon.stub( window, "appendOrderButtons" );
        stub.changeOrderIcon                            = sinon.stub( window, "changeOrderIcon" );
        stub.changeOrderGroupIcon                       = sinon.stub( window, "changeOrderGroupIcon" );
        stub.set_folder_browtab_sort_buttons_listeners  = sinon.stub( window, "set_folder_browtab_sort_buttons_listeners" );

        var res = folder_browtab_sort_document_ready_handler( );

        assert.ok( stub.appendOrderButtons.calledOnce, 'appendOrderButtons should be called once' );
        assert.ok( stub.appendOrderButtons.calledWithExactly( 1, columnsNumber ), 
                                                        'appendOrderButtons should be called with arg' );
        assert.ok( stub.changeOrderIcon.calledOnce, 'changeOrderIcon should be called once' );
        assert.ok( stub.changeOrderIcon.calledWithExactly( 2, 2, columnsNumber ), 
                                                        'changeOrderIcon should be called with arg' );
        assert.ok( stub.changeOrderGroupIcon.calledOnce, 'changeOrderGroupIcon should be called once' );
        assert.ok( stub.changeOrderGroupIcon.calledWithExactly( 1 ), 
                                                        'changeOrderGroupIcon should be called with arg' );
        assert.ok( stub.set_folder_browtab_sort_buttons_listeners.calledOnce, 
                                                        'set_folder_browtab_sort_buttons_listeners should be called once' );
        assert.ok( stub.set_folder_browtab_sort_buttons_listeners.calledWithExactly( ), 
                                                        'set_folder_browtab_sort_buttons_listeners should be called with arg' );

        assert.equal( res, undefined, 'folder_browtab_sort_document_ready_handler should return undefined' );
    });
    QUnit.test( 'set_folder_browtab_sort_buttons_listeners', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 19 );

        stub.off = sinon.spy( jQuery.prototype, "off" );
        stub.on  = sinon.spy( jQuery.prototype, "on" );

        var res = set_folder_browtab_sort_buttons_listeners( );

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
        assert.equal( res, undefined, 'set_folder_browtab_sort_buttons_listeners should return false' );
    });
    QUnit.test( 'set_folder_browtab_sort_buttons_listeners functional', function ( assert ) {
        expect( 6 );

        stub.grouping = sinon.stub( window, "grouping" );
        stub.ordering = sinon.stub( window, "ordering" );

        appendOrderButtons( 1, columnsNumber );
        set_folder_browtab_sort_buttons_listeners( );

        var col, s;
        for ( col = 1 ; col <= columnsNumber ; col++ ){
            s = "#button-sort-" + col;
            $( s )[0].click();
        }

        assert.equal( stub.grouping.callCount, 1, 'grouping should be called 1 times' );
        assert.equal( stub.ordering.callCount, columnsNumber-1, 'ordering should be called columnsNumber-1 times' );
        col = 1;
        assert.deepEqual( stub.grouping.args[col-1], [ col ], 'grouping should be called with args' );
        for ( col = 2 ; col <= columnsNumber ; col++ ){
            assert.deepEqual( stub.ordering.args[col-2], [ col ], 'ordering should be called with args' );
        }
    });
} );
//=============================================================================
QUnit.module( "folder_browtab_sort functions", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'grouping orderAsc=[0, 0, 0, 0, 0]', function ( assert ) {
        expect( 8 );

        var col = 1;
        var qsTRarr = [ 'qsTRarr' ];
        qs_TR_arr = [ 'qs_TR_arr' ];

        orderAsc        = [0, 0, 0, 0, 0];
        var ordered_col = -1;
        
        stub.changeOrderGroupIcon   = sinon.stub( window, "changeOrderGroupIcon" );
        stub.sort_table             = sinon.stub( window, "sort_table" ).returns( qsTRarr );
        stub.display_qs_TR_arr      = sinon.stub( window, "display_qs_TR_arr" );

        var res = grouping( col );

        assert.ok( stub.changeOrderGroupIcon.calledOnce, 'changeOrderGroupIcon should be called once' );
        assert.ok( stub.changeOrderGroupIcon.calledWithExactly( col ), 'changeOrderGroupIcon should be called with arg' );
        assert.ok( stub.sort_table.calledOnce, 'sort_table should be called once' );
        assert.ok( stub.sort_table.calledWithExactly( [ 'qs_TR_arr' ], ordered_col, orderAsc[ordered_col] ), 
                                                        'sort_table should be called with arg' );
        assert.ok( stub.display_qs_TR_arr.calledOnce, 'display_qs_TR_arr should be called once' );
        assert.ok( stub.display_qs_TR_arr.calledWithExactly( ), 'display_qs_TR_arr should be called with arg' );

        assert.deepEqual( qs_TR_arr, qsTRarr, 'grouping should set proper value to global var' );

        assert.equal( res, undefined, 'grouping should return undefined' );
    });
    QUnit.test( 'grouping orderAsc=[0, 1, 0, 0, 0]', function ( assert ) {
        expect( 8 );

        var col = 1;
        var qsTRarr = [ 'qsTRarr' ];
        qs_TR_arr = [ 'qs_TR_arr' ];

        orderAsc        = [0, 1, 0, 0, 0];
        var ordered_col = 1;
        
        stub.changeOrderGroupIcon   = sinon.stub( window, "changeOrderGroupIcon" );
        stub.sort_table             = sinon.stub( window, "sort_table" ).returns( qsTRarr );
        stub.display_qs_TR_arr      = sinon.stub( window, "display_qs_TR_arr" );

        var res = grouping( col );

        assert.ok( stub.changeOrderGroupIcon.calledOnce, 'changeOrderGroupIcon should be called once' );
        assert.ok( stub.changeOrderGroupIcon.calledWithExactly( col ), 'changeOrderGroupIcon should be called with arg' );
        assert.ok( stub.sort_table.calledOnce, 'sort_table should be called once' );
        assert.ok( stub.sort_table.calledWithExactly( [ 'qs_TR_arr' ], ordered_col, orderAsc[ordered_col] ), 
                                                        'sort_table should be called with arg' );
        assert.ok( stub.display_qs_TR_arr.calledOnce, 'display_qs_TR_arr should be called once' );
        assert.ok( stub.display_qs_TR_arr.calledWithExactly( ), 'display_qs_TR_arr should be called with arg' );

        assert.deepEqual( qs_TR_arr, qsTRarr, 'grouping should set proper value to global var' );

        assert.equal( res, undefined, 'grouping should return undefined' );
    });
    QUnit.test( 'grouping orderAsc=[0, -1, 0, 0, 0]', function ( assert ) {
        expect( 8 );

        var col = 1;
        var qsTRarr = [ 'qsTRarr' ];
        qs_TR_arr = [ 'qs_TR_arr' ];

        orderAsc        = [0, -1, 0, 0, 0];
        var ordered_col = 1;
        
        stub.changeOrderGroupIcon   = sinon.stub( window, "changeOrderGroupIcon" );
        stub.sort_table             = sinon.stub( window, "sort_table" ).returns( qsTRarr );
        stub.display_qs_TR_arr      = sinon.stub( window, "display_qs_TR_arr" );

        var res = grouping( col );

        assert.ok( stub.changeOrderGroupIcon.calledOnce, 'changeOrderGroupIcon should be called once' );
        assert.ok( stub.changeOrderGroupIcon.calledWithExactly( col ), 'changeOrderGroupIcon should be called with arg' );
        assert.ok( stub.sort_table.calledOnce, 'sort_table should be called once' );
        assert.ok( stub.sort_table.calledWithExactly( [ 'qs_TR_arr' ], ordered_col, orderAsc[ordered_col] ), 
                                                        'sort_table should be called with arg' );
        assert.ok( stub.display_qs_TR_arr.calledOnce, 'display_qs_TR_arr should be called once' );
        assert.ok( stub.display_qs_TR_arr.calledWithExactly( ), 'display_qs_TR_arr should be called with arg' );

        assert.deepEqual( qs_TR_arr, qsTRarr, 'grouping should set proper value to global var' );

        assert.equal( res, undefined, 'grouping should return undefined' );
    });
    QUnit.test( 'ordering', function ( assert ) {
        expect( 8 );

        var col = 1;
        columnsNumber = 4;
        var qsTRarr = [ 'qsTRarr' ];
        qs_TR_arr = [ 'qs_TR_arr' ];

        orderAsc        = [0, 0, 0, 0, 0];

        stub.changeOrderIcon    = sinon.stub( window, "changeOrderIcon" );
        stub.sort_table         = sinon.stub( window, "sort_table" ).returns( qsTRarr );
        stub.display_qs_TR_arr  = sinon.stub( window, "display_qs_TR_arr" );

        var res = ordering( col );

        assert.ok( stub.changeOrderIcon.calledOnce, 'changeOrderIcon should be called once' );
        assert.ok( stub.changeOrderIcon.calledWithExactly( col, 2, columnsNumber ), 
                                                                'changeOrderIcon should be called with arg' );
        assert.ok( stub.sort_table.calledOnce, 'sort_table should be called once' );
        assert.ok( stub.sort_table.calledWithExactly( [ 'qs_TR_arr' ], col, orderAsc[col] ), 
                                                        'sort_table should be called with arg' );
        assert.ok( stub.display_qs_TR_arr.calledOnce, 'display_qs_TR_arr should be called once' );
        assert.ok( stub.display_qs_TR_arr.calledWithExactly( ), 'display_qs_TR_arr should be called with arg' );

        assert.deepEqual( qs_TR_arr, qsTRarr, 'ordering should set proper value to global var' );

        assert.equal( res, undefined, 'ordering should return undefined' );
    });
} );
//=============================================================================
QUnit.module( "folder_browtab_sort sort_table", function( hooks ) { 
    var arr;
    hooks.beforeEach( function( assert ) {
        stub = {};
        arr = [
                [{0:0},'r','abc','2015',100],
                [{1:1},'r','bbc','2014',10],
                [{2:2},'f','aBc','2017',20],
                [{3:3},'f','bBc','2018',300] 
        ];
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    //-----------------------------------------------------------------
    QUnit.test( 'col=1, asc=1, orderGroup=false', function ( assert ) {
        expect( 1 );
        var col     = 1;
        var asc     = 1;
        orderGroup  = false;
        var expected_arr = [
                [{2:2},'f','aBc','2017',20],
                [{3:3},'f','bBc','2018',300],
                [{0:0},'r','abc','2015',100],
                [{1:1},'r','bbc','2014',10]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=1, asc=1, orderGroup=true', function ( assert ) {
        expect( 1 );
        var col     = 1;
        var asc     = 1;
        orderGroup  = true;
        var expected_arr = [
                [{2:2},'f','aBc','2017',20],
                [{3:3},'f','bBc','2018',300],
                [{0:0},'r','abc','2015',100],
                [{1:1},'r','bbc','2014',10]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=1, asc=-1, orderGroup=false', function ( assert ) {
        expect( 1 );
        var col     = 1;
        var asc     = -1;
        orderGroup  = false;
        var expected_arr = [
                [{0:0},'r','abc','2015',100],
                [{1:1},'r','bbc','2014',10],
                [{2:2},'f','aBc','2017',20],
                [{3:3},'f','bBc','2018',300] 
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=1, asc=-1, orderGroup=true', function ( assert ) {
        expect( 1 );
        var col     = 1;
        var asc     = -1;
        orderGroup  = true;
        var expected_arr = [
                [{2:2},'f','aBc','2017',20],
                [{3:3},'f','bBc','2018',300],
                [{0:0},'r','abc','2015',100],
                [{1:1},'r','bbc','2014',10]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( 'col=2, asc=1, orderGroup=false', function ( assert ) {
        expect( 1 );
        var col     = 2;
        var asc     = 1;
        orderGroup  = false;
        var expected_arr = [
                [{0:0},'r','abc','2015',100],
                [{2:2},'f','aBc','2017',20],
                [{1:1},'r','bbc','2014',10],
                [{3:3},'f','bBc','2018',300]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=2, asc=1, orderGroup=true', function ( assert ) {
        expect( 1 );
        var col     = 2;
        var asc     = 1;
        orderGroup  = true;
        var expected_arr = [
                [{2:2},'f','aBc','2017',20],
                [{3:3},'f','bBc','2018',300],
                [{0:0},'r','abc','2015',100],
                [{1:1},'r','bbc','2014',10]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=2, asc=-1, orderGroup=false', function ( assert ) {
        expect( 1 );
        var col     = 2;
        var asc     = -1;
        orderGroup  = false;
        var expected_arr = [
                [{1:1},'r','bbc','2014',10],
                [{3:3},'f','bBc','2018',300],
                [{0:0},'r','abc','2015',100],
                [{2:2},'f','aBc','2017',20]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=2, asc=-1, orderGroup=true', function ( assert ) {
        expect( 1 );
        var col     = 2;
        var asc     = -1;
        orderGroup  = true;
        var expected_arr = [
                [{3:3},'f','bBc','2018',300],
                [{2:2},'f','aBc','2017',20],
                [{1:1},'r','bbc','2014',10],
                [{0:0},'r','abc','2015',100]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( 'col=3, asc=1, orderGroup=false', function ( assert ) {
        expect( 1 );
        var col     = 3;
        var asc     = 1;
        orderGroup  = false;
        var expected_arr = [
                [{1:1},'r','bbc','2014',10],
                [{0:0},'r','abc','2015',100],
                [{2:2},'f','aBc','2017',20],
                [{3:3},'f','bBc','2018',300]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=3, asc=1, orderGroup=true', function ( assert ) {
        expect( 1 );
        var col     = 3;
        var asc     = 1;
        orderGroup  = true;
        var expected_arr = [
                [{2:2},'f','aBc','2017',20],
                [{3:3},'f','bBc','2018',300],
                [{1:1},'r','bbc','2014',10],
                [{0:0},'r','abc','2015',100]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=3, asc=-1, orderGroup=false', function ( assert ) {
        expect( 1 );
        var col     = 3;
        var asc     = -1;
        orderGroup  = false;
        var expected_arr = [
                [{3:3},'f','bBc','2018',300],
                [{2:2},'f','aBc','2017',20],
                [{0:0},'r','abc','2015',100],
                [{1:1},'r','bbc','2014',10]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=3, asc=-1, orderGroup=true', function ( assert ) {
        expect( 1 );
        var col     = 3;
        var asc     = -1;
        orderGroup  = true;
        var expected_arr = [
                [{3:3},'f','bBc','2018',300],
                [{2:2},'f','aBc','2017',20],
                [{0:0},'r','abc','2015',100],
                [{1:1},'r','bbc','2014',10]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( 'col=4, asc=1, orderGroup=false', function ( assert ) {
        expect( 1 );
        var col     = 4;
        var asc     = 1;
        orderGroup  = false;
        var expected_arr = [
                [{1:1},'r','bbc','2014',10],
                [{2:2},'f','aBc','2017',20],
                [{0:0},'r','abc','2015',100],
                [{3:3},'f','bBc','2018',300]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=4, asc=1, orderGroup=true', function ( assert ) {
        expect( 1 );
        var col     = 4;
        var asc     = 1;
        orderGroup  = true;
        var expected_arr = [
                [{2:2},'f','aBc','2017',20],
                [{3:3},'f','bBc','2018',300],
                [{1:1},'r','bbc','2014',10],
                [{0:0},'r','abc','2015',100]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=4, asc=-1, orderGroup=false', function ( assert ) {
        expect( 1 );
        var col     = 4;
        var asc     = -1;
        orderGroup  = false;
        var expected_arr = [
                [{3:3},'f','bBc','2018',300],
                [{0:0},'r','abc','2015',100],
                [{2:2},'f','aBc','2017',20],
                [{1:1},'r','bbc','2014',10]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    QUnit.test( 'col=4, asc=-1, orderGroup=true', function ( assert ) {
        expect( 1 );
        var col     = 4;
        var asc     = -1;
        orderGroup  = true;
        var expected_arr = [
                [{3:3},'f','bBc','2018',300],
                [{2:2},'f','aBc','2017',20],
                [{0:0},'r','abc','2015',100],
                [{1:1},'r','bbc','2014',10]
        ];
        var res = sort_table(arr, col, asc);
        assert.deepEqual( res, expected_arr, 'sort_table should return proper value' );
    });
    //-----------------------------------------------------------------
} );
