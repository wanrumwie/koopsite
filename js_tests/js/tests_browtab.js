/*
Global:  $ (?), JSON (?), QUnit (?), TR_start (?), auxiliary_handler, browtab_document_ready_handler (?), changeSelElement (?), columnsNumber, create_qs_TR_arr (?), deleteElement (?), display_qs_TR_arr (?), expect (?), getRowIndexbyID (?), getSelRowIndexLimited (?), getSelectorTR (?), getTRbyID (?), getTRbyIndex (?), getTRfromTbodyByIndex (?), getVisibleIndex (?), get_m_id_n_ByIndex (?), get_qs_TR_arr (?), markSelRow (?), normalStyle (?), onClick_handler (?), onDblclick_handler (?), onKeyDown (?), onKeydown_handler (?), qs_TR_arr (?), restore_qs_TR_arr (?), rowsNumber (?), scrollToRow (?), selElement (?), selRowFocus (?), selRowIndex (?), selTR (?), selectRow (?), selectStyle (?), setSelRow (?), setStartRow (?), setValToHTML, setValToHTMLrow (?), set_browtab_listeners (?), sinon (?), storeSelRowIndex (?), stub, totalOuterHeight (?), window (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

//=============================================================================
QUnit.module( "browtab document ready", function( hooks ) { 
    var tbody_selector;
    var target_selector;
    hooks.beforeEach( function( assert ) {
        stub = {};
        target_selector = "#td_qwerty";
        tbody_selector  = "#browtable tbody";
        // $tbody          = $( tbody_selector );
		browtab_document_ready_handler( );
        // set_browtab_listeners(); 
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'browtab_document_ready_handler', function ( assert ) {
        expect( 7 );
        stub.set_browtab_listeners = sinon.stub( window, "set_browtab_listeners" );
        var res = browtab_document_ready_handler( );
        assert.ok( stub.set_browtab_listeners.calledOnce, 'set_browtab_listeners should be called once' );
        assert.ok( stub.set_browtab_listeners.calledWithExactly( ), 'set_browtab_listeners should be called with arg' );

		assert.deepEqual( TR_start, [], 'array for storing <tr> data immediately after page loaded');
		assert.deepEqual( selElement, {}, 'object = selElement.model , selElement.id , selElement.name');
		assert.equal( selectStyle, "selected", 'CSS style for selected row');
		assert.equal( normalStyle, "normal", 'CSS style for unselected row');

        assert.equal( res, undefined, 'browtab_document_ready_handler should return false' );
    });
    QUnit.test( 'set_browtab_listeners', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon,stub
        expect( 9 );

        stub.off = sinon.spy( $tbody, "off" );
        stub.on  = sinon.spy( $tbody, "on" );

        var res = set_browtab_listeners( $tbody );

        assert.ok( stub.off.calledThrice, 'off should be called thrice' );
        assert.ok( stub.on.calledThrice, 'on should be called thrice' );

        assert.ok( stub.off.getCall( 0 ).calledWithExactly( "click",    "td" ), '0 off should be called with arg' );
        assert.ok( stub.off.getCall( 1 ).calledWithExactly( "dblclick", "td" ), '1 off should be called with arg' );
        assert.ok( stub.off.getCall( 2 ).calledWithExactly( "keydown",  "td" ), '2 off should be called with arg' );

        assert.ok( stub.on.getCall( 0 ).calledWithExactly( "click",    "td", onClick_handler ), 
                                                                                '0 on should be called with arg' );
        assert.ok( stub.on.getCall( 1 ).calledWithExactly( "dblclick", "td", onDblclick_handler ), 
                                                                                '1 on should be called with arg' );
        assert.ok( stub.on.getCall( 2 ).calledWithExactly( "keydown",  "td", onKeydown_handler ), 
                                                                                '2 on should be called with arg' );

        assert.equal( res, undefined, 'set_browtab_listeners should return false' );
    });
    QUnit.test( 'onClick_handler', function ( assert ) {
        expect( 3 );
        var e = {                               // e is needed as onClick argument
            currentTarget: sinon.stub()
        };
        stub.selectRow = sinon.stub( window, "selectRow" );
        var res = onClick_handler( e );
        assert.ok( stub.selectRow.calledOnce, 'selectRow should be called once' );
        assert.ok( stub.selectRow.calledWithExactly( e.currentTarget ), 'selectRow should be called with arg' );
        assert.equal( res, false, 'onClick_handler should return false' );
    });
    QUnit.test( '$( ... ).on( "click",... STUB selectRow', function ( assert ) {
        expect( 1 );
        stub.selectRow = sinon.stub( window, "selectRow" );
        $( target_selector ).trigger( 'click' );
        assert.ok( stub.selectRow.calledOnce, 'selectRow should be called once' );
    });
    QUnit.test( 'onDblclick_handler', function ( assert ) {
        expect( 5 );
        var e = {                               // e is needed as onClick argument
            currentTarget: sinon.stub()
        };
        stub.selectRow = sinon.stub( window, "selectRow" );
        stub.runhref = sinon.stub( window, "runhref" );
        var res = onDblclick_handler( e );
        assert.ok( stub.selectRow.calledOnce, 'selectRow should be called once' );
        assert.ok( stub.selectRow.calledWithExactly( e.currentTarget ), 'selectRow should be called with arg' );
        assert.ok( stub.runhref.calledOnce, 'runhref should be called once' );
        assert.ok( stub.runhref.calledWithExactly(), 'runhref should be called with no arg' );
        assert.equal( res, false, 'onDblclick_handler should return false' );
    });
    QUnit.test( '$( ... ).on( "dblclick",... STUB called func.', function ( assert ) {
        expect( 2 );
        stub.selectRow = sinon.stub( window, "selectRow" );
        stub.runhref = sinon.stub( window, "runhref" );
        $( target_selector ).trigger( 'dblclick' );
        assert.ok( stub.selectRow.calledOnce, 'selectRow should be called once' );
        assert.ok( stub.runhref.calledOnce, 'runhref should be called once' );
    });
    QUnit.test( 'onKeydown_handler', function ( assert ) {
        expect( 3 );
        var e = {                               // e is needed as onClick argument
            which: sinon.stub()
        };
        stub.onKeyDown = sinon.stub( window, "onKeyDown" );
        var res = onKeydown_handler( e );
        assert.ok( stub.onKeyDown.calledOnce, 'onKeyDown should be called once' );
        assert.ok( stub.onKeyDown.calledWithExactly( e.which ), 'onKeyDown should be called with arg' );
        assert.equal( res, false, 'onKeydown_handler should return false' );
    });
    QUnit.test( '$( ... ).on( "keydown",... STUB onKeyDown', function ( assert ) {
        expect( 1 );
        stub.onKeyDown = sinon.stub( window, "onKeyDown" );
        $( target_selector ).trigger( $.Event( "keydown", { keyCode: 9 } ) );
        assert.ok( stub.onKeyDown.calledOnce, 'onKeyDown should be called once' );
    });
} );
/*  It's impossible to stub function inside on():  $( ... ).on( ..., onClick_handler ) ?
QUnit.test( '$( ... ).on( "click",... STUB onClick_handler', function ( assert ) {
    stub = sinon.stub( window, "onClick_handler" );
    $( target_selector ).trigger( 'click' );
    assert.equal( stub.calledOnce, true, 'onClick_handler should be called once' );
});
*/
//=============================================================================
QUnit.module( "browtab sel row functions", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
		browtab_document_ready_handler( );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'setStartRow', function ( assert ) {
        expect( 6 );
        stub.setSelRow = sinon.stub( window, "setSelRow" );
        $( "#selRowIndex" ).val( 55 );
        var res = setStartRow();
        assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
        assert.ok( stub.setSelRow.calledWithExactly( 55 ), 'selectRow should be called with arg' );
        assert.equal( res, undefined, 'setStartRow should return undefined' );

        stub.setSelRow.reset();
        $( "#selRowIndex" ).val( "" );
        res = setStartRow();
        assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
        assert.ok( stub.setSelRow.calledWithExactly( 0 ), 'selectRow should be called with arg' );
        assert.equal( res, undefined, 'setStartRow should return undefined' );
    });
    QUnit.test( 'setSelRow', function ( assert ) {
        expect( 10 );
        rowsNumber = 10;
        var i = 1;
        var expected_setTR = { '0':0 };
        stub.getSelRowIndexLimited = sinon.spy( window, "getSelRowIndexLimited" );
        stub.getTRbyIndex   = sinon.stub( window, "getTRbyIndex" ).returns( expected_setTR );
        stub.scrollToRow    = sinon.stub( window, "scrollToRow" );
        stub.markSelRow     = sinon.stub( window, "markSelRow" );
        var res = setSelRow( i );
        assert.ok( stub.getSelRowIndexLimited.calledOnce, 'getSelRowIndexLimited should be called once' );
        assert.ok( stub.getSelRowIndexLimited.calledWithExactly( i ), 'getSelRowIndexLimited should be called with arg' );
        assert.ok( stub.getTRbyIndex.calledOnce, 'getTRbyIndex should be called once' );
        assert.ok( stub.getTRbyIndex.calledWithExactly( selRowIndex ), 'getTRbyIndex should be called with arg' );
        assert.ok( stub.scrollToRow.calledOnce, 'scrollToRow should be called once' );
        assert.ok( stub.scrollToRow.calledWithExactly( selRowIndex ), 'scrollToRow should be called with arg' );
        assert.ok( stub.markSelRow.calledOnce, 'markSelRow should be called once' );
        assert.ok( stub.markSelRow.calledWithExactly(), 'markSelRow should be called with arg' );
        assert.equal( selTR, expected_setTR, 'setSelRow should set selTR value' );
        assert.equal( res, undefined, 'setSelRow should return undefined' );
    });
    QUnit.test( 'setSelRow rowsNumber=0', function ( assert ) {
        expect( 7 );
        rowsNumber = 0;
        var i = 1;
        var expected_setTR = selTR;
        stub.getSelRowIndexLimited = sinon.spy( window, "getSelRowIndexLimited" );
        stub.getTRbyIndex   = sinon.stub( window, "getTRbyIndex" ).returns( expected_setTR );
        stub.scrollToRow    = sinon.stub( window, "scrollToRow" );
        stub.markSelRow     = sinon.stub( window, "markSelRow" );
        var res = setSelRow( i );
        assert.ok( stub.getSelRowIndexLimited.calledOnce, 'getSelRowIndexLimited should be called once' );
        assert.ok( stub.getSelRowIndexLimited.calledWithExactly( i ), 'getSelRowIndexLimited should be called with arg' );
        assert.notOk( stub.getTRbyIndex.called, 'getTRbyIndex should not be called' );
        assert.notOk( stub.scrollToRow.called, 'scrollToRow should not be called' );
        assert.notOk( stub.markSelRow.called, 'markSelRow should not be called' );
        assert.equal( selTR, expected_setTR, 'setSelRow should not change selTR value' );
        assert.equal( res, undefined, 'setSelRow should return undefined' );
    });
    QUnit.test('getSelRowIndexLimited', function ( assert ) {
        expect( 7 );
        rowsNumber = 10;
        assert.strictEqual( getSelRowIndexLimited( -1 ), 0, 'sel row index min value must be 0');
        assert.strictEqual( getSelRowIndexLimited(  0 ), 0, 'sel row index must be = 0');
        assert.strictEqual( getSelRowIndexLimited(  5 ), 5, 'sel row index must be = 5');
        assert.strictEqual( getSelRowIndexLimited( rowsNumber ), rowsNumber - 1, 
                                                        'sel row index max value must be rowsNumber-1');
        rowsNumber = 0;
        assert.strictEqual( getSelRowIndexLimited( -1 ), 0, 'sel row index must be 0 if rowsNumber=0');
        assert.strictEqual( getSelRowIndexLimited(  0 ), 0, 'sel row index must be 0 if rowsNumber=0');
        assert.strictEqual( getSelRowIndexLimited( 10 ), 0, 'sel row index must be 0 if rowsNumber=0');
    });
    QUnit.test('check_selRowIndex_range', function ( assert ) {
        expect( 14 );
        rowsNumber = 10;
        selRowIndex = 0;
        assert.strictEqual( check_selRowIndex_range( ), true, 'sel row index should be in range of 0.. rowsNumber');
        selRowIndex = rowsNumber - 1;
        assert.strictEqual( check_selRowIndex_range( ), true, 'sel row index should be in range of 0.. rowsNumber');
        selRowIndex = rowsNumber;
        assert.strictEqual( check_selRowIndex_range( ), false, 'sel row index should be in range of 0.. rowsNumber');
        selRowIndex = -1;
        assert.strictEqual( check_selRowIndex_range( ), false, 'sel row index should be in range of 0.. rowsNumber');
        selRowIndex = undefined;
        assert.strictEqual( check_selRowIndex_range( ), false, 'sel row index should be in range of 0.. rowsNumber');
        rowsNumber = 0;
        selRowIndex = rowsNumber;
        assert.strictEqual( check_selRowIndex_range( ), false, 'sel row index should be in range of 0.. rowsNumber');
        selRowIndex = -1;
        assert.strictEqual( check_selRowIndex_range( ), false, 'sel row index should be in range of 0.. rowsNumber');
        selRowIndex = undefined;
        assert.strictEqual( check_selRowIndex_range( ), false, 'sel row index should be in range of 0.. rowsNumber');

        rowsNumber = "10";
        selRowIndex = "0";
        assert.strictEqual( check_selRowIndex_range( ), true, 'sel row index should be in range of 0.. rowsNumber');
        rowsNumber = "10";
        selRowIndex = "5";
        assert.strictEqual( check_selRowIndex_range( ), true, 'sel row index should be in range of 0.. rowsNumber');
        rowsNumber = "10";
        selRowIndex = "";
        assert.strictEqual( check_selRowIndex_range( ), true, 'sel row index should be in range of 0.. rowsNumber');
        rowsNumber = 10;
        selRowIndex = "";
        assert.strictEqual( check_selRowIndex_range( ), true, 'sel row index should be in range of 0.. rowsNumber');
        rowsNumber = "10";
        selRowIndex = 5;
        assert.strictEqual( check_selRowIndex_range( ), true, 'sel row index should be in range of 0.. rowsNumber');
        rowsNumber = "10";
        selRowIndex = "12";
        assert.strictEqual( check_selRowIndex_range( ), false, 'sel row index should be in range of 0.. rowsNumber');
	});
    QUnit.test( 'get_thisfolder_name', function ( assert ) {
        expect( 4 );

        stub.text   = sinon.stub( jQuery.prototype, "text" ).returns('f_name');

        var res = get_thisfolder_name();

        assert.deepEqual( stub.text.thisValues[0], $( "#thisfolder span" ), 'text called as method of proper this' );
        assert.equal( stub.text.callCount, 1, 'text should be called once' );
        assert.ok( stub.text.calledWithExactly( ), 'text should be called with arg' );
        assert.equal( res, 'f_name', 'get_thisfolder_name should return proper value' );
    });
    QUnit.test('selRowFocus functional', function ( assert ) {
        expect( 4 );

        selTR = $( "#tr_qwerty_s" );
        selTR.find( 'A' ).blur();
        assert.notOk( $( "#a_qwerty_s" ).is(':focus'), 'proper <a> should not be focused before selRowFocus');

        var res = selRowFocus();

        assert.equal( res, undefined, 'selRowFocus should return undefined' );
        assert.ok( selTR.find( 'A' ).is(':focus'), 'proper <a> should be focused');
        assert.ok( $( "#tr_qwerty_s A" ).is(':focus'), 'proper <a> should be focused');
    });
    QUnit.test( 'selRowFocus', function ( assert ) {
        expect( 6 );
        selTR = $( "#tr_qwerty_s" );

        stub.find   = sinon.spy( jQuery.prototype, "find" );
        stub.focus  = sinon.spy( jQuery.prototype, "focus" );

        var res = selRowFocus();

        assert.deepEqual( stub.find.thisValues[0], $( selTR ), 'find called as method of proper this' );
        assert.equal( stub.find.callCount, 1, 'find should be called once' );
        assert.ok( stub.find.calledWithExactly( "A" ), 'find should be called with arg' );
        assert.equal( stub.focus.callCount, 1, 'focus should be called once' );
        assert.ok( stub.focus.calledWithExactly( ), 'focus should be called with arg' );
        assert.equal( res, undefined, 'selRowFocus should return undefined' );
    });
    QUnit.test('selRowFocus selTR==undefined', function ( assert ) {
        expect( 3 );

        selTR = undefined;
        assert.notOk( $( "#a_qwerty_s" ).is(':focus'), 'proper <a> should not be focused before selRowFocus');

        var res = selRowFocus();

        assert.equal( res, undefined, 'selRowFocus should return undefined' );
        assert.notOk( $( "#tr_qwerty_s A" ).is(':focus'), 'nothing should be focused');
    });
    QUnit.test( 'markSelRow', function ( assert ) {
        expect( 11 );
        selElement = undefined;
        stub.get_m_id_n_ByIndex = sinon.stub( window, "get_m_id_n_ByIndex" ).returns( { id: '0'} );
        stub.storeSelRowIndex   = sinon.stub( window, "storeSelRowIndex" );
        stub.selRowFocus        = sinon.stub( window, "selRowFocus" );
        selTR = "#tr_qwerty";
        assert.notOk( $( selTR ).is('.'+selectStyle), 'selTR should not be not selectStyled before markSelRow');
        var res = markSelRow();
        assert.notOk( $( "#tr_qwerty_s" ).is('.'+selectStyle), 
                                                        'previous selTR should not be not selectStyled after markSelRow');
        assert.ok( $( selTR ).is('.'+selectStyle), 'selTR should be selectStyled after markSelRow');
        assert.ok( stub.get_m_id_n_ByIndex.calledOnce, 'get_m_id_n_ByIndex should be called once' );
        assert.ok( stub.get_m_id_n_ByIndex.calledWithExactly( selRowIndex ), 'get_m_id_n_ByIndex should be called with arg' );
        assert.ok( stub.storeSelRowIndex.calledOnce, 'storeSelRowIndex should be called once' );
        assert.ok( stub.storeSelRowIndex.calledWithExactly(), 'storeSelRowIndex should be called with arg' );
        assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
        assert.ok( stub.selRowFocus.calledWithExactly(), 'selRowFocus should be called with arg' );
        assert.equal( res, false, 'markSelRow should return false' );
        assert.equal( selElement.id, '0', 'markSelRow should set selElement value' );
    });
    QUnit.test( 'selectRow', function ( assert ) {
        expect( 5 );
        var targ = "#td_qwerty_s";
        stub.markSelRow = sinon.stub( window, "markSelRow" );
        var res = selectRow( targ );
        assert.ok( stub.markSelRow.calledOnce, 'markSelRow should be called once' );
        assert.ok( stub.markSelRow.calledWithExactly(), 'markSelRow should be called with arg' );
        assert.equal( res, false, 'selectRow should return false' );
        assert.equal( selRowIndex, 1, 'selectRow should set selRowIndex value' );
        assert.equal( $( selTR )[0], $( "#tr_qwerty_s" )[0], 'selectRow should set selTR value' );
    //
    //    All properties of $( selTR ) object are identical with $( "#tr_qwerty_s" ) one except "selector":
    //    var prop;
    //    for ( prop in $( selTR ) ) {
    //        if ( prop != "selector" ){
    //            assert.equal( $( selTR )[prop], $( "#tr_qwerty_s" )[prop], 'selectRow should set selTR value' );
    //        }
    //    }
    //    This not works:
    //    assert.deepEqual( $( selTR ), $( "#tr_qwerty_s" ), 'selectRow should set selTR value' );
    });
} );
//=============================================================================

