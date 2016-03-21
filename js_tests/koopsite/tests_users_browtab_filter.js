/*
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

//=============================================================================
QUnit.module( "users_browtab_filter document ready", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'users_browtab_filter_document_ready_handler', function ( assert ) {
        expect( 16 );

        stub.appendFilterListeners      = sinon.stub( window, "appendFilterListeners" );
        stub.appendDateFields           = sinon.stub( window, "appendDateFields" );
        stub.appendDateFieldsListeners  = sinon.stub( window, "appendDateFieldsListeners" );
//        stub.get_filters_default        = sinon.stub( window, "get_filters_default" ).returns( "filt" );
        stub.clearFilterFields          = sinon.stub( window, "clearFilterFields" );
        stub.clearDateFields            = sinon.stub( window, "clearDateFields" );

        var res = users_browtab_filter_document_ready_handler( );

        assert.ok( stub.appendDateFields         .calledAfter( stub.appendFilterListeners     ), 'call sequence check');
        assert.ok( stub.appendDateFieldsListeners.calledAfter( stub.appendDateFields          ), 'call sequence check');
//        assert.ok( stub.get_filters_default      .calledAfter( stub.appendDateFieldsListeners ), 'call sequence check');
        assert.ok( stub.clearFilterFields        .calledAfter( stub.appendDateFieldsListeners ), 'call sequence check');
        assert.ok( stub.clearDateFields          .calledAfter( stub.clearFilterFields         ), 'call sequence check');

        assert.ok( stub.appendFilterListeners.calledOnce, 'appendFilterListeners should be called once' );
        assert.ok( stub.appendFilterListeners.calledWithExactly( ), 'appendFilterListeners should be called with arg' );
        assert.ok( stub.appendDateFields.calledOnce, 'appendDateFields should be called once' );
        assert.ok( stub.appendDateFields.calledWithExactly( ), 'appendDateFields should be called with arg' );
        assert.ok( stub.appendDateFieldsListeners.calledOnce, 'appendDateFieldsListeners should be called once' );
        assert.ok( stub.appendDateFieldsListeners.calledWithExactly( ), 
                                                                'appendDateFieldsListeners should be called with arg' );
//        assert.ok( stub.get_filters_default.calledOnce, 'get_filters_default should be called once' );
//        assert.ok( stub.get_filters_default.calledWithExactly( ), 'get_filters_default should be called with arg' );
        assert.ok( stub.clearFilterFields.calledOnce, 'clearFilterFields should be called once' );
        assert.ok( stub.clearFilterFields.calledWithExactly( ), 'clearFilterFields should be called with arg' );
        assert.ok( stub.clearDateFields.calledOnce, 'clearDateFields should be called once' );
        assert.ok( stub.clearDateFields.calledWithExactly( ), 'clearDateFields should be called with arg' );

        assert.deepEqual( radio_names, ['is_recognized', 'is_active', 'has_members', 'date_joined_all'],
                                                    'users_browtab_filter_document_ready_handler set proper global values' );
//        assert.equal( filt_val_default,  "filt" , 'users_browtab_filter_document_ready_handler set proper global values' );
//        assert.equal( filt_val_previous,  "filt" , 'users_browtab_filter_document_ready_handler set proper global values' );

        assert.equal( res, undefined, 'users_browtab_filter_document_ready_handler should return undefined' );
    });
    QUnit.test( 'appendFilterListeners', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 7 );

        var $filter_box = $( "#filter_box" );

        stub.off = sinon.spy( jQuery.prototype, "off" );
        stub.on  = sinon.spy( jQuery.prototype, "on" );

        var res = appendFilterListeners( );

        assert.equal( stub.off.callCount, 1, 'off should be called 1 times' );
        assert.equal( stub.on.callCount, 1, 'on should be called 1 times' );

        assert.deepEqual( stub.off.thisValues[0], $filter_box, 'off called as method of proper this' );
        assert.deepEqual( stub.on.thisValues[0], $filter_box, 'on called as method of proper this' );
        assert.ok( stub.off.getCall( 0 ).calledWithExactly( "change", "input"  ), 'off called with args' );
        assert.ok( stub.on.getCall( 0 ).calledWithExactly( "change", "input" , filter_handler ), 
                                                                                    ' on called with proper args' );

        assert.equal( res, undefined, 'appendFilterListeners should return undefined' );
    });
    QUnit.test( 'appendFilterListeners functional', function ( assert ) {
        expect( 34 );

        var $filter_box_input = $( "#filter_box input" );

        stub.filter_handler = sinon.stub( window, "filter_handler" );

    	appendFilterListeners();

        $filter_box_input.each( function( i ) {
            $( this ).trigger( 'change' );
            assert.equal( stub.filter_handler.callCount, i+1, 'filter_handler should be called '+(i+1)+' times' );
            assert.deepEqual( stub.filter_handler.thisValues[i], this, 'filter_handler called as method of proper this' );
        });

    });
} );
//=============================================================================
QUnit.module( "users_browtab_filter Filtering data", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        // global vars:
        users_browtab_filter_document_ready_handler();
        qs_TR_arr        = [ 'qs_TR_arr' ];
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'applyFilter', function ( assert ) {
        expect( 18 );

        // expected values:
        var qsTRarr = [ 'qsTRarr' ];
        var filtval = { 'filtval': 0 };
        
        stub.restore_data           = sinon.stub( window, "restore_data" );
        stub.get_filters            = sinon.stub( window, "get_filters" ).returns( filtval );
        stub.filter_table           = sinon.stub( window, "filter_table" ).returns( qsTRarr );
        stub.display_qs_TR_arr      = sinon.stub( window, "display_qs_TR_arr" );
        stub.display_records_info   = sinon.stub( window, "display_records_info" );

        var res = applyFilter( );

        assert.ok( stub.get_filters         .calledAfter( stub.restore_data         ), 'call sequence check');
        assert.ok( stub.filter_table        .calledAfter( stub.get_filters          ), 'call sequence check');
        assert.ok( stub.display_qs_TR_arr   .calledAfter( stub.filter_table         ), 'call sequence check');
        assert.ok( stub.display_records_info.calledAfter( stub.display_qs_TR_arr    ), 'call sequence check');

        assert.ok( stub.restore_data.calledOnce, 'restore_data should be called once' );
        assert.ok( stub.restore_data.calledWithExactly( ), 'restore_data should be called with arg' );
        assert.ok( stub.get_filters.calledOnce, 'get_filters should be called once' );
        assert.ok( stub.get_filters.calledWithExactly( ), 'get_filters should be called with arg' );
        assert.ok( stub.filter_table.calledOnce, 'filter_table should be called once' );
        assert.deepEqual( stub.filter_table.args[0], [ [ 'qs_TR_arr' ] ], 'filter_table should be called with arg' );
        assert.ok( stub.display_qs_TR_arr.calledOnce, 'display_qs_TR_arr should be called once' );
        assert.ok( stub.display_qs_TR_arr.calledWithExactly( ), 'display_qs_TR_arr should be called with arg' );
        assert.ok( stub.display_records_info.calledOnce, 'display_records_info should be called once' );
        assert.ok( stub.display_records_info.calledWithExactly( ), 'display_records_info should be called with arg' );

        assert.deepEqual( filt_val, filtval, 'applyFilter should set proper value to global var' );
        assert.deepEqual( qs_TR_arr, qsTRarr, 'applyFilter should set proper value to global var' );
        assert.deepEqual( rowsNumber, 1, 'applyFilter should set proper value to global var' );

        assert.equal( res, undefined, 'applyFilter should return undefined' );
    });
    QUnit.test( 'cancelFilter', function ( assert ) {
        expect( 9 );

        stub.restore_data           = sinon.stub( window, "restore_data" );
        stub.display_qs_TR_arr      = sinon.stub( window, "display_qs_TR_arr" );
        stub.display_records_info   = sinon.stub( window, "display_records_info" );

        var res = cancelFilter( );

        assert.ok( stub.display_qs_TR_arr   .calledAfter( stub.restore_data         ), 'call sequence check');
        assert.ok( stub.display_records_info.calledAfter( stub.display_qs_TR_arr    ), 'call sequence check');

        assert.ok( stub.restore_data.calledOnce, 'restore_data should be called once' );
        assert.ok( stub.restore_data.calledWithExactly( ), 'restore_data should be called with arg' );
        assert.ok( stub.display_qs_TR_arr.calledOnce, 'display_qs_TR_arr should be called once' );
        assert.ok( stub.display_qs_TR_arr.calledWithExactly( ), 'display_qs_TR_arr should be called with arg' );
        assert.ok( stub.display_records_info.calledOnce, 'display_records_info should be called once' );
        assert.ok( stub.display_records_info.calledWithExactly( ), 'display_records_info should be called with arg' );

        assert.equal( res, undefined, 'cancelFilter should return undefined' );
    });
    QUnit.test( 'restore_data', function ( assert ) {
        expect( 9 );

        orderAsc[77] = 55;
        // expected values:
        var qsTRarr = [ 'qsTRarr' ];
        
        stub.get_ordered_col    = sinon.stub( window, "get_ordered_col" ).returns( 77 );
        stub.restore_qs_TR_arr  = sinon.stub( window, "restore_qs_TR_arr" );
        stub.sort_table         = sinon.stub( window, "sort_table" ).returns( qsTRarr );

        var res = restore_data( );

        assert.ok( stub.restore_qs_TR_arr   .calledAfter( stub.get_ordered_col    ), 'call sequence check');
        assert.ok( stub.sort_table          .calledAfter( stub.restore_qs_TR_arr  ), 'call sequence check');

        assert.ok( stub.get_ordered_col.calledOnce, 'get_ordered_col should be called once' );
        assert.ok( stub.get_ordered_col.calledWithExactly( ), 'get_ordered_col should be called with arg' );
        assert.ok( stub.restore_qs_TR_arr.calledOnce, 'restore_qs_TR_arr should be called once' );
        assert.ok( stub.restore_qs_TR_arr.calledWithExactly( ), 'restore_qs_TR_arr should be called with arg' );
        assert.ok( stub.sort_table.calledOnce, 'sort_table should be called once' );
        assert.deepEqual( stub.sort_table.args[0], [ [ 'qs_TR_arr' ], 77, 55 ], 'sort_table should be called with arg' );

        assert.equal( res, undefined, 'restore_data should return undefined' );
    });
} );
//=============================================================================
QUnit.module( "users_browtab_filter functions", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        users_browtab_filter_document_ready_handler();
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'display_records_info', function ( assert ) {
        expect( 7 );
        rowsNumber = 5;
        rowsNumber_start = 20;
        
        stub.show = sinon.spy( jQuery.prototype, "show" );
        stub.text = sinon.spy( jQuery.prototype, "text" );

        var res = display_records_info( );

        assert.equal( stub.show.callCount, 1, 'show should be called 12+1 times' );
        assert.deepEqual( stub.show.thisValues[0], $( "#records_info_box" ), 'show called as method of proper this' );
        assert.deepEqual( stub.show.args[0], [ ], 'show should be called with arg' );

        assert.equal( stub.text.callCount, 1, 'text should be called 12+1 times' );
        assert.deepEqual( stub.text.thisValues[0], $( "#records_info" ), 'text called as method of proper this' );
        assert.deepEqual( stub.text.args[0], [ "5 / 20" ], 'text should be called with arg' );

        assert.equal( res, undefined, 'display_records_info should return undefined' );
    });
    QUnit.test( 'clearFilterFields', function ( assert ) {
        expect( 4 );

        stub.val                = sinon.spy( jQuery.prototype, "val" );

        var res = clearFilterFields( );

        assert.equal( stub.val.callCount, 13, 'val should be called 12+1 times' );
        assert.deepEqual( stub.val.args[0], [ ['all'] ], 'val should be called with arg' );
        assert.deepEqual( stub.val.thisValues[0], $( "input:radio" ), 'val called as method of proper this' );

        assert.equal( res, undefined, 'clearFilterFields should return undefined' );
    });
    QUnit.test( 'get_filters', function ( assert ) {
        expect( 8 );

        // expected values:
        var dict = { 
            is_recognized:   "none", 
            is_active:       "true", 
            has_members:     "all", 
            date_joined_all: "no" 
        };
        // set values to html:        
        var sel_patt = "#filter_box input:radio[name=<>]";
        var i, selector, n;
        for ( i in radio_names ) {
            n = radio_names[i];
            selector = sel_patt.replace( '<>', n );
            $( selector ).val( dict[n] );
        }
        var date1 = 'date1';
        var date2 = 'date2';

        stub.val            = sinon.spy( jQuery.prototype, "val" );
        stub.get_iso_field  = sinon.stub( window, "get_iso_field" );
        stub.get_iso_field.onCall( 0 ).returns( date1 );
        stub.get_iso_field.onCall( 1 ).returns( date2 );

        var res = get_filters( );

        assert.equal( stub.val.callCount, 4, 'val should be called 4 times' );
        assert.ok( stub.val.calledWithExactly(), 'val should be called with arg' );
//        assert.deepEqual( stub.val.thisValues[0], $( "input:radio" ), 'val called as method of proper this' );
        assert.equal( stub.get_iso_field.callCount, 2, 'get_iso_field should be called 2 times' );
        assert.deepEqual( stub.get_iso_field.args[0], [ "iso_", "#date_joined_from" ], 
                                                                    '0 get_iso_field should be called with arg' );
        assert.deepEqual( stub.get_iso_field.args[1], [ "iso_", "#date_joined_to" ], 
                                                                    '1 get_iso_field should be called with arg' );

        assert.deepEqual( date_joined_from, date1, 'cancelFilter should set proper value to global var' );
        assert.deepEqual( date_joined_to, date2, 'cancelFilter should set proper value to global var' );

        assert.deepEqual( res, dict, 'get_filters should return proper values' );
    });
    QUnit.test( 'get_iso_field v=""', function ( assert ) {
        expect( 4 );

        var iso          = "iso_";
        var selector     = "#date_joined_from";
        var iso_selector = "#iso_date_joined_from";
        var v            = "";
        var iso_v        = "";
        
        stub.val = sinon.stub( jQuery.prototype, "val" );
        stub.val.onCall( 0 ).returns( v );
        stub.val.onCall( 1 ).returns( iso_v );

        var res = get_iso_field( iso, selector );

        assert.equal( stub.val.callCount, 1, 'val should be called 1 times' );
        assert.deepEqual( stub.val.args[0], [], '0 val should be called with arg' );
        assert.deepEqual( stub.val.thisValues[0], $( selector ), '0 val called as method of proper this' );

        assert.deepEqual( res, iso_v, 'get_iso_field should return proper values' );
    });
    QUnit.test( 'get_iso_field !v', function ( assert ) {
        expect( 4 );

        var iso          = "iso_";
        var selector     = "#date_joined_from";
        var iso_selector = "#iso_date_joined_from";
        var v            = undefined;
        var iso_v        = "";
        
        stub.val = sinon.stub( jQuery.prototype, "val" );
        stub.val.onCall( 0 ).returns( v );
        stub.val.onCall( 1 ).returns( iso_v );

        var res = get_iso_field( iso, selector );

        assert.equal( stub.val.callCount, 1, 'val should be called 1 times' );
        assert.deepEqual( stub.val.args[0], [], '0 val should be called with arg' );
        assert.deepEqual( stub.val.thisValues[0], $( selector ), '0 val called as method of proper this' );

        assert.deepEqual( res, iso_v, 'get_iso_field should return proper values' );
    });
} );
//=============================================================================
//=============================================================================
QUnit.module( "users_browtab_filter filter_table", function( hooks ) { 
    var arr;
    hooks.beforeEach( function( assert ) {
        stub = {};
        arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012-12-01',     true,     true,  true],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    true,  true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     true,  true],
                [{3:3},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, true],
                [{4:4},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, true],
                [{5:5},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, true],
                [{6:6},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, false],
                [{7:7},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, false],
                [{8:8},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, false],
                [{9:0},'beta', 'abc', '1', 'eEe', '2012-12-01T16',  true,     true,  true],
                [{9:1},'Beta', 'bbc', '15','EeE', '',               false,    true,  true],
                [{9:2},'alfa', 'aBc', '2', 'bBb', '',               null,     true,  true]
        ];
        date_joined_from = undefined;
        date_joined_to   = undefined;
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    //-----------------------------------------------------------------
    QUnit.test( '#1 all', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "all", 
            is_active:       "all", 
            has_members:     "all", 
            date_joined_all: "all" 
        };
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012-12-01',     true,     true,  true],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    true,  true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     true,  true],
                [{3:3},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, true],
                [{4:4},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, true],
                [{5:5},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, true],
                [{6:6},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, false],
                [{7:7},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, false],
                [{8:8},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, false],
                [{9:0},'beta', 'abc', '1', 'eEe', '2012-12-01T16',  true,     true,  true],
                [{9:1},'Beta', 'bbc', '15','EeE', '',               false,    true,  true],
                [{9:2},'alfa', 'aBc', '2', 'bBb', '' ,             null,     true,  true]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( '#2 is_recognized=yes', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "yes", 
            is_active:       "all", 
            has_members:     "all", 
            date_joined_all: "all" 
        };
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012-12-01',     true,     true,  true],
                [{3:3},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, true],
                [{6:6},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, false],
                [{9:0},'beta', 'abc', '1', 'eEe', '2012-12-01T16',  true,     true,  true]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    QUnit.test( '#3 is_recognized=none', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "none", 
            is_active:       "all", 
            has_members:     "all", 
            date_joined_all: "all" 
        };
        var expected_arr = [
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     true,  true],
                [{5:5},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, true],
                [{8:8},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, false],
                [{9:2},'alfa', 'aBc', '2', 'bBb', '' ,             null,     true,  true]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    QUnit.test( '#4 is_recognized=no', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "no", 
            is_active:       "all", 
            has_members:     "all", 
            date_joined_all: "all" 
        };
        var expected_arr = [
                [{1:1},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    true,  true],
                [{4:4},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, true],
                [{7:7},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, false],
                [{9:1},'Beta', 'bbc', '15','EeE', '',               false,    true,  true]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( '#5 is_active=yes', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "all", 
            is_active:       "yes", 
            has_members:     "all", 
            date_joined_all: "all" 
        };
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012-12-01',     true,     true,  true],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    true,  true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     true,  true],
                [{9:0},'beta', 'abc', '1', 'eEe', '2012-12-01T16',  true,     true,  true],
                [{9:1},'Beta', 'bbc', '15','EeE', '',               false,    true,  true],
                [{9:2},'alfa', 'aBc', '2', 'bBb', '' ,             null,     true,  true]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    QUnit.test( '#6 is_active=no', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "all", 
            is_active:       "no", 
            has_members:     "all", 
            date_joined_all: "all" 
        };
        var expected_arr = [
                [{3:3},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, true],
                [{4:4},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, true],
                [{5:5},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, true],
                [{6:6},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, false],
                [{7:7},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, false],
                [{8:8},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, false]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( '#7 has_members=yes', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "all", 
            is_active:       "all", 
            has_members:     "yes", 
            date_joined_all: "all" 
        };
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012-12-01',     true,     true,  true],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    true,  true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     true,  true],
                [{3:3},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, true],
                [{4:4},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, true],
                [{5:5},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, true],
                [{9:0},'beta', 'abc', '1', 'eEe', '2012-12-01T16',  true,     true,  true],
                [{9:1},'Beta', 'bbc', '15','EeE', '',               false,    true,  true],
                [{9:2},'alfa', 'aBc', '2', 'bBb', '' ,             null,     true,  true]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    QUnit.test( '#8 has_members=no', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "all", 
            is_active:       "all", 
            has_members:     "no", 
            date_joined_all: "all" 
        };
        var expected_arr = [
                [{6:6},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, false],
                [{7:7},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, false],
                [{8:8},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, false]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    //-----------------------------------------------------------------
    QUnit.test( '#9 date_joined_all=no date_joined_from=undefined date_joined_to=undefined', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "all", 
            is_active:       "all", 
            has_members:     "all", 
            date_joined_all: "no" 
        };
        date_joined_from = undefined;
        date_joined_to   = undefined;
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012-12-01',     true,     true,  true],
                [{1:1},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    true,  true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     true,  true],
                [{3:3},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, true],
                [{4:4},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, true],
                [{5:5},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, true],
                [{6:6},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, false],
                [{7:7},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, false],
                [{8:8},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, false],
                [{9:0},'beta', 'abc', '1', 'eEe', '2012-12-01T16',  true,     true,  true],
                [{9:1},'Beta', 'bbc', '15','EeE', '',               false,    true,  true],
                [{9:2},'alfa', 'aBc', '2', 'bBb', '' ,             null,     true,  true]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    QUnit.test( '#10 date_joined_all=no date_joined_from=... date_joined_to=undefined', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "all", 
            is_active:       "all", 
            has_members:     "all", 
            date_joined_all: "no" 
        };
        date_joined_from = "2011-11-01";
        date_joined_to   = undefined;
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012-12-01',     true,     true,  true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     true,  true],
                [{5:5},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, true],
                [{8:8},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, false],
                [{9:0},'beta', 'abc', '1', 'eEe', '2012-12-01T16',  true,     true,  true]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    QUnit.test( '#11 date_joined_all=no date_joined_from=undefined date_joined_to=...', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "all", 
            is_active:       "all", 
            has_members:     "all", 
            date_joined_all: "no" 
        };
        date_joined_from = undefined;
        date_joined_to   = "2011-12-31";
        var expected_arr = [
                [{1:1},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    true,  true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     true,  true],
                [{3:3},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, true],
                [{4:4},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, true],
                [{5:5},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, true],
                [{6:6},'beta', 'abc', '1', 'eEe', '2009-09-01',     true,     false, false],
                [{7:7},'Beta', 'bbc', '15','EeE', '2010-10-01',     false,    false, false],
                [{8:8},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, false],
                [{9:1},'Beta', 'bbc', '15','EeE', '',               false,    true,  true],
                [{9:2},'alfa', 'aBc', '2', 'bBb', '' ,             null,     true,  true]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    QUnit.test( '#12 date_joined_all=no date_joined_from=... date_joined_to=...', function ( assert ) {
        expect( 1 );
        filt_val = { 
            is_recognized:   "all", 
            is_active:       "all", 
            has_members:     "all", 
            date_joined_all: "no" 
        };
        date_joined_from = "2011-11-01";
        date_joined_to   = "2012-12-31";
        var expected_arr = [
                [{0:0},'beta', 'abc', '1', 'eEe', '2012-12-01',     true,     true,  true],
                [{2:2},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     true,  true],
                [{5:5},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, true],
                [{8:8},'alfa', 'aBc', '2', 'bBb', '2011-11-01',     null,     false, false],
                [{9:0},'beta', 'abc', '1', 'eEe', '2012-12-01T16',  true,     true,  true]
        ];
        var res = filter_table( arr );
        assert.deepEqual( res, expected_arr, 'filter_table should return proper value' );
    });
    //-----------------------------------------------------------------
} );
//=============================================================================
QUnit.module( "users_browtab_filter date fields", function( hooks ) { 
    var $inputs;
    hooks.beforeEach( function( assert ) {
        stub = {};
        $inputs = [
            $( "#date_joined_from"  ),
            $( "#date_joined_to" )
        ];
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'appendDateFields', function ( assert ) {
        expect( 8 );

        var defaults = {
            altFormat:          "yy-mm-dd",
            buttonImageOnly:    true,
            buttonImage:        "/static/admin/img/icon_calendar.gif",
    		dateFormat:			"dd.mm.yy",
    		gotoCurrent: 		true,
            numberOfMonths:     1,
            regional:           "uk",
            selectOtherMonths:  true,
            showOn:             "button",
            showOtherMonths:    true
        };
        var arg_from = {
            altField: 	 '#iso_date_joined_from', 
            defaultDate: "-1w"
        };
        var arg_to = {
            altField: 	 '#iso_date_joined_to', 
            defaultDate: ""
        };

        stub.datepicker = sinon.spy( jQuery.prototype, "datepicker" );
        stub.setDefaults = sinon.stub( $.datepicker, "setDefaults" );

        var res = appendDateFields( );

        assert.equal( stub.setDefaults.callCount, 1, 'setDefaults should be called 1 times' );
        assert.deepEqual( stub.setDefaults.args[0], [ defaults ], 'setDefaults should be called with args' );
        assert.equal( stub.datepicker.callCount, 2, 'datepicker should be called 2 times' );
        assert.deepEqual( stub.datepicker.args[0][0], arg_from, '0 datepicker args' );
        assert.deepEqual( stub.datepicker.args[1][0], arg_to, '1 datepicker args' );
        var i;
        for ( i = 0; i < 2; i++ ){
            assert.deepEqual( stub.datepicker.thisValues[i], $inputs[i], i+': datepicker called as method of proper this' );
        }

        assert.equal( res, undefined, 'appendDateFields should return undefined' );
    });
    QUnit.test( 'appendDateFieldsListeners', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 11 );

        stub.off = sinon.spy( jQuery.prototype, "off" );
        stub.on  = sinon.spy( jQuery.prototype, "on" );

        var res = appendDateFieldsListeners( );

        assert.equal( stub.off.callCount, 2, 'off should be called 2 times' );
        assert.equal( stub.on.callCount, 2, 'on should be called 2 times' );

        var i;
        for ( i = 0; i < 2; i++ ){
            assert.deepEqual( stub.off.thisValues[i], $inputs[i], i+': off called as method of proper this' );
            assert.deepEqual( stub.on.thisValues[i], $inputs[i], i+': on called as method of proper this' );
            assert.ok( stub.off.getCall( i ).calledWithExactly( "change" ), i+':off called with args' );
            assert.ok( stub.on.getCall( i ).calledWithExactly( "change", dateFieldListener ), 
                                                                                    i+': on called with proper args' );
        }
        assert.equal( res, undefined, 'appendDateFieldsListeners should return undefined' );
    });
    QUnit.test( 'appendDateFieldsListeners functional', function ( assert ) {
        expect( 1 );

        var i;
        stub.dateFieldListener = sinon.stub( window, "dateFieldListener" );

    	appendDateFields();
    	appendDateFieldsListeners();

        for ( i = 0; i < 2; i++ ){
            $inputs[i].trigger( 'change' );
        }
        assert.ok( stub.dateFieldListener.calledTwice, 'dateFieldListener should be called twice' );
    });
    QUnit.test( 'dateFieldListener functional', function ( assert ) {
        expect( 12 );

        var date = '01.02.2016';
        var iso_date = '2016-02-01';
        var fail_date = '01022016';
        var i;
        var altField;

    	appendDateFields();
    	appendDateFieldsListeners();

        for ( i = 0; i < 2; i++ ){
	        altField = $inputs[i].datepicker( "option", "altField" );

	        // send correct date
            $inputs[i].val( date );
            $( altField ).val( iso_date );
            dateFieldListener.apply( $inputs[i] );
            assert.equal( $( altField ).val(), iso_date, ': datepicker send correct date to alt field' );
            assert.notOk( $inputs[i].hasClass ( "error" ), 'dateFieldListener clear error class in date field' );

	        // send fail date
            $inputs[i].val( fail_date );
//            $( altField ).val( iso_date );
            dateFieldListener.apply( $inputs[i] );
            assert.equal( $( altField ).val(), "", ': dateFieldListener clear alt field' );
            assert.ok( $inputs[i].hasClass ( "error" ), 'dateFieldListener add error class in date field' );

	        // send correct date once more
            $inputs[i].val( date );
            $( altField ).val( iso_date );
            dateFieldListener.apply( $inputs[i] );
            assert.equal( $( altField ).val(), iso_date, ': datepicker send correct date to alt field' );
            assert.notOk( $inputs[i].hasClass ( "error" ), 'dateFieldListener clear error class in date field' );
         }
    });
    QUnit.test( 'clearDateFields functional', function ( assert ) {
        expect( 9 );

        var date = '01.02.2016';
        var iso_date = '2016-02-01';
        var i, v;
        var altField;

    	appendDateFields();
    	appendDateFieldsListeners();

        for ( i = 0; i < 2; i++ ){
	        altField = $inputs[i].datepicker( "option", "altField" );
            $inputs[i].val( date );
            $( altField ).val( iso_date );
         }
        for ( i = 0; i < 2; i++ ){
	        altField = $inputs[i].datepicker( "option", "altField" );
            assert.equal( $inputs[i].val(), date, 'value should be set to html before test' );
            assert.equal( $( altField ).val(), iso_date, 'value should be set to html before test' );
         }
        var res = clearDateFields( );

        $( ".date-input input" ).each( function( i ) {
            v = $( this ).val();
            assert.equal( v, "", i+': clearDateFields set "" to field' );
        });

        assert.equal( res, undefined, 'clearDateFields should return undefined' );
    });
} );
//=============================================================================

//=============================================================================
QUnit.module( "users_browtab_filter filter handler", function( hooks ) { 
    var $checkbox;
    hooks.beforeEach( function( assert ) {
        stub = {};
        stub.applyFilter = sinon.stub( window, "applyFilter" );
        stub.cancelFilter = sinon.stub( window, "cancelFilter" );

        $checkbox = $( '#id_apply_filters' );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'filter_handler true', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 3 );
         
        $checkbox.prop('checked', true );

        var res = filter_handler.apply( $checkbox );

        assert.equal( stub.applyFilter.callCount, 1, 'applyFilter should be called 1 times' );
        assert.equal( stub.cancelFilter.callCount, 0, 'cancelFilter should be called 0 times' );

        assert.equal( res, undefined, 'filter_handler should return undefined' );
    });
    QUnit.test( 'filter_handler false', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 3 );
         
        $checkbox.prop('checked', false );

        var res = filter_handler.apply( $checkbox );

        assert.equal( stub.applyFilter.callCount, 0, 'applyFilter should be called 0 times' );
        assert.equal( stub.cancelFilter.callCount, 1, 'cancelFilter should be called 1 times' );

        assert.equal( res, undefined, 'filter_handler should return undefined' );
    });
    QUnit.test( 'filter_handler functional', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 4 );

        appendFilterListeners();

        $checkbox.prop( 'checked', true );
        $checkbox.trigger( 'change' );

        assert.equal( stub.applyFilter.callCount, 1, 'applyFilter should be called 1 times' );
        assert.equal( stub.cancelFilter.callCount, 0, 'cancelFilter should be called 0 times' );

        $checkbox.prop( 'checked', false );
        $checkbox.trigger( 'change' );

        assert.equal( stub.applyFilter.callCount, 1, 'applyFilter should be called still 1 times' );
        assert.equal( stub.cancelFilter.callCount, 1, 'cancelFilter now should be called 1 times' );
    });
} );
//=============================================================================
