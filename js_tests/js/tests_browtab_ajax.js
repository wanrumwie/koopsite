/*
Global:  $ (?), JSON (?), QUnit (?), XMLHttpRequest (?), ajaxSuccessHandler, ajax_selRowIndexToSession (?), ajax_selRowIndexToSession_error_handler (?), ajax_selRowIndexToSession_success_handler (?), ajax_settings (?), ajax_startRowIndexFromSession (?), ajax_startRowIndexFromSession_error_handler (?), ajax_startRowIndexFromSession_success_handler (?), browtab_ajax_document_ready_handler (?), console (?), csrf_token (?), defineAbortButton, dialog, dialogMessage, dialog_box_form_close, expect (?), folderEmptyMessage, getSelElementArr, listeners_setting (?), loadEndHandler, onChange_handler (?), progressHandler, progressbarShow, rowsNumber (?), set_browtab_ajax_listeners (?), sinon (?), stub, transferCanceled (?), transferFailed (?), transferSuccess (?), transferSuccessDownload (?), window (?), xhrErrorAlert (?), xhrErrorHandler (?), xhrSuccessHandler, xhr_POST (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test
function getSelElementArr(){    // function declared in another file
    return {};
}
//=============================================================================
QUnit.module( "browtab_ajax document ready", function( hooks ) { 
//    var $tbody;
    var $selRowIndex;
    var selRowIndex_selector;
    var target_selector;
    var saved_csrf_token;
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler();
        
        target_selector       = "#td_qwerty";
        selRowIndex_selector  = "#selRowIndex";
        $selRowIndex          = $( selRowIndex_selector );
        set_browtab_ajax_listeners(); 
        saved_csrf_token      = $( "#csrfmiddlewaretoken" ).val();
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
        $( "#csrfmiddlewaretoken" ).val( saved_csrf_token );
        csrf_token = saved_csrf_token;
    } );
    QUnit.test( 'browtab_ajax_document_ready_handler', function ( assert ) {
        expect( 8 );
        $( "#csrfmiddlewaretoken" ).val( 'qwerty' );
        stub.create_qs_TR_arr = sinon.stub( window, "create_qs_TR_arr" );
        stub.ajax_startRowIndexFromSession = sinon.stub( window, "ajax_startRowIndexFromSession" );
        stub.set_browtab_ajax_listeners = sinon.stub( window, "set_browtab_ajax_listeners" );
        var res = browtab_ajax_document_ready_handler( );
        assert.ok( stub.create_qs_TR_arr.calledOnce, 'create_qs_TR_arr should be called once' );
        assert.ok( stub.create_qs_TR_arr.calledWithExactly( ), 'create_qs_TR_arr should be called with arg' );
        assert.ok( stub.ajax_startRowIndexFromSession.calledOnce, 'ajax_startRowIndexFromSession should be called once' );
        assert.ok( stub.ajax_startRowIndexFromSession.calledWithExactly(),
                                                                'ajax_startRowIndexFromSession should be called with arg');
        assert.ok( stub.set_browtab_ajax_listeners.calledOnce, 'set_browtab_ajax_listeners should be called once' );
        assert.ok( stub.set_browtab_ajax_listeners.calledWithExactly( ), 
                                                                'set_browtab_ajax_listeners should be called with arg' );
        assert.equal( csrf_token, 'qwerty', 'browtab_ajax_document_ready_handler should set value to global var' );
        assert.equal( res, undefined, 'browtab_ajax_document_ready_handler should return undefined' );
    });
    QUnit.test( 'set_browtab_ajax_listeners', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 5 );

        stub.off = sinon.spy( $selRowIndex, "off" );
        stub.on  = sinon.spy( $selRowIndex, "on" );

        var res = set_browtab_ajax_listeners( $selRowIndex );

        assert.ok( stub.off.calledOnce, 'off should be called once' );
        assert.ok( stub.on.calledOnce, 'on should be called once' );
        assert.ok( stub.off.getCall( 0 ).calledWithExactly( "change" ), '0 off should be called with arg' );
        assert.ok( stub.on.getCall( 0 ).calledWithExactly( "change", onChange_handler ), '0 on should be called with arg' );
        assert.equal( res, undefined, 'set_browtab_ajax_listeners should return undefined' );
    });
    QUnit.test( 'onChange_handler', function ( assert ) {
        expect( 3 );
        stub.ajax_selRowIndexToSession = sinon.stub( window, "ajax_selRowIndexToSession" );
        var res = onChange_handler( );
        assert.ok( stub.ajax_selRowIndexToSession.calledOnce, 'ajax_selRowIndexToSession should be called once' );
        assert.ok( stub.ajax_selRowIndexToSession.calledWithExactly(  ), 
                                                                'ajax_selRowIndexToSession should be called with arg' );
        assert.equal( res, false, 'onChange_handler should return false' );
    });
    QUnit.test( '$( ... ).on( "change",... STUB ajax_selRowIndexToSession', function ( assert ) {
        expect( 1 );
        stub.ajax_selRowIndexToSession = sinon.stub( window, "ajax_selRowIndexToSession" );
        $('#selRowIndex').trigger( 'change' );  // actibation of data exchange with session
//        $( selRowIndex_selector ).trigger( 'change' );
        assert.ok( stub.ajax_selRowIndexToSession.calledOnce, 'ajax_selRowIndexToSession should be called once' );
    });
} );
//=============================================================================
function dialogMessage( a,b,c,d ){  // function declared in another file
}
function dialog( a ){               // function declared in another file
}
function dialog_box_form_close() {  // function declared in another file
}
QUnit.module( "browtab_ajax dialogs & alert", function( hooks ) { 
    var xhr = {};
    hooks.beforeEach( function( assert ) {
        stub = {};
        xhr.status      ='s'; 
        xhr.statusText  ='t';
        xhr.responseText='r';
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'xhrErrorAlert', function ( assert ) {
        expect( 3 );
        var ss = '';
        var arg = 'xhrErrorAlert: ' + ss +
                '\n xhr.status='        + xhr.status + 
                '\n xhr.statusText='    + xhr.statusText + 
                '\n xhr.responseText='  + xhr.responseText;
        
        stub.alert = sinon.stub( window, "alert" );
        var res = xhrErrorAlert( xhr, ss );
        assert.ok( stub.alert.calledOnce, 'alert should be called once' );
        assert.ok( stub.alert.calledWithExactly( arg ), 'alert should be called with arg' );
        assert.equal( res, undefined, 'xhrErrorAlert should return undefined' );
    });
    QUnit.test( 'xhrErrorAlert ss', function ( assert ) {
        expect( 3 );
        var ss = 'qwerty';
        var arg = 'xhrErrorAlert: ' + ss +
                '\n xhr.status='        + xhr.status + 
                '\n xhr.statusText='    + xhr.statusText + 
                '\n xhr.responseText='  + xhr.responseText;
        
        stub.alert = sinon.stub( window, "alert" );
        var res = xhrErrorAlert( xhr, ss );
        assert.ok( stub.alert.calledOnce, 'alert should be called once' );
        assert.ok( stub.alert.calledWithExactly( arg ), 'alert should be called with arg' );
        assert.equal( res, undefined, 'xhrErrorAlert should return undefined' );
    });
    QUnit.test( 'xhrErrorHandler 200', function ( assert ) {
        expect( 5 );
        xhr.status      = 200; 
       
        stub.xhrErrorAlert          = sinon.stub( window, "xhrErrorAlert" );
        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );

        var res = xhrErrorHandler( xhr );

        assert.ok( stub.xhrErrorAlert.calledOnce, 'xhrErrorAlert should be called once' );
        assert.ok( stub.xhrErrorAlert.calledWithExactly( xhr, 'xhrErrorHandler' ), 'xhrErrorAlert should be called with arg' );
        assert.notOk( stub.dialogMessage.called, 'dialogMessage should not be called' );
        assert.notOk( stub.dialog_box_form_close.called, 'dialog_box_form_close should not be called' );
        assert.equal( res, undefined, 'xhrErrorHandler should return undefined' );
    });
    QUnit.test( 'xhrErrorHandler 401', function ( assert ) {
        expect( 6 );
        xhr.status      = 401; 
       
        stub.xhrErrorAlert          = sinon.stub( window, "xhrErrorAlert" );
        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );

        var res = xhrErrorHandler( xhr );

        assert.notOk( stub.xhrErrorAlert.called, 'xhrErrorAlert should not be called' );
        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( "Ви не маєте доступу до цієї операції!",
                      "Error", "Помилка доступу" ), 'dialogMessage should be called with arg' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly(  ), 'dialog_box_form_close should be called with arg' );
        assert.equal( res, undefined, 'xhrErrorHandler should return undefined' );
    });
    QUnit.test( 'xhrErrorHandler 403', function ( assert ) {
        expect( 6 );
        xhr.status      = 403; 
       
        stub.xhrErrorAlert          = sinon.stub( window, "xhrErrorAlert" );
        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );

        var res = xhrErrorHandler( xhr );

        assert.notOk( stub.xhrErrorAlert.called, 'xhrErrorAlert should not be called' );
        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( "Ви не маєте доступу до цієї операції!",
                      "Error", "Помилка доступу" ), 'dialogMessage should be called with arg' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly(  ), 'dialog_box_form_close should be called with arg' );
        assert.equal( res, undefined, 'xhrErrorHandler should return undefined' );
    });
    QUnit.test( 'transferFailed', function ( assert ) {
        expect( 5 );
        var evt = "";

        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );

        var res = transferFailed( evt );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( 
                        "An error occurred while transferring the file. Probably file too long", 
                        "Error", "UPLOAD ERROR" ), 'dialogMessage should be called with arg' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly(  ), 'dialog_box_form_close should be called with arg' );
        assert.equal( res, undefined, 'transferFailed should return undefined' );
    });
    QUnit.test( 'transferCanceled', function ( assert ) {
        expect( 5 );
        var evt = "";

        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );

        var res = transferCanceled( evt );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( "The transfer has been canceled by the user.", "", 
                                            "UPLOAD CANCELED", 5000 ), 'dialogMessage should be called with arg' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly(  ), 'dialog_box_form_close should be called with arg' );
        assert.equal( res, undefined, 'transferCanceled should return undefined' );
    });
} );
//=============================================================================
QUnit.test( 'browtab_ajax ajax_settings', function ( assert ) {
    expect( 1 );
    var as = {
        type    : "POST",
        dataType: "json",
        success : ajaxSuccessHandler,
        error   : xhrErrorHandler
    };
    var res = ajax_settings( );
    assert.deepEqual( res, as, 'ajax_settings should return proper value' );
});
//=============================================================================
function folderEmptyMessage( f_name ) {    // This function declared in another js file.
}
QUnit.module( "browtab_ajax session handlers", function( hooks ) { 
    var xhr;
    var sr;
    var json;
    hooks.beforeEach( function( assert ) {
        stub = {};
        xhr = 'qwerty';
        sr = {};
        sr.selRowIndex  = 55;
        sr.model        = 'folder';
        sr.id           = 77;
        json = {};
        json.server_response = sr;
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'ajax_selRowIndexToSession_error_handler', function ( assert ) {
        expect( 3 );
        stub.xhrErrorAlert = sinon.stub( window, "xhrErrorAlert" );
        var res = ajax_selRowIndexToSession_error_handler( xhr );
        assert.ok( stub.xhrErrorAlert.calledOnce, 'xhrErrorAlert should be called once' );
        assert.ok( stub.xhrErrorAlert.calledWithExactly( xhr, 'ajax_selRowIndexToSession' ), 
                                                                'xhrErrorAlert should be called with arg' );
        assert.equal( res, undefined, 'ajax_selRowIndexToSession_error_handler should return undefined' );
    });
    QUnit.test( 'ajax_startRowIndexFromSession_error_handler', function ( assert ) {
        expect( 5 );
        stub.xhrErrorAlert = sinon.stub( window, "xhrErrorAlert" );
        stub.setStartRow = sinon.stub( window, "setStartRow" );
        var res = ajax_startRowIndexFromSession_error_handler( xhr );
        assert.ok( stub.xhrErrorAlert.calledOnce, 'xhrErrorAlert should be called once' );
        assert.ok( stub.xhrErrorAlert.calledWithExactly( xhr, 'ajax_startRowIndexFromSession' ), 
                                                                'xhrErrorAlert should be called with arg' );
        assert.ok( stub.setStartRow.calledOnce, 'setStartRow should be called once' );
        assert.ok( stub.setStartRow.calledWithExactly( ), 'setStartRow should be called with arg' );
        assert.equal( res, undefined, 'ajax_startRowIndexFromSession_error_handler should return undefined' );
    });
    QUnit.test( 'ajax_startRowIndexFromSession_success_handler', function ( assert ) {
        expect( 7 );
        rowsNumber = 100;

        stub.setStartRow = sinon.stub( window, "setStartRow" );
        stub.folderEmptyMessage = sinon.stub( window, "folderEmptyMessage" );

        var res = ajax_startRowIndexFromSession_success_handler( json );

        assert.ok( stub.setStartRow.calledOnce, 'setStartRow should be called once' );
        assert.ok( stub.setStartRow.calledWithExactly( ), 'setStartRow should be called with arg' );
        assert.notOk( stub.folderEmptyMessage.called, 'folderEmptyMessage should not be called' );

        assert.equal( $( "#selRowIndex" ).val(), sr.selRowIndex, 'function set value to html' );
        assert.equal( $( "#selElementModel" ).val(), sr.model, 'function set value to html' );
        assert.equal( $( "#selElementID" ).val(), sr.id, 'function set value to html' );

        assert.equal( res, undefined, 'ajax_startRowIndexFromSession_success_handler should return undefined' );
    });
    QUnit.test( 'ajax_startRowIndexFromSession_success_handler empty folder', function ( assert ) {
        expect( 8 );
        rowsNumber = 0;
        var f_name = $( "#thisfolder span" ).text();    // parent folder name

        stub.setStartRow = sinon.stub( window, "setStartRow" );
        stub.folderEmptyMessage = sinon.stub( window, "folderEmptyMessage" );

        var res = ajax_startRowIndexFromSession_success_handler( json );

        assert.ok( stub.setStartRow.calledOnce, 'setStartRow should be called once' );
        assert.ok( stub.setStartRow.calledWithExactly( ), 'setStartRow should be called with arg' );
        assert.ok( stub.folderEmptyMessage.calledOnce, 'folderEmptyMessage should be called once' );
        assert.ok( stub.folderEmptyMessage.calledWithExactly( f_name ), 'folderEmptyMessage should be called with arg' );

        assert.equal( $( "#selRowIndex" ).val(), sr.selRowIndex, 'function set value to html' );
        assert.equal( $( "#selElementModel" ).val(), sr.model, 'function set value to html' );
        assert.equal( $( "#selElementID" ).val(), sr.id, 'function set value to html' );

        assert.equal( res, undefined, 'ajax_startRowIndexFromSession_success_handler should return undefined' );
    });
} );
//=============================================================================
function ajaxSuccessHandler(){  // function declared in another file
}
QUnit.module( "browtab_ajax ajax", function( hooks ) { 
    var requests = sinon.requests;
    var done;
    hooks.beforeEach( function( assert ) {
        stub = {};
        csrf_token = $( "#csrfmiddlewaretoken" ).val();
        this.xhr = sinon.useFakeXMLHttpRequest();
        requests = [];
        this.xhr.onCreate = function ( request ) {
            requests.push( request );
        };
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
        this.xhr.restore();
    } );
    QUnit.test( 'ajax_selRowIndexToSession', function ( assert ) {
        expect( 15 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/ajax-selrowindex-to-session";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var as = ajax_settings();
        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.success            = sinon.stub( window, "ajax_selRowIndexToSession_success_handler" );
        stub.error              = sinon.stub( window, "ajax_selRowIndexToSession_error_handler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.ajax_settings      = sinon.stub( window, "ajax_settings" ).returns( as );

        var res = ajax_selRowIndexToSession( );

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( as ), 'ajax should be called with arg' );

        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
        assert.equal( as.success, ajax_selRowIndexToSession_success_handler, 'function should set as.success' );
        assert.equal( as.error,   ajax_selRowIndexToSession_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_selRowIndexToSession should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_selRowIndexToSession error', function ( assert ) {
        expect( 15 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/ajax-selrowindex-to-session";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var as = ajax_settings();
        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.success            = sinon.stub( window, "ajax_selRowIndexToSession_success_handler" );
        stub.error              = sinon.stub( window, "ajax_selRowIndexToSession_error_handler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.ajax_settings      = sinon.stub( window, "ajax_settings" ).returns( as );

        var res = ajax_selRowIndexToSession( );

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( as ), 'ajax should be called with arg' );

        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
        assert.equal( as.success, ajax_selRowIndexToSession_success_handler, 'function should set as.success' );
        assert.equal( as.error,   ajax_selRowIndexToSession_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called once' );
        assert.ok( stub.error.calledOnce, 'error should not be called' );

        assert.equal( res, false, 'ajax_selRowIndexToSession should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_startRowIndexFromSession', function ( assert ) {
        expect( 15 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/ajax-startrowindex-from-session";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var as = ajax_settings();
        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.success            = sinon.stub( window, "ajax_startRowIndexFromSession_success_handler" );
        stub.error              = sinon.stub( window, "ajax_startRowIndexFromSession_error_handler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.ajax_settings      = sinon.stub( window, "ajax_settings" ).returns( as );

        var res = ajax_startRowIndexFromSession( );

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( as ), 'ajax should be called with arg' );

        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
        assert.equal( as.success, ajax_startRowIndexFromSession_success_handler, 'function should set as.success' );
        assert.equal( as.error,   ajax_startRowIndexFromSession_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_startRowIndexFromSession should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_startRowIndexFromSession error', function ( assert ) {
        expect( 15 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/ajax-startrowindex-from-session";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var as = ajax_settings();
        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.success            = sinon.stub( window, "ajax_startRowIndexFromSession_success_handler" );
        stub.error              = sinon.stub( window, "ajax_startRowIndexFromSession_error_handler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.ajax_settings      = sinon.stub( window, "ajax_settings" ).returns( as );

        var res = ajax_startRowIndexFromSession( );

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( as ), 'ajax should be called with arg' );

        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
        assert.equal( as.success, ajax_startRowIndexFromSession_success_handler, 'function should set as.success' );
        assert.equal( as.error,   ajax_startRowIndexFromSession_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called once' );
        assert.ok( stub.error.calledOnce, 'error should not be called' );

        assert.equal( res, false, 'ajax_startRowIndexFromSession should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
} );
//=============================================================================
QUnit.test( 'browtab_ajax listeners_setting', function ( assert ) {
    expect( 1 );
    var listeners = {};
    listeners.load   = transferSuccess;
    listeners.error  = transferFailed;
    listeners.abort  = transferCanceled;
    var res = listeners_setting( );
    assert.deepEqual( res, listeners, 'listeners_setting should return proper value' );
});
function xhrSuccessHandler( ) {  // function declared in another file
}
function progressHandler( ) {  // function declared in another file
}
function loadEndHandler( ) {  // function declared in another file
}
function defineAbortButton( ) {  // function declared in another file
}
function progressbarShow( ) {  // function declared in another file
}
//=============================================================================
QUnit.module( "browtab_ajax hxr", function( hooks ) { 
    var requests = sinon.requests;
    var done;
    hooks.beforeEach( function( assert ) {
        stub = {};
        csrf_token = $( "#csrfmiddlewaretoken" ).val();
        this.xhr = sinon.useFakeXMLHttpRequest();
        requests = [];
        this.xhr.onCreate = function ( request ) {
            requests.push( request );
        };
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
        this.xhr.restore();
    } );
    QUnit.test( 'transferSuccess 200', function ( assert ) {
        expect( 4 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var sr = {};
        sr.id           = 33;
        var json_string_sr = JSON.stringify( sr );

        stub.xhrSuccessHandler  = sinon.stub( window, "xhrSuccessHandler" );
        stub.xhrErrorHandler    = sinon.stub( window, "xhrErrorHandler" );

        var xhr = new XMLHttpRequest();
        xhr.readyState = 4;
        xhr.status = 200;
        xhr.responseHeaders = { "Content-Type": "application/json" , 'server_response': json_string_sr };

        var res = transferSuccess.call( xhr );  // no need to call transferSuccess, because it is called by xhr.respond

        assert.ok( stub.xhrSuccessHandler.calledOnce, 'xhrSuccessHandler should be called once' );
        assert.ok( stub.xhrSuccessHandler.calledWithExactly( sr ), 'xhrSuccessHandler should be called with arg' );
        assert.notOk( stub.xhrErrorHandler.called, 'xhrErrorHandler should not be called' );
        assert.equal( res, undefined, 'transferSuccess should return undefined' );

        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'transferSuccess 200 1', function ( assert ) {
        expect( 4 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var sr = {};
        sr.id           = 33;
        var json_string_sr = JSON.stringify( sr );

        stub.xhrSuccessHandler  = sinon.stub( window, "xhrSuccessHandler" );
        stub.xhrErrorHandler    = sinon.stub( window, "xhrErrorHandler" );

        var xhr = new XMLHttpRequest();
        xhr.readyState = 1;
        xhr.status = 200;
        xhr.responseHeaders = { "Content-Type": "application/json" , 'server_response': json_string_sr };

        var res = transferSuccess.call( xhr );  // no need to call transferSuccess, because it is called by xhr.respond

        assert.notOk( stub.xhrSuccessHandler.called, 'xhrSuccessHandler should not be called' );
        assert.ok( stub.xhrErrorHandler.called, 'xhrErrorHandler should not be called' );
        assert.ok( stub.xhrErrorHandler.calledWithExactly( xhr ), 'xhrErrorHandler should be called with arg' );
        assert.equal( res, undefined, 'transferSuccess should return undefined' );

        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'transferSuccess 400', function ( assert ) {
        expect( 4 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var sr = {};
        sr.id           = 33;
        var json_string_sr = JSON.stringify( sr );

        stub.xhrSuccessHandler  = sinon.stub( window, "xhrSuccessHandler" );
        stub.xhrErrorHandler    = sinon.stub( window, "xhrErrorHandler" );

        var xhr = new XMLHttpRequest();
        xhr.readyState = 1;
        xhr.status = 200;
        xhr.responseHeaders = { "Content-Type": "application/json" , 'server_response': json_string_sr };

        var res = transferSuccess.call( xhr );  // no need to call transferSuccess, because it is called by xhr.respond

        assert.notOk( stub.xhrSuccessHandler.called, 'xhrSuccessHandler should not be called' );
        assert.ok( stub.xhrErrorHandler.called, 'xhrErrorHandler should not be called' );
        assert.ok( stub.xhrErrorHandler.calledWithExactly( xhr ), 'xhrErrorHandler should be called with arg' );
        assert.equal( res, undefined, 'transferSuccess should return undefined' );

        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'transferSuccessDownload 200', function ( assert ) {
        expect( 6 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var sr = {};
        sr.id           = 33;
        var json_string_sr = JSON.stringify( sr );

        stub.download           = sinon.stub( window, "download" );
        stub.xhrSuccessHandler  = sinon.stub( window, "xhrSuccessHandler" );
        stub.xhrErrorHandler    = sinon.stub( window, "xhrErrorHandler" );

        var xhr = new XMLHttpRequest();
        xhr.readyState = 4;
        xhr.status = 200;
        xhr.responseHeaders = { "Content-Type": "application/json" , 'server_response': json_string_sr };

        var res = transferSuccessDownload.call( xhr );  // no need to call transferSuccess, because it is called by xhr.respond

        assert.ok( stub.download.calledOnce, 'download should be called once' );
        assert.ok( stub.download.calledWithExactly( xhr.response, sr.title ), 'download should be called with arg' );
        assert.ok( stub.xhrSuccessHandler.calledOnce, 'xhrSuccessHandler should be called once' );
        assert.ok( stub.xhrSuccessHandler.calledWithExactly( sr ), 'xhrSuccessHandler should be called with arg' );
        assert.notOk( stub.xhrErrorHandler.called, 'xhrErrorHandler should not be called' );
        assert.equal( res, undefined, 'transferSuccessDownload should return undefined' );

        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'transferSuccessDownload 200 1', function ( assert ) {
        expect( 5 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var sr = {};
        sr.id           = 33;
        var json_string_sr = JSON.stringify( sr );

        stub.download           = sinon.stub( window, "download" );
        stub.xhrSuccessHandler  = sinon.stub( window, "xhrSuccessHandler" );
        stub.xhrErrorHandler    = sinon.stub( window, "xhrErrorHandler" );

        var xhr = new XMLHttpRequest();
        xhr.readyState = 1;
        xhr.status = 200;
        xhr.responseHeaders = { "Content-Type": "application/json" , 'server_response': json_string_sr };

        var res = transferSuccessDownload.call( xhr );  // no need to call transferSuccess, because it is called by xhr.respond

        assert.notOk( stub.download.called, 'download should not be called' );
        assert.notOk( stub.xhrSuccessHandler.called, 'xhrSuccessHandler should not be called' );
        assert.ok( stub.xhrErrorHandler.called, 'xhrErrorHandler should not be called' );
        assert.ok( stub.xhrErrorHandler.calledWithExactly( xhr ), 'xhrErrorHandler should be called with arg' );
        assert.equal( res, undefined, 'transferSuccessDownload should return udefined' );

        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'transferSuccessDownload 400', function ( assert ) {
        expect( 5 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var sr = {};
        sr.id           = 33;
        var json_string_sr = JSON.stringify( sr );

        stub.download           = sinon.stub( window, "download" );
        stub.xhrSuccessHandler  = sinon.stub( window, "xhrSuccessHandler" );
        stub.xhrErrorHandler    = sinon.stub( window, "xhrErrorHandler" );

        var xhr = new XMLHttpRequest();
        xhr.readyState = 4;
        xhr.status = 400;
        xhr.responseHeaders = { "Content-Type": "application/json" , 'server_response': json_string_sr };

        var res = transferSuccessDownload.call( xhr );  // no need to call transferSuccess, because it is called by xhr.respond

        assert.notOk( stub.download.called, 'download should not be called' );
        assert.notOk( stub.xhrSuccessHandler.called, 'xhrSuccessHandler should not be called' );
        assert.ok( stub.xhrErrorHandler.called, 'xhrErrorHandler should not be called' );
        assert.ok( stub.xhrErrorHandler.calledWithExactly( xhr ), 'xhrErrorHandler should be called with arg' );
        assert.equal( res, undefined, 'transferSuccessDownload should return udefined' );

        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'xhr_POST', function ( assert ) {
        expect( 17 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var url = "/folders/ajax-report-download";
        var json_string = JSON.stringify( arr );
        var encoded_json_string = encodeURIComponent( json_string );
        var expected_requestHeaders = {
                "Content-Type"      : "text/plain;charset=utf-8",
                "X-CSRFToken"       : csrf_token,
                "X-client-request"  : encoded_json_string
                };
        var expected_requestBody = undefined;

        var sr = {};
        sr.selRowIndex  = 77;
        sr.model        = 'report';
        sr.id           = 33;
        var arr_sr = {};
        arr_sr.server_response = sr;
        var json_string_sr = JSON.stringify( arr_sr );

        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" , 'server_response': json_string_sr };
        var response_body     = '[77]';

        stub.transferSuccess    = sinon.stub( window, "transferSuccess" );
        stub.transferFailed     = sinon.stub( window, "transferFailed" );
        stub.transferCanceled   = sinon.stub( window, "transferCanceled" );
        stub.progressHandler    = sinon.stub( window, "progressHandler" );
        stub.loadEndHandler     = sinon.stub( window, "loadEndHandler" );
        stub.defineAbortButton  = sinon.stub( window, "defineAbortButton" );
        stub.progressbarShow    = sinon.stub( window, "progressbarShow" );

        var listeners = listeners_setting( );
        var res = xhr_POST( url, encoded_json_string, listeners );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, url, "request should have proper url" );
        assert.equal( requests[0].method, "POST", "request should have proper method" );
        assert.equal( requests[0].async, true, "request should have proper async" );
        assert.equal( requests[0].responseType, 'blob', "request should have proper responseType" );
        assert.deepEqual( requests[0].onprogress, progressHandler, "request should have proper onprogress" );
        assert.deepEqual( requests[0].onloadend, loadEndHandler, "request should have proper onloadend" );
        assert.deepEqual( requests[0].upload.onprogress, progressHandler, "request should have proper upload.onprogress" );
        assert.deepEqual( requests[0].eventListeners.load[1], transferSuccess, "request should have proper on load" );
        assert.deepEqual( requests[0].eventListeners.error[0], transferFailed, "request should have proper on error" );
        assert.deepEqual( requests[0].eventListeners.abort[1], transferCanceled, "request should have proper on abort" );
        assert.deepEqual( requests[0].requestHeaders, expected_requestHeaders, "request should have proper requestHeaders" );
        assert.equal( requests[0].requestBody, expected_requestBody, "request should have proper requestBody" );

	    requests[0].respond( response_status, response_headers, response_body );

        assert.equal( stub.transferSuccess.callCount,  1, 'transferSuccess should be called' );
        assert.equal( stub.transferFailed.callCount,   0, 'transferFailed should not be called' );
        assert.equal( stub.transferCanceled.callCount, 0, 'transferCanceled should not be called' );

        assert.equal( res, undefined, 'xhr_POST should return undefined' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'xhr_POST file', function ( assert ) {
        expect( 17 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var file = "file_content";
        var arr = {'id':55};
        var url = "/folders/ajax-report-upload";
        var json_string = JSON.stringify( arr );
        var encoded_json_string = encodeURIComponent( json_string );
        var expected_requestHeaders = {
                "Content-Type"      : "text/plain;charset=utf-8",
                "X-CSRFToken"       : csrf_token,
                "X-client-request"  : encoded_json_string
                };
        var expected_requestBody = file;

        var sr = {};
        sr.selRowIndex  = 77;
        sr.model        = 'report';
        sr.id           = 33;
        var arr_sr = {};
        arr_sr.server_response = sr;
        var json_string_sr = JSON.stringify( arr_sr );

        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" , 'server_response': json_string_sr };
        var response_body     = '[77]';

        stub.transferSuccess    = sinon.stub( window, "transferSuccess" );
        stub.transferFailed     = sinon.stub( window, "transferFailed" );
        stub.transferCanceled   = sinon.stub( window, "transferCanceled" );
        stub.progressHandler    = sinon.stub( window, "progressHandler" );
        stub.loadEndHandler     = sinon.stub( window, "loadEndHandler" );
        stub.defineAbortButton  = sinon.stub( window, "defineAbortButton" );
        stub.progressbarShow    = sinon.stub( window, "progressbarShow" );

        var listeners = listeners_setting( );
        var res = xhr_POST( url, encoded_json_string, listeners, file );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, url, "request should have proper url" );
        assert.equal( requests[0].method, "POST", "request should have proper method" );
        assert.equal( requests[0].async, true, "request should have proper async" );
        assert.equal( requests[0].responseType, 'blob', "request should have proper responseType" );
        assert.deepEqual( requests[0].onprogress, progressHandler, "request should have proper onprogress" );
        assert.deepEqual( requests[0].onloadend, loadEndHandler, "request should have proper onloadend" );
        assert.deepEqual( requests[0].upload.onprogress, progressHandler, "request should have proper upload.onprogress" );
        assert.deepEqual( requests[0].eventListeners.load[1], transferSuccess, "request should have proper on load" );
        assert.deepEqual( requests[0].eventListeners.error[0], transferFailed, "request should have proper on error" );
        assert.deepEqual( requests[0].eventListeners.abort[1], transferCanceled, "request should have proper on abort" );
        assert.deepEqual( requests[0].requestHeaders, expected_requestHeaders, "request should have proper requestHeaders" );
        assert.equal( requests[0].requestBody, expected_requestBody, "request should have proper requestBody" );

	    requests[0].respond( response_status, response_headers, response_body );

        assert.equal( stub.transferSuccess.callCount,  1, 'transferSuccess should be called' );
        assert.equal( stub.transferFailed.callCount,   0, 'transferFailed should not be called' );
        assert.equal( stub.transferCanceled.callCount, 0, 'transferCanceled should not be called' );

        assert.equal( res, undefined, 'xhr_POST should return undefined' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    // TODO-Make integral test for xhr_POST() to check all listeners
    QUnit.test( 'xhr_POST integral', function ( assert ) {
        expect( 3 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var url = "/folders/ajax-report-download";
        var json_string = JSON.stringify( arr );
        var encoded_json_string = encodeURIComponent( json_string );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;
        var listeners = listeners_setting( );

        var sr = {};
        sr.selRowIndex  = 77;
        sr.model        = 'report';
        sr.id           = 33;
        var arr_sr = {};
        arr_sr.server_response = sr;
        var json_string_sr = JSON.stringify( arr_sr );

        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" , 'server_response': json_string_sr };
        var response_body     = '[77]';

        // Attention! for some functions stub is name for sinon.spy, not sinon.stub
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );
        stub.xhr_POST           = sinon.spy( window, "xhr_POST" );
        // set stub or spy to functions inside xhr_POST, because it's called as spy, not stub!
        stub.progressHandler    = sinon.stub( window, "progressHandler" );
        stub.loadEndHandler     = sinon.stub( window, "loadEndHandler" );
        stub.defineAbortButton  = sinon.stub( window, "defineAbortButton" );
        stub.progressbarShow    = sinon.stub( window, "progressbarShow" );
        stub.transferSuccess    = sinon.spy( window, "transferSuccess" );
        stub.download           = sinon.spy( window, "download" );
        stub.xhrSuccessHandler  = sinon.stub( window, "xhrSuccessHandler" );
        stub.xhrErrorHandler    = sinon.stub( window, "xhrErrorHandler" );

        var res = xhr_POST( url, encoded_json_string, listeners );

//        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
//        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
//        assert.ok( stub.xhr_POST.calledOnce, 'xhr_POST should be called once' );
//        assert.ok( stub.xhr_POST.calledWithExactly( url, encoded_json_string ), 'xhr_POST should be called with arg' );
/*
        assert.equal( as.url, expected_url, 'function should set as.url' );
        assert.deepEqual( as.data, {
                                    client_request : json_string,
                                    csrfmiddlewaretoken: csrf_token
                                    }, 
                                    'function should set as.data' );
*/
//        assert.equal( as.success, ajax_FoldersTreeFromBase_success_handler, 'function should set as.success' );
//        assert.equal( as.error,   ajax_FoldersTreeFromBase_error_handler, 'function should set as.error' );

        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

console.log('stub.xhr_POST:-------------------------');
console.log('args =', stub.xhr_POST.args);
console.log('returnValues', stub.xhr_POST.returnValues);
console.log('stub.transferSuccess:-------------------------');
console.log('args =', stub.transferSuccess.args);
console.log('returnValues', stub.transferSuccess.returnValues);
//        assert.ok( stub.success.calledOnce, 'success should be called once' );
//        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, undefined, 'xhr_POST should return undefined' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
} );
//=============================================================================