function auxiliary_handler(){
}
QUnit.module( "browtab storeSelRowIndex", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        $( '#selRowIndex' ).off( "change").on( "change", function() {
            auxiliary_handler();
            return false;
        });
        expect( 3 );
        stub.auxiliary_handler = sinon.stub( window, "auxiliary_handler" );
        selRowIndex = "1";
        selElement.model = 'folder';
        selElement.id = "55";
        auxiliary_set_val_to_html();
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    function auxiliary_set_val_to_html(){
        $( '#selRowIndex').val( selRowIndex );
        $( '#selElementModel' ).val( selElement.model );
        $( '#selElementID' ).val( selElement.id );
    }
    function auxiliary_get_val_from_html(){
        var ri = $( '#selRowIndex').val();
        var md = $( '#selElementModel' ).val();
        var id = $( '#selElementID' ).val();
        return [ri, md, id];
    }
    QUnit.test( '#1', function ( assert ) {
        selRowIndex = "2";
        var res = storeSelRowIndex();
        assert.equal( res, undefined, 'storeSelRowIndex should return undefined' );
        assert.deepEqual( auxiliary_get_val_from_html(),
                    [selRowIndex, selElement.model, selElement.id],
                    'storeSelRowIndex should store proper values to html' );
        assert.ok( stub.auxiliary_handler.calledOnce, 'on change handler should be called once' );
    });
    QUnit.test( '#2', function ( assert ) {
        selElement.model = 'user';
        var res = storeSelRowIndex();
        assert.equal( res, undefined, 'storeSelRowIndex should return undefined' );
        assert.deepEqual( auxiliary_get_val_from_html(),
                    [selRowIndex, selElement.model, selElement.id],
                    'storeSelRowIndex should store proper values to html' );
        assert.ok( stub.auxiliary_handler.calledOnce, 'on change handler should be called once' );
    });
    QUnit.test( '#3', function ( assert ) {
        selElement.id = '77';
        var res = storeSelRowIndex();
        assert.equal( res, undefined, 'storeSelRowIndex should return undefined' );
        assert.deepEqual( auxiliary_get_val_from_html(),
                    [selRowIndex, selElement.model, selElement.id],
                    'storeSelRowIndex should store proper values to html' );
        assert.ok( stub.auxiliary_handler.calledOnce, 'on change handler should be called once' );
    });
    QUnit.test( '#4', function ( assert ) {
        var res = storeSelRowIndex();
        assert.equal( res, undefined, 'storeSelRowIndex should return undefined' );
        assert.deepEqual( auxiliary_get_val_from_html(),
                    [selRowIndex, selElement.model, selElement.id],
                    'storeSelRowIndex should store proper values to html' );
        assert.notOk( stub.auxiliary_handler.called, 'on change handler should not be called' );
    });
} );

