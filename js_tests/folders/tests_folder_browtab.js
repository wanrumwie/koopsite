/*
Global:  $ (?), QUnit (?), addNewElement (?), columnsNumber (?), createEmptyTR (?), expect (?), getTRfromTbodyByIndex (?), moveElement (?), qs_TR_arr (?), rowsNumber (?), selElement (?), selRowIndex (?), selTR (?), setValToHTML (?), set_name_to_selElement (?), sinon (?), stub, window (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

//var qs_TR_arr;   var declared in another file
QUnit.test( 'js file start assignments', function ( assert ) {
    expect( 1 );
    assert.deepEqual( columnsNumber, 4, 'columnsNumber should be set immediately after page loaded');
});
//=============================================================================
QUnit.module( "folder_browtab setValToHTML", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( '#1', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 1;
        var val = "/static/img/file-icons/32px/pdf.png";
        var supplement = {};
        supplement.iconPath = val;
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'img' ).attr( "src" );

        assert.equal( put, val, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#2', function ( assert ) {
        expect( 3 );
        var i = 1;
        var j = 2;
        var val = 'qwerty';
        var iconPath = "/static/img/file-icons/32px/pdf.png";
        var supplement = {};
        supplement.iconPath = iconPath;
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        var tr_selector = "#browtable tbody tr:nth-child(" + (i+1) + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'A' ).text();
        var put_icon = $( tr_selector ).find( 'img' ).attr( "src" );

        assert.equal( put, val, 'setValToHTML should put value in template' );
        assert.equal( put_icon, iconPath, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#3', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 3;
        var val = '2016-01-31';
        var d = new Date( val );             // transform f_date (string) to js Date object
        d = d.toLocaleDateString();    // format date to dd.mm.yyyy
        var supplement = {};
        supplement.iconPath = [];
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'span' ).text();

        assert.equal( put, d, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
    QUnit.test( '#4', function ( assert ) {
        expect( 2 );
        var i = 1;
        var j = 4;
        var val = "";
        var supplement = {};
        supplement.iconPath = val;
        var selector = "#browtable tbody tr:nth-child(" + (i+1) + ") td:nth-child(" + j + ")";
        
        var res = setValToHTML( i, j, val, supplement );
        var put = $( selector ).find( 'span' ).text();

        assert.equal( put, val, 'setValToHTML should put value in template' );
        assert.equal( res, undefined, 'setValToHTML should return undefined value' );
    });
} );
//=============================================================================
QUnit.test( 'folder_browtab set_name_to_selElement', function ( assert ) {
    expect( 3 );
	browtab_document_ready_handler();
    var newName = 'qwerty';
    selRowIndex = 1;
    qs_TR_arr = [ [{},1,2,3,4],[{},1,2,3,4],[{},1,2,3,4] ];
    var res = set_name_to_selElement( newName );
    assert.equal( selElement.name, newName, 'set_name_to_selElement should set val tp global');
    assert.equal( qs_TR_arr[selRowIndex][0].name, newName, 'set_name_to_selElement should set val tp global');
    assert.equal( res, undefined, 'set_name_to_selElement should return undefined value' );
});
QUnit.test( 'folder_browtab createEmptyTR', function ( assert ) {
    expect( 1 );
    var f_model  = 'report';  
    var f_id     = 555;
    var f_name   = 'fred.pdf';
    var expected = "<tr id=\"tr-report#555\" ><td id=\"td1-report#555\" ><img src=\"\" alt=\"report\"/></td><td id=\"td2-report#555\" ><a id=\"report#555\" href=\"/folders/report/555/\"></a></td><td id=\"td3-report#555\" ><span></span></td><td id=\"td4-report#555\" ><span></span></td></tr>";
    var res = createEmptyTR( f_model, f_id, f_name );
    assert.equal( res, expected, 'createEmptyTR should return expected value' );
});
//=============================================================================
QUnit.module( "folder_browtab addNewElement", function( hooks ) { 
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
    //-------------------------------------------------------------------------
    QUnit.test( 'addNewElement', function ( assert ) {
        expect( 27 );
        selRowIndex = 1;
        rowsNumber = 4;
        qs_TR_arr = [ [{},1,2,3,4], [{},1,2,3,4], [{},1,2,3,4], [{},1,2,3,4] ];

        var j;
        var ob = {};
        ob.model  = 'report';  
        ob.id     = 555;
        ob.name   = 'fred.pdf';
        var changes = [ob, '', 'fred.pdf', '11.01.2016', 1234567];
        var supplement = {};
        supplement.iconPath = "/static/img/file-icons/32px/pdf.png";
        var tr_pattern = '<tr id="tr555" ><td>new row</td></tr>';
        var TR = 'qwerty'; 

        stub.createEmptyTR          = sinon.stub( window, "createEmptyTR" ).returns( tr_pattern );
        stub.setValToHTMLrow        = sinon.stub( window, "setValToHTMLrow" );
        stub.getTRfromTbodyByIndex  = sinon.stub( window, "getTRfromTbodyByIndex" ).returns( TR );
        stub.setSelRow              = sinon.stub( window, "setSelRow" );
        stub.scrollToRow            = sinon.stub( window, "scrollToRow" );
        stub.selRowFocus            = sinon.stub( window, "selRowFocus" );

        var res = addNewElement( changes, supplement );
        
        assert.equal( $( "#browtable tbody tr" ).length,  5, 'addNewElement should add new TR to html' );
        assert.equal( $( "#tr555" ).find("td").text(),  'new row', 'addNewElement should add new TR to html' );
        assert.equal( qs_TR_arr.length,  5, 'addNewElement should add new row to qs_TR_arr' );
        assert.equal( qs_TR_arr[4][0].id,  ob.id, 'addNewElement should add new row to qs_TR_arr' );

        assert.ok( stub.createEmptyTR.calledOnce, 'createEmptyTR should be called once' );
        assert.ok( stub.createEmptyTR.calledWithExactly( ob.model, ob.id, ob.name ), 
                                                    'createEmptyTR should be called with arg' );
        assert.ok( stub.setValToHTMLrow.calledOnce, 'setValToHTMLrow should be called once' );
        assert.ok( stub.setValToHTMLrow.calledWithExactly( selRowIndex, changes, supplement ),
                                                            'setValToHTMLrow should be called with arg' );
        assert.ok( stub.getTRfromTbodyByIndex.calledOnce, 'getTRfromTbodyByIndex should be called once' );
        assert.ok( stub.getTRfromTbodyByIndex.calledWithExactly( selRowIndex ),
                                                    'getTRfromTbodyByIndex should be called with arg' );
        assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
        assert.ok( stub.setSelRow.calledWithExactly( rowsNumber ),'setSelRow should be called with arg' );
        assert.ok( stub.scrollToRow.calledOnce, 'scrollToRow should be called once' );
        assert.ok( stub.scrollToRow.calledWithExactly( selRowIndex ),'scrollToRow should be called with arg' );
        assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
        assert.ok( stub.selRowFocus.calledWithExactly(),'selRowFocus should be called with arg' );

        assert.deepEqual( rowsNumber, 5, 'addNewElement should set value to global var' );
        assert.deepEqual( selRowIndex, 4, 'addNewElement should set value to global var' );
        assert.deepEqual( qs_TR_arr[selRowIndex][0].TR, TR, 'addNewElement should set value to global var' );
        assert.equal( qs_TR_arr[selRowIndex][0].model,  ob.model, 'addNewElement should set value to global var' );
        assert.equal( qs_TR_arr[selRowIndex][0].id,     ob.id, 'addNewElement should set value to global var' );
        assert.equal( qs_TR_arr[selRowIndex][0].name,   ob.name, 'addNewElement should set value to global var' );
        for ( j=1 ; j<=4 ; j++ ){
            assert.equal( qs_TR_arr[selRowIndex][j], changes[j], 'addNewElement should set value to global var' );
        }
        assert.deepEqual( res, undefined, 'addNewElement should return proper value' );  
    });
    QUnit.test( 'moveElement', function ( assert ) {
        expect( 10 );
        selRowIndex = 1;
        rowsNumber = 4;
        selTR = getTRfromTbodyByIndex( 1 );
        qs_TR_arr = [ [{},1,2,3,4], [{},11,12,13,14], [{},21,22,23,24], [{},31,32,33,34] ];

        stub.setSelRow              = sinon.stub( window, "setSelRow" );
        stub.selRowFocus            = sinon.stub( window, "selRowFocus" );

        var res = moveElement( );

        assert.equal( $( "#browtable tbody tr" ).length,  3, 'addNewElement should remove TR from html' );
        assert.equal( $( "tr-folder#9" ).length, 0, 'addNewElement should remove proper TR from html' );
        assert.equal( qs_TR_arr.length,  3, 'addNewElement should remove row from qs_TR_arr' );
        assert.equal( qs_TR_arr[1][1],  21, 'addNewElement should remove proper row from qs_TR_arr' );

        assert.ok( stub.setSelRow.calledOnce, 'setSelRow should be called once' );
        assert.ok( stub.setSelRow.calledWithExactly( selRowIndex ),'setSelRow should be called with arg' );
        assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
        assert.ok( stub.selRowFocus.calledWithExactly(),'selRowFocus should be called with arg' );

        assert.deepEqual( rowsNumber, 3, 'addNewElement should set value to global var' );
        assert.deepEqual( res, undefined, 'addNewElement should return proper value' );  
    });
    //-------------------------------------------------------------------------
} );