//=============================================================================
QUnit.module( "browtab onKeyDown", function( hooks ) { 
    var arr = {};
    var tbody_tr_selector;
    hooks.beforeEach( function( assert ) {
        stub = {};
        tbody_tr_selector = "#browtable tbody tr";
        stub.runhref         = sinon.stub( window, "runhref" );
        stub.getVisibleIndex = sinon.stub( window, "getVisibleIndex" ).returns( arr );
        stub.setSelRow       = sinon.stub( window, "setSelRow" );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( "Enter key", function( assert ) {
        expect( 5 );
        var k   = 13;    // key pressed code
        var res = onKeyDown( k );
        assert.ok( stub.runhref.calledOnce, 'runhref should be called once' );
        assert.ok( stub.runhref.calledWithExactly(), 'runhref should be called with arg' );
        assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
        assert.notOk( stub.setSelRow.called, 'setSelRow should not be called' );
        assert.equal( res, false, 'onKeyDown should return false' );
    } );
    QUnit.test( "Improper key", function( assert ) {
        expect( 4 );
        var k   = 0;    // key pressed code
        var res = onKeyDown( k );
        assert.notOk( stub.runhref.called, 'runhref should not be called' );
        assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
        assert.notOk( stub.setSelRow.called, 'setSelRow should not be called' );
        assert.equal( res, false, 'onKeyDown should return false' );
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#1", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  8;    // index of first visible record
            arr.i_bot   = 13;    // index of last visible record
            selRowIndex = 10;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -2; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 3; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#2", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  8;    // index of first visible record
            arr.i_bot   = 13;    // index of last visible record
            selRowIndex =  8;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#3", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  8;    // index of first visible record
            arr.i_bot   = 13;    // index of last visible record
            selRowIndex = 13;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#4", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  2;    // index of first visible record
            arr.i_bot   =  7;    // index of last visible record
            selRowIndex =  2;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#5", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   = 15;    // index of first visible record
            arr.i_bot   = 20;    // index of last visible record
            selRowIndex = 20;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#6", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 5;    // number of all records
            arr.i_top   = 0;    // index of first visible record
            arr.i_bot   = 4;    // index of last visible record
            selRowIndex = 2;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -2; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 2; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#7", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 1;    // number of all records
            arr.i_top   = 0;    // index of first visible record
            arr.i_bot   = 0;    // index of last visible record
            selRowIndex = 0;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = 0; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 0; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#8", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  8;    // index of first visible record
            arr.i_bot   = 13;    // index of last visible record
            selRowIndex =  6;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 7; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "#9", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            tbody_tr_selector = "#browtable tbody tr";
            rowsNumber  = 22;    // number of all records
            arr.i_top   =  8;    // index of first visible record
            arr.i_bot   = 13;    // index of last visible record
            selRowIndex = 15;    // selected row index 0 <= selRowIndex < rowsNumber
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'Page up', function ( assert ) {
            expect( 6 );
            var k   = 33;    // key pressed code
            var iShift = -7; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Page down', function ( assert ) {
            expect( 6 );
            var k   = 34;    // key pressed code
            var iShift = 5; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.ok( stub.getVisibleIndex.calledOnce, 'getVisibleIndex should be called once' );
            assert.ok( stub.getVisibleIndex.calledWithExactly( tbody_tr_selector ), 
                                                                            'getVisibleIndex should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'End key', function ( assert ) {
            expect( 5 );
            var k   = 35;    // key pressed code
            var iShift = rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Home key', function ( assert ) {
            expect( 5 );
            var k   = 36;    // key pressed code
            var iShift = -rowsNumber; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Left arrow key', function ( assert ) {
            expect( 5 );
            var k   = 37;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Up arrow key', function ( assert ) {
            expect( 5 );
            var k   = 38;    // key pressed code
            var iShift = -1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Right arrow key', function ( assert ) {
            expect( 5 );
            var k   = 39;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
        QUnit.test( 'Down arrow key', function ( assert ) {
            expect( 5 );
            var k   = 40;    // key pressed code
            var iShift = 1; // expected value of iShift inside onKeyDown()
            var res = onKeyDown( k );
            assert.notOk( stub.runhref.called, 'runhref should not be called' );
            assert.notOk( stub.getVisibleIndex.called, 'getVisibleIndex should not be called' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex + iShift ), 'setSelRow should be called with arg' );
            assert.equal( res, false, 'onKeyDown should return false' );
        });
    } );
    //-------------------------------------------------------------------------
} );
//=============================================================================
QUnit.module( "browtab qs_TR_arr functions", function( hooks ) { 
    var arr = {};
    hooks.beforeEach( function( assert ) {
        stub = {};
        arr.length = 55;
		rowsNumber = 77;
        stub.get_qs_TR_arr = sinon.stub( window, "get_qs_TR_arr" ).returns( arr );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( "create_qs_TR_arr", function( assert ) {
        expect( 5 );
        var res = create_qs_TR_arr();
        assert.ok( stub.get_qs_TR_arr.calledOnce, 'get_qs_TR_arr should be called once' );
        assert.ok( stub.get_qs_TR_arr.calledWithExactly( true ), 'get_qs_TR_arr should be called with arg' );
        assert.equal( qs_TR_arr, arr, 'create_qs_TR_arr should set value to global object' );
        assert.equal( rowsNumber_start, rowsNumber, 'create_qs_TR_arr should set value to global object' );
        assert.equal( res, undefined, 'create_qs_TR_arr should return undefined' );
    } );
    QUnit.test( "restore_qs_TR_arr", function( assert ) {
        expect( 4 );
        var res = restore_qs_TR_arr();
        assert.ok( stub.get_qs_TR_arr.calledOnce, 'get_qs_TR_arr should be called once' );
        assert.ok( stub.get_qs_TR_arr.calledWithExactly( false ), 'get_qs_TR_arr should be called with arg' );
        assert.equal( qs_TR_arr, arr, 'restore_qs_TR_arr should set value to global object' );
        // assert.equal( rowsNumber, 55, 'restore_qs_TR_arr should set value to global object' );
        assert.equal( res, undefined, 'restore_qs_TR_arr should return undefined' );
    } );
    QUnit.test( "getTRfromTbodyByIndex", function( assert ) {
        expect( 1 );
        var i = 1;
        var res = getTRfromTbodyByIndex( i );
        assert.equal( res[0], $( "#tr_qwerty_s" )[0], 'getTRfromTbodyByIndex should return proper value' );
    } );
} );

//=============================================================================
var columnsNumber;  // var declared in another js file, not in browtab.js 
QUnit.module( "browtab get_qs_TR_arr", function( hooks ) { 
    var i, j, TR;
    var expected_arr = [];   // 2D array - table
    var qs_obj = {};    // array stringified on server side
    var expected_TR_start = [];
    hooks.beforeEach( function( assert ) {
        stub = {};
        qs_obj = { 
                0: {
                    0: {'id': '3', 'model': 'user', 'name': 'george'}, 
                    1: 'george', 
                    2: ''
                    }, 
                1: {
                    0: {'id': '1', 'model': 'user', 'name': 'john'}, 
                    1: 'john', 
                    2: ''
                    },
                2: {
                    0: {'id': '3', 'model': 'folder', 'name': 'fjohn'}, 
                    1: 'fjohn', 
                    2: ''
                    }
                };
        var json_string = JSON.stringify( qs_obj ); // array stored in html by server
        $( "#json_arr" ).val( json_string );
        columnsNumber = 2;
        TR_start = [];
        for ( i in qs_obj ) {
            expected_arr[i] = [];
            TR = getTRfromTbodyByIndex( i );    // already tested function
            TR_start[i] = TR;
            expected_TR_start[i] = TR;
            expected_arr[i][0] = qs_obj[i][0];
            expected_arr[i][0].TR = TR;
            for ( j = 1 ; j <= columnsNumber; j++ ) {
                expected_arr[i][j] = qs_obj[i][j];
            }
        }
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( "is_start=true", function( assert ) {
        expect( 3 );
        TR_start = []; // clear array before this test
        var res = get_qs_TR_arr( true );
        assert.deepEqual( TR_start, expected_TR_start, 'get_qs_TR_arr should set value to global object' );
        assert.equal( rowsNumber, 3, 'get_qs_TR_arr should set value to global object' );
        assert.deepEqual( res, expected_arr, 'get_qs_TR_arr should return proper value' );
    } );
    QUnit.test( "is_start=false", function( assert ) {
        expect( 3 );
        var res = get_qs_TR_arr( false );
        assert.deepEqual( TR_start, expected_TR_start, 'get_qs_TR_arr should set value to global object' );
        assert.equal( rowsNumber, 3, 'get_qs_TR_arr should set value to global object' );
        assert.deepEqual( res, expected_arr, 'get_qs_TR_arr should return proper value' );
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "Get different data from qs_TR_arr", function( hooks ) {
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
		browtab_document_ready_handler();
		qs_TR_arr = get_qs_TR_arr( true ); // already tested function
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( 'getTRbyIndex', function ( assert ) {
            expect( 1 );
            qs_TR_arr[1][0].TR = 'qwerty';
            var res = getTRbyIndex( 1 );
            assert.equal( res, 'qwerty', 'getTRbyIndex should return proper value' );
        });
        QUnit.test( 'getTRbyIndex i out of range', function ( assert ) {
            expect( 1 );
            qs_TR_arr[1][0].TR = 'qwerty';
            var res = getTRbyIndex( 1 );
            assert.equal( res, 'qwerty', 'getTRbyIndex should return proper value' );
        });
        QUnit.test( 'get_m_id_n_ByIndex', function ( assert ) {
            expect( 1 );
            var expected = {'id': '1', 'model': 'user', 'name': 'john'};
            var res = get_m_id_n_ByIndex( 1 );
            assert.deepEqual( res, expected, 'get_m_id_n_ByIndex should return proper value' );
        });
        QUnit.test( 'getRowIndexbyID', function ( assert ) {
            expect( 5 );
            assert.equal( getRowIndexbyID( 'user'  , 3 ), 0, 'getRowIndexbyID should return proper value' );
            assert.equal( getRowIndexbyID( 'user'  , 1 ), 1, 'getRowIndexbyID should return proper value' );
            assert.equal( getRowIndexbyID( 'folder', 3 ), 2, 'getRowIndexbyID should return proper value' );
            assert.equal( getRowIndexbyID( 'report', 3 ), 0, 'getRowIndexbyID should return proper value' );
            assert.equal( getRowIndexbyID( 'user'  , 9 ), 0, 'getRowIndexbyID should return proper value' );
        });
        QUnit.test( 'getTRbyID', function ( assert ) {
            expect( 5 );
            assert.equal( getTRbyID( 'user'  , 3 ), getTRbyIndex( 0 ), 'getTRbyID should return proper value' );
            assert.equal( getTRbyID( 'user'  , 1 ), getTRbyIndex( 1 ), 'getTRbyID should return proper value' );
            assert.equal( getTRbyID( 'folder', 3 ), getTRbyIndex( 2 ), 'getTRbyID should return proper value' );
            assert.equal( getTRbyID( 'report', 3 ), undefined, 'getTRbyID should return proper value' );
            assert.equal( getTRbyID( 'user'  , 9 ), undefined, 'getTRbyID should return proper value' );
        });
        QUnit.test( 'display_qs_TR_arr', function ( assert ) {
            rowsNumber = 3;
            expect( 9 + rowsNumber );
            selElement.model = 'qwerty';
            selElement.id    = 77;
            var tbody_selector = "#browtable tbody";
            var TR = "<tr><th>hello!</th></tr>";
            stub.getTRbyIndex       = sinon.stub( window, "getTRbyIndex" ).returns( TR );
            stub.getRowIndexbyID    = sinon.stub( window, "getRowIndexbyID" ).returns( 55 );
            stub.setSelRow          = sinon.stub( window, "setSelRow" );
//            stub.get_m_id_n_ByIndex = sinon.stub( window, "get_m_id_n_ByIndex" ).returns( {m:'mm', i:99} );
//            stub.storeSelRowIndex   = sinon.stub( window, "storeSelRowIndex" );
//            stub.scrollToRow        = sinon.stub( window, "scrollToRow" );
//            stub.selRowFocus        = sinon.stub( window, "selRowFocus" );

            var res = display_qs_TR_arr();
            
            assert.equal( $( "td", tbody_selector ).length, 0, "old rows cleared successfully!" );
            assert.equal( $( "th", tbody_selector ).length, rowsNumber, "new rows added successfully!" );

            assert.equal( stub.getTRbyIndex.callCount, rowsNumber, 'getTRbyIndex should be called '+rowsNumber+' times' );
            for ( i = 0 ; i < rowsNumber ; i++ ) {
                assert.ok( stub.getTRbyIndex.calledWithExactly( i ), 'getTRbyIndex should be called with i='+i );
            }
            assert.ok( stub.getRowIndexbyID.calledOnce, 'getRowIndexbyID should be called once' );
            assert.ok( stub.getRowIndexbyID.calledWithExactly( 'qwerty', 77 ), 'getRowIndexbyID should be called with arg' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( 55 ), 'setSelRow should be called with arg' );
//            assert.ok( stub.get_m_id_n_ByIndex.calledOnce, 'get_m_id_n_ByIndex should be called once' );
//            assert.ok( stub.get_m_id_n_ByIndex.calledWithExactly( 55 ), 'get_m_id_n_ByIndex should be called with arg' );
//            assert.ok( stub.storeSelRowIndex.calledOnce, 'storeSelRowIndex should be called once' );
//            assert.ok( stub.storeSelRowIndex.calledWithExactly(), 'storeSelRowIndex should be called with arg' );
//            assert.ok( stub.scrollToRow.calledOnce, 'scrollToRow should be called once' );
//            assert.ok( stub.scrollToRow.calledWithExactly( 55 ), 'scrollToRow should be called with arg' );
//            assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
            assert.equal( selRowIndex, 55, 'display_qs_TR_arr should set value to global selRowIndex' );
//            assert.deepEqual( selElement, {m:'mm', i:99}, 'display_qs_TR_arr should set value to global selElement' );
            assert.equal( res, undefined, 'display_qs_TR_arr should return proper value' );
        });
        QUnit.test( 'deleteElement', function ( assert ) {
            expect( 8 );
            selRowIndex = 1;
            selTR = getTRbyIndex( selRowIndex );    // already tested function

            stub.setSelRow          = sinon.stub( window, "setSelRow" );
            stub.selRowFocus        = sinon.stub( window, "selRowFocus" );

            assert.equal( qs_TR_arr.length, 3, 'qs_TR_arr.length before test should be equal to 3' );
            
            var res = deleteElement();
            
            assert.equal( qs_TR_arr.length, 2, 'qs_TR_arr.length after test should be equal to 2' );
            assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
            assert.ok( stub.setSelRow.calledWithExactly( selRowIndex ), 'setSelRow should be called with arg' );
            assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
            assert.ok( stub.selRowFocus.calledWithExactly(), 'selRowFocus should be called with arg' );
            assert.equal( rowsNumber, 2, 'deleteElement should set value to global selRowIndex' );
            assert.equal( res, undefined, 'deleteElement should return proper value' );
        });
    } );
} );
//=============================================================================
QUnit.module( "browtab Scrolling", function( hooks ) { // This test described in tbody_hidden.xlsx file
    hooks.beforeEach( function( assert ) {
        stub = {};
		browtab_document_ready_handler();
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'getSelectorTR', function ( assert ) {
        expect( 1 );
        var qq = 55, i = 77;
        var s = "#browtable tbody tr:" + qq + "(" + i + ")" ;
        var res = getSelectorTR( qq, i );
        assert.equal( res, s, 'getSelectorTR should return proper value' );
    });
    //-------------------------------------------------------------------------
    QUnit.module( "getVisibleIndex", function( hooks ) {
        var hi;
        var tbody_selector = "#browtable tbody";
        var tbody_tr_selector = "#browtable tbody tr";
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            rowsNumber = 20;
			browtab_document_ready_handler();
            // $tbody = $( tbody_selector );
            $( tbody_tr_selector ).remove(); // removing all <TR> from table
            var i, TR;
            for ( i = 0 ; i < rowsNumber ; i++ ) {    // adding all new <TR> to table
                TR = "<tr><td>" + i + "</td></tr>";
                $( tbody_selector ).append( TR ); 
            }
            hi = $( tbody_tr_selector ).outerHeight();   // height of i-th element
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( '#1', function ( assert ) {
            expect( 7 );
            var expected = {};
            var i_top = 0;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.0;
            h_tbody  += hi * 0.0;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 0;

            stub.scrollTop   = sinon.stub( $tbody, "scrollTop" ).returns( h_hidden );
            stub.height      = sinon.stub( $tbody, "height" ).returns( h_tbody );
            stub.outerHeight = sinon.spy( jQuery.prototype, "outerHeight" );
            var res = getVisibleIndex( tbody_tr_selector );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWithExactly(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWithExactly(), 'height should be called with arg' );
            assert.equal( stub.outerHeight.callCount, rowsNumber, 'outerHeight should be called rowsNumber times' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#2', function ( assert ) {
            expect( 7 );
            var expected = {};
            var i_top = 1;
            var i_bot = 10;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.0;
            h_tbody  += hi * 0.0;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 0;

            stub.scrollTop   = sinon.stub( $tbody, "scrollTop" ).returns( h_hidden );
            stub.height      = sinon.stub( $tbody, "height" ).returns( h_tbody );
            stub.outerHeight = sinon.spy( jQuery.prototype, "outerHeight" );
            var res = getVisibleIndex( tbody_tr_selector );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWithExactly(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWithExactly(), 'height should be called with arg' );
            assert.equal( stub.outerHeight.callCount, rowsNumber, 'outerHeight should be called rowsNumber times' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#3', function ( assert ) {
            expect( 7 );
            var expected = {};
            var i_top = 10;
            var i_bot = 19;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.0;
            h_tbody  += hi * 0.0;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 0;

            stub.scrollTop   = sinon.stub( $tbody, "scrollTop" ).returns( h_hidden );
            stub.height      = sinon.stub( $tbody, "height" ).returns( h_tbody );
            stub.outerHeight = sinon.spy( jQuery.prototype, "outerHeight" );
            var res = getVisibleIndex( tbody_tr_selector );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWithExactly(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWithExactly(), 'height should be called with arg' );
            assert.equal( stub.outerHeight.callCount, rowsNumber, 'outerHeight should be called rowsNumber times' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#4', function ( assert ) {
            expect( 7 );
            var expected = {};
            var i_top = 0;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.40;
            h_tbody  += hi * 0.0;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 0;

            stub.scrollTop   = sinon.stub( $tbody, "scrollTop" ).returns( h_hidden );
            stub.height      = sinon.stub( $tbody, "height" ).returns( h_tbody );
            stub.outerHeight = sinon.spy( jQuery.prototype, "outerHeight" );
            var res = getVisibleIndex( tbody_tr_selector );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWithExactly(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWithExactly(), 'height should be called with arg' );
            assert.equal( stub.outerHeight.callCount, rowsNumber, 'outerHeight should be called rowsNumber times' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#5', function ( assert ) {
            expect( 7 );
            var expected = {};
            var i_top = 0;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.60;
            h_tbody  -= hi * 0.40;
            expected.i_top = i_top + 1;
            expected.i_bot = i_bot + 0;

            stub.scrollTop   = sinon.stub( $tbody, "scrollTop" ).returns( h_hidden );
            stub.height      = sinon.stub( $tbody, "height" ).returns( h_tbody );
            stub.outerHeight = sinon.spy( jQuery.prototype, "outerHeight" );
            var res = getVisibleIndex( tbody_tr_selector );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWithExactly(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWithExactly(), 'height should be called with arg' );
            assert.equal( stub.outerHeight.callCount, rowsNumber, 'outerHeight should be called rowsNumber times' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#6', function ( assert ) {
            expect( 7 );
            var expected = {};
            var i_top = 1;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.000;
            h_tbody  += hi * 0.40;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 0;

            stub.scrollTop   = sinon.stub( $tbody, "scrollTop" ).returns( h_hidden );
            stub.height      = sinon.stub( $tbody, "height" ).returns( h_tbody );
            stub.outerHeight = sinon.spy( jQuery.prototype, "outerHeight" );
            var res = getVisibleIndex( tbody_tr_selector );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWithExactly(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWithExactly(), 'height should be called with arg' );
            assert.equal( stub.outerHeight.callCount, rowsNumber, 'outerHeight should be called rowsNumber times' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#7', function ( assert ) {
            expect( 7 );
            var expected = {};
            var i_top = 1;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.000;
            h_tbody  += hi * 0.60;
            expected.i_top = i_top + 0;
            expected.i_bot = i_bot + 1;

            stub.scrollTop   = sinon.stub( $tbody, "scrollTop" ).returns( h_hidden );
            stub.height      = sinon.stub( $tbody, "height" ).returns( h_tbody );
            stub.outerHeight = sinon.spy( jQuery.prototype, "outerHeight" );
            var res = getVisibleIndex( tbody_tr_selector );
            assert.equal( $( "td", tbody_selector ).length, rowsNumber, "new rows added successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWithExactly(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWithExactly(), 'height should be called with arg' );
            assert.equal( stub.outerHeight.callCount, rowsNumber, 'outerHeight should be called rowsNumber times' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( '#8 empty tbody', function ( assert ) {
            expect( 7 );
            $( tbody_tr_selector ).remove(); // removing all <TR> from table
            var expected = {};
            var i_top = 0;
            var i_bot = 9;
            // size in pixels for not fractioned namber of records:
            var h_hidden = hi * i_top;                  // hidden part above tbody in px
            var h_tbody  = hi * (i_bot - i_top + 1);    // visible tbody height in px
            // change sizes for some fractions of record:
            h_hidden += hi * 0.00;
            h_tbody  += hi * 0.00;
            expected.i_top = 0;
            expected.i_bot = 0;

            stub.scrollTop   = sinon.stub( $tbody, "scrollTop" ).returns( h_hidden );
            stub.height      = sinon.stub( $tbody, "height" ).returns( h_tbody );
            stub.outerHeight = sinon.spy( jQuery.prototype, "outerHeight" );
            var res = getVisibleIndex( tbody_tr_selector );
            assert.equal( $( "td", tbody_selector ).length, 0, "rows removed successfully!" );
            assert.ok( stub.scrollTop.calledOnce, 'scrollTop should be called once' );
            assert.ok( stub.scrollTop.calledWithExactly(), 'scrollTop should be called with arg' );
            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.height.calledWithExactly(), 'height should be called with arg' );
            assert.equal( stub.outerHeight.callCount, 0, 'outerHeight should be called 0 times' );
            assert.deepEqual( res, expected, 'getVisibleIndex should return proper value' );
        });
        QUnit.test( 'totalOuterHeight', function ( assert ) {
            expect( 1 );
            $( tbody_tr_selector ).outerHeight( 30 );
            hi = $( tbody_tr_selector ).outerHeight();   // height of i-th element
            var h = hi * rowsNumber;
            var res = totalOuterHeight( tbody_tr_selector );
            assert.equal( res, h, 'totalOuterHeight should return proper value' );
        });
        QUnit.test( 'totalOuterHeight empty tbody', function ( assert ) {
            expect( 1 );
            $( tbody_tr_selector ).remove(); // removing all <TR> from table
//            $( tbody_tr_selector ).outerHeight( 30 );
            hi = $( tbody_tr_selector ).outerHeight();   // height of i-th element
            var h = hi * rowsNumber;
            var res = totalOuterHeight( tbody_tr_selector );
            assert.equal( res, h, 'totalOuterHeight should return proper value' );
        });
    } );
    //-------------------------------------------------------------------------
    QUnit.module( "scrollToRow", function( hooks ) {
        var hi;
        var tbody_selector = "#browtable tbody";
        hooks.beforeEach( function( assert ) { // This will run after the parent module's beforeEach hook
            rowsNumber = 20;
            $tbody = $( tbody_selector );
            hi = 20;   // height of i-th element
        } );
        hooks.afterEach( function( assert ) {  // This will run before the parent module's afterEach
        } );
        QUnit.test( '#0', function ( assert ) {
            expect( 12 );
            var i = 5;
            var h_hidden    = 0;
            var h_tbody     = 200;

            var selectorLtI = 'lt';
            var selectorEqI = 'eq';
            var h_tr        = hi;
            var h_aboveSel  = hi * i;
            var h_uptoSel   = h_aboveSel + h_tr;                    // -//- including i-th tr height
            // expected value calculated by formula:
            var h_hidden_calc = h_hidden;
            if ( h_hidden >= h_aboveSel ) {                         // i-th row is in hidden area above tbody?
                h_hidden_calc = h_aboveSel;                              // we allow to hide this part of common height
            } else if ( h_uptoSel >= h_hidden + h_tbody ) {         // i-th row is not visible below tbody?
                h_hidden_calc = h_uptoSel - h_tbody;                     // we allow to hide this part of common heiight
            }

            stub.height             = sinon.stub( $tbody, "height" );
            stub.scrollTop          = sinon.stub( $tbody, "scrollTop" );
            stub.getSelectorTR      = sinon.stub( window, "getSelectorTR" );
            stub.totalOuterHeight   = sinon.stub( window, "totalOuterHeight" );

            stub.height             .onCall( 0 ).returns( h_tbody );
            stub.scrollTop          .onCall( 0 ).returns( h_hidden );
            stub.scrollTop          .onCall( 1 ).returns();
            stub.getSelectorTR      .onCall( 0 ).returns( selectorLtI );
            stub.getSelectorTR      .onCall( 1 ).returns( selectorEqI );
            stub.totalOuterHeight   .onCall( 0 ).returns( h_tr );
            stub.totalOuterHeight   .onCall( 1 ).returns( h_aboveSel );

            var res = scrollToRow( i, $tbody );

            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.scrollTop.calledTwice, 'scrollTop should be called twice' );
            assert.ok( stub.getSelectorTR.calledTwice, 'getSelectorTR should be called twice' );
            assert.ok( stub.totalOuterHeight.calledTwice, 'totalOuterHeight should be called twice' );

            assert.ok( stub.getSelectorTR.getCall( 0 ).calledWithExactly(  "lt", i  ), 
                                                                            'getSelectorTR should be called with arg' );
            assert.ok( stub.getSelectorTR.getCall( 1 ).calledWithExactly(  "eq", i  ), 
                                                                            'getSelectorTR should be called with arg' );
            assert.ok( stub.height.getCall( 0 ).calledWithExactly(), 'height should be called with arg' );
            assert.ok( stub.totalOuterHeight.getCall( 0 ).calledWithExactly( selectorEqI ), 
                                                                            'totalOuterHeight should be called with arg' );
            assert.ok( stub.totalOuterHeight.getCall( 1 ).calledWithExactly( selectorLtI ), 
                                                                            'totalOuterHeight should be called with arg' );
            assert.ok( stub.scrollTop.getCall( 0 ).calledWithExactly(), '0 scrollTop should be called with arg' );
            assert.ok( stub.scrollTop.getCall( 1 ).calledWithExactly( h_hidden_calc ), 
                                                                            '1 scrollTop should be called with arg' );

            assert.equal( res, h_hidden_calc, 'scrollToRow should return proper value' );
        });
        QUnit.test( '#1', function ( assert ) {
            expect( 12 );
            var i = 5;
            var h_hidden    = 0;
            var h_tbody     = 200;
            var h_hidden_calc = 0;            // selected row is visible
            // expected value calculated manually

            var selectorLtI = 'lt';
            var selectorEqI = 'eq';
            var h_tr        = hi;
            var h_aboveSel  = hi * i;

            stub.height             = sinon.stub( $tbody, "height" );
            stub.scrollTop          = sinon.stub( $tbody, "scrollTop" );
            stub.getSelectorTR      = sinon.stub( window, "getSelectorTR" );
            stub.totalOuterHeight   = sinon.stub( window, "totalOuterHeight" );

            stub.height             .onCall( 0 ).returns( h_tbody );
            stub.scrollTop          .onCall( 0 ).returns( h_hidden );
            stub.scrollTop          .onCall( 1 ).returns();
            stub.getSelectorTR      .onCall( 0 ).returns( selectorLtI );
            stub.getSelectorTR      .onCall( 1 ).returns( selectorEqI );
            stub.totalOuterHeight   .onCall( 0 ).returns( h_tr );
            stub.totalOuterHeight   .onCall( 1 ).returns( h_aboveSel );

            var res = scrollToRow( i, $tbody );

            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.scrollTop.calledTwice, 'scrollTop should be called twice' );
            assert.ok( stub.getSelectorTR.calledTwice, 'getSelectorTR should be called twice' );
            assert.ok( stub.totalOuterHeight.calledTwice, 'totalOuterHeight should be called twice' );

            assert.ok( stub.getSelectorTR.getCall( 0 ).calledWithExactly(  "lt", i  ), 
                                                                            'getSelectorTR should be called with arg' );
            assert.ok( stub.getSelectorTR.getCall( 1 ).calledWithExactly(  "eq", i  ), 
                                                                            'getSelectorTR should be called with arg' );
            assert.ok( stub.height.getCall( 0 ).calledWithExactly(), 'height should be called with arg' );
            assert.ok( stub.totalOuterHeight.getCall( 0 ).calledWithExactly( selectorEqI ), 
                                                                            'totalOuterHeight should be called with arg' );
            assert.ok( stub.totalOuterHeight.getCall( 1 ).calledWithExactly( selectorLtI ), 
                                                                            'totalOuterHeight should be called with arg' );
            assert.ok( stub.scrollTop.getCall( 0 ).calledWithExactly(), '0 scrollTop should be called with arg' );
            assert.ok( stub.scrollTop.getCall( 1 ).calledWithExactly( h_hidden_calc ), 
                                                                            '1 scrollTop should be called with arg' );

            assert.equal( res, h_hidden_calc, 'scrollToRow should return proper value' );
        });
        QUnit.test( '#2', function ( assert ) {
            expect( 12 );
            var i = 2;
            var h_hidden    = 70;
            var h_tbody     = 200;
            var h_hidden_calc = 40;            // selected row is hidden above the tbody
            // expected value calculated manually

            var selectorLtI = 'lt';
            var selectorEqI = 'eq';
            var h_tr        = hi;
            var h_aboveSel  = hi * i;

            stub.height             = sinon.stub( $tbody, "height" );
            stub.scrollTop          = sinon.stub( $tbody, "scrollTop" );
            stub.getSelectorTR      = sinon.stub( window, "getSelectorTR" );
            stub.totalOuterHeight   = sinon.stub( window, "totalOuterHeight" );

            stub.height             .onCall( 0 ).returns( h_tbody );
            stub.scrollTop          .onCall( 0 ).returns( h_hidden );
            stub.scrollTop          .onCall( 1 ).returns();
            stub.getSelectorTR      .onCall( 0 ).returns( selectorLtI );
            stub.getSelectorTR      .onCall( 1 ).returns( selectorEqI );
            stub.totalOuterHeight   .onCall( 0 ).returns( h_tr );
            stub.totalOuterHeight   .onCall( 1 ).returns( h_aboveSel );

            var res = scrollToRow( i, $tbody );

            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.scrollTop.calledTwice, 'scrollTop should be called twice' );
            assert.ok( stub.getSelectorTR.calledTwice, 'getSelectorTR should be called twice' );
            assert.ok( stub.totalOuterHeight.calledTwice, 'totalOuterHeight should be called twice' );

            assert.ok( stub.getSelectorTR.getCall( 0 ).calledWithExactly(  "lt", i  ), 
                                                                            'getSelectorTR should be called with arg' );
            assert.ok( stub.getSelectorTR.getCall( 1 ).calledWithExactly(  "eq", i  ), 
                                                                            'getSelectorTR should be called with arg' );
            assert.ok( stub.height.getCall( 0 ).calledWithExactly(), 'height should be called with arg' );
            assert.ok( stub.totalOuterHeight.getCall( 0 ).calledWithExactly( selectorEqI ), 
                                                                            'totalOuterHeight should be called with arg' );
            assert.ok( stub.totalOuterHeight.getCall( 1 ).calledWithExactly( selectorLtI ), 
                                                                            'totalOuterHeight should be called with arg' );
            assert.ok( stub.scrollTop.getCall( 0 ).calledWithExactly(), '0 scrollTop should be called with arg' );
            assert.ok( stub.scrollTop.getCall( 1 ).calledWithExactly( h_hidden_calc ), '1 scrollTop should be called with arg' );

            assert.equal( res, h_hidden_calc, 'scrollToRow should return proper value' );
        });
        QUnit.test( '#3', function ( assert ) {
            expect( 12 );
            var i = 11;
            var h_hidden    = 10;
            var h_tbody     = 200;
            var h_hidden_calc = 40;            // selected row is hidden below the tbody
            // expected value calculated manually

            var selectorLtI = 'lt';
            var selectorEqI = 'eq';
            var h_tr        = hi;
            var h_aboveSel  = hi * i;

            stub.height             = sinon.stub( $tbody, "height" );
            stub.scrollTop          = sinon.stub( $tbody, "scrollTop" );
            stub.getSelectorTR      = sinon.stub( window, "getSelectorTR" );
            stub.totalOuterHeight   = sinon.stub( window, "totalOuterHeight" );

            stub.height             .onCall( 0 ).returns( h_tbody );
            stub.scrollTop          .onCall( 0 ).returns( h_hidden );
            stub.scrollTop          .onCall( 1 ).returns();
            stub.getSelectorTR      .onCall( 0 ).returns( selectorLtI );
            stub.getSelectorTR      .onCall( 1 ).returns( selectorEqI );
            stub.totalOuterHeight   .onCall( 0 ).returns( h_tr );
            stub.totalOuterHeight   .onCall( 1 ).returns( h_aboveSel );

            var res = scrollToRow( i, $tbody );

            assert.ok( stub.height.calledOnce, 'height should be called once' );
            assert.ok( stub.scrollTop.calledTwice, 'scrollTop should be called twice' );
            assert.ok( stub.getSelectorTR.calledTwice, 'getSelectorTR should be called twice' );
            assert.ok( stub.totalOuterHeight.calledTwice, 'totalOuterHeight should be called twice' );

            assert.ok( stub.getSelectorTR.getCall( 0 ).calledWithExactly(  "lt", i  ), 
                                                                            'getSelectorTR should be called with arg' );
            assert.ok( stub.getSelectorTR.getCall( 1 ).calledWithExactly(  "eq", i  ), 
                                                                            'getSelectorTR should be called with arg' );
            assert.ok( stub.height.getCall( 0 ).calledWithExactly(), 'height should be called with arg' );
            assert.ok( stub.totalOuterHeight.getCall( 0 ).calledWithExactly( selectorEqI ), 
                                                                            'totalOuterHeight should be called with arg' );
            assert.ok( stub.totalOuterHeight.getCall( 1 ).calledWithExactly( selectorLtI ), 
                                                                            'totalOuterHeight should be called with arg' );
            assert.ok( stub.scrollTop.getCall( 0 ).calledWithExactly(), '0 scrollTop should be called with arg' );
            assert.ok( stub.scrollTop.getCall( 1 ).calledWithExactly( h_hidden_calc ), 
                                                                            '1 scrollTop should be called with arg' );

            assert.equal( res, h_hidden_calc, 'scrollToRow should return proper value' );
        });
    } );
} );
//=============================================================================
function setValToHTML( i, j, val, supplement ) {    // function declared in another js file, not in browtab.js 
}

QUnit.module( "browtab Changing both <tbody> and qs_TR_arr", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    //-------------------------------------------------------------------------
    QUnit.test( 'setValToHTMLrow', function ( assert ) {
        expect( 4 );
        var i = 5;
        var j;
        var changes = ['000','111'];
        var supplement = 'qwerty';
        stub.setValToHTML = sinon.stub( window, "setValToHTML" );
        var res = setValToHTMLrow( i, changes, supplement  );
        assert.ok( stub.setValToHTML.calledTwice, 'setValToHTML should be called twice' );
        assert.ok( stub.setValToHTML.getCall( 0 ).calledWithExactly( i, '0', '000', supplement ), 
                                                                            '0 setValToHTML should be called with arg' );
        assert.ok( stub.setValToHTML.getCall( 1 ).calledWithExactly( i, '1', '111', supplement ), 
                                                                            '1 setValToHTML should be called with arg' );
        assert.deepEqual( res, undefined, 'setValToHTMLrow should return proper value' );  
    });
    //-------------------------------------------------------------------------
    QUnit.test( 'changeSelElement', function ( assert ) {
        expect( 12 );
        selRowIndex = 1;
        qs_TR_arr = [ [0, 0], [0, 0] ];
        var TR = $( "#browtable tbody tr" ); 
        var ob = {};
        ob.model  = 'user';  
        ob.id     = 55;
        ob.name   = 'fred';
        var changes = [ob, '111'];
        var supplement = 'qwerty';

        stub.setValToHTMLrow = sinon.stub( window, "setValToHTMLrow" );
        stub.getTRfromTbodyByIndex = sinon.stub( window, "getTRfromTbodyByIndex" ).returns( TR );
        stub.selRowFocus = sinon.stub( window, "selRowFocus" );

        var res = changeSelElement( changes, supplement );

        assert.ok( stub.setValToHTMLrow.calledOnce, 'setValToHTMLrow should be called once' );
        assert.ok( stub.setValToHTMLrow.calledWithExactly( selRowIndex, changes, supplement ),
                                                            'setValToHTMLrow should be called with arg' );
        assert.ok( stub.getTRfromTbodyByIndex.calledOnce, 'getTRfromTbodyByIndex should be called once' );
        assert.ok( stub.getTRfromTbodyByIndex.calledWithExactly( selRowIndex ),
                                                            'getTRfromTbodyByIndex should be called with arg' );
        assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
        assert.ok( stub.selRowFocus.calledWithExactly(),'selRowFocus should be called with arg' );

        assert.deepEqual( qs_TR_arr[selRowIndex][0].TR, TR, 'changeSelElement should set value to global var' );
        assert.equal( qs_TR_arr[selRowIndex][0].model,  'user', 'changeSelElement should set value to global var' );
        assert.equal( qs_TR_arr[selRowIndex][0].id,     55, 'changeSelElement should set value to global var' );
        assert.equal( qs_TR_arr[selRowIndex][0].name,   'fred', 'changeSelElement should set value to global var' );
        assert.equal( qs_TR_arr[selRowIndex][1],        '111', 'changeSelElement should set value to global var' );

        assert.deepEqual( res, undefined, 'changeSelElement should return proper value' );  
    });
    //-------------------------------------------------------------------------
} );
//=============================================================================
