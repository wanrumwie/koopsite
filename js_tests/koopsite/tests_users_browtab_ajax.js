/*
Global:  $ (?), JSON (?), QUnit (?), ajaxSuccessHandler (?), ajax_activateAccount (?), ajax_activateAllAccounts (?), ajax_deactivateAccount (?), ajax_deleteAccount (?), ajax_denyAccount (?), ajax_denyMemberAccount (?), ajax_recognizeAccount (?), ajax_setMemberAccount (?), ajax_setMemberAllAccounts (?), csrf_token (?), dialogMessage, dialog_box_form_close, expect (?), getAllElementsArr (?), getSelElementArr (?), qs_TR_arr (?), selElement (?), set0_qs_TR_arr, sinon (?), stub, window (?), xhrErrorHandler (?), xhrSuccessHandler (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test
//=============================================================================
function dialogMessage( a,b,c,d ){  // function declared in another file
}
function dialog_box_form_close(){  // function declared in another file
}
QUnit.module( "users_browtab_ajax handlers", function( hooks ) { 
    var sr;
    hooks.beforeEach( function( assert ) {
        stub = {};
        sr = {};
        sr.message  = 'qwerty';
        sr.type     = '';
        sr.title    = 'title';
        var ob = {};
        ob.model  = 'user';  
        ob.id     = 555;
        ob.name   = 'Lennon John';
        sr.changes  = [ob, 'john', 'Lennon', '', 'e@mail.com', '11.01.2016', undefined, true, false];
        sr.supplement = {};
        sr.supplement.iconPath = [];
        sr.supplement.iconPath[6] = "/static/admin/img/icon-unknown.gif";
        sr.supplement.iconPath[7] = "/static/admin/img/icon-yes.gif";
        sr.supplement.iconPath[8] = "/static/admin/img/icon-no.gif";
        
        stub.dialogMessage          = sinon.stub( window, "dialogMessage" );
        stub.dialog_box_form_close  = sinon.stub( window, "dialog_box_form_close" );
        stub.changeSelElement       = sinon.stub( window, "changeSelElement" );
        stub.changeAllElements      = sinon.stub( window, "changeAllElements" );
        stub.deleteElement          = sinon.stub( window, "deleteElement" );

    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'ajaxSuccessHandler', function ( assert ) {
        expect( 3 );
        stub.xhrSuccessHandler = sinon.stub( window, "xhrSuccessHandler" );
        var res = ajaxSuccessHandler( sr );
        assert.ok( stub.xhrSuccessHandler.calledOnce, 'xhrSuccessHandler should be called once' );
        assert.ok( stub.xhrSuccessHandler.calledWithExactly( sr ), 'xhrSuccessHandler should be called with arg' );
        assert.equal( res, undefined, 'ajaxSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler IncorrectData', function ( assert ) {
        expect( 7 );

        sr.type = 'IncorrectData';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.notOk( stub.dialog_box_form_close.called, 'dialog_box_form_close should be not called' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.changeAllElements.called, 'changeAllElements should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler Error', function ( assert ) {
        expect( 8 );

        sr.type = 'Error';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.changeAllElements.called, 'changeAllElements should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler Forbidden', function ( assert ) {
        expect( 8 );

        sr.type = 'Forbidden';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.changeAllElements.called, 'changeAllElements should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler Normal', function ( assert ) {
        expect( 8 );

        sr.type = 'Normal';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.changeAllElements.called, 'changeAllElements should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler NoChange', function ( assert ) {
        expect( 8 );

        sr.type = 'NoChange';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.changeAllElements.called, 'changeAllElements should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler Rename', function ( assert ) {
        expect( 8 );

        sr.type = 'Rename';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.changeAllElements.called, 'changeAllElements should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler Group', function ( assert ) {
        expect( 9 );

        sr.type = 'Group';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.ok( stub.changeAllElements.calledOnce, 'changeAllElements should be called once' );
        assert.ok( stub.changeAllElements.calledWithExactly( sr.group ), 'changeAllElements should be called with args' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler Change', function ( assert ) {
        expect( 9 );

        sr.type = 'Change';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.changeAllElements.called, 'changeAllElements should be not called' );
        assert.ok( stub.changeSelElement.calledOnce, 'changeSelElement should be called once' );
        assert.ok( stub.changeSelElement.calledWithExactly( sr.changes, sr.supplement ), 
                                                    'changeSelElement should be called with args' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler DeleteRow', function ( assert ) {
        expect( 9 );

        sr.type = 'DeleteRow';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.changeAllElements.called, 'changeAllElements should be not called' );
        assert.ok( stub.deleteElement.called, 'deleteElement should be called once' );
        assert.ok( stub.deleteElement.calledWithExactly( ), 'deleteElement should be called with args' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
    QUnit.test( 'xhrSuccessHandler unknown', function ( assert ) {
        expect( 8 );

        sr.type = 'unknown';

        var res = xhrSuccessHandler( sr );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( sr.message, sr.type, sr.title, 2000 ), 
                                                                        'dialogMessage should be called with args' );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 'dialog_box_form_close should be called with args' );
        assert.notOk( stub.changeSelElement.called, 'changeSelElement should be not called' );
        assert.notOk( stub.changeAllElements.called, 'changeAllElements should be not called' );
        assert.notOk( stub.deleteElement.called, 'deleteElement should be not called' );

        assert.equal( res, undefined, 'xhrSuccessHandler should return undefined' );
    });
} );
//=============================================================================
QUnit.test( 'getSelElementArr', function ( assert ) {
    expect( 1 );
    // set fake values to fixture:
    document.getElementById("browTabName").value = "browTabName";
    document.getElementById("selRowIndex").value = "selRowIndex";
    browtab_document_ready_handler();
    selElement.model = 'users';
    selElement.id    = 55;
    selElement.name  = 'name';
    var arr = {};
    arr.browTabName = "browTabName";
    arr.parent_id   = "";
    arr.selRowIndex = "selRowIndex";
    arr.sendMail    = undefined;
    arr.model       = 'users';
    arr.id          = 55;
    arr.name        = 'name';
    
    var res = getSelElementArr( );

    assert.deepEqual( res, arr, 'getSelElementArr should return prorer value' );
    });
//=============================================================================
/********************************************************************/
function set0_qs_TR_arr() {
    // helper function to fill qs_TR_arr by sample values:
    var i, j, ob, TR;
    var arr = [];   // 2D array - table
    for ( i = 0 ; i < 10 ; i++ ) {
        arr[i] = [];
        TR = "TR";
        ob = {};
        ob.TR     = TR;  // add DOM TR object to array as 0th column 
        ob.model  = "model";  
        ob.id     = "id";
        ob.name   = "name";
        arr[i][0] = ob;
        for ( j = 1 ; j <= 8; j++ ) {
            arr[i][j] = i * 10 + j;
        }
    }
    return arr;
}
/********************************************************************/
QUnit.test('self test: set sample values to qs_TR_arr', function ( assert ) {
    expect( 8 * 10 );
    var qs_TR_arr = set0_qs_TR_arr();
    var i, j;
    for ( i = 0 ; i < 10 ; i++ ) {
        for ( j = 1 ; j <= 8; j++ ) {
            assert.strictEqual( qs_TR_arr[i][j], i * 10 + j, 'row value');
        }
    }
});
QUnit.test('self test: set sample values to qs_TR_arr[i][0] objects', function ( assert ) {
    expect( 4 * 10 );
    var qs_TR_arr = set0_qs_TR_arr();
    var i;
    for ( i = 0 ; i < 10 ; i++ ) {
        assert.strictEqual( qs_TR_arr[i][0].TR,     "TR",    'object element');
        assert.strictEqual( qs_TR_arr[i][0].model,  "model", 'object element');
        assert.strictEqual( qs_TR_arr[i][0].id,     "id",    'object element');
        assert.strictEqual( qs_TR_arr[i][0].name,   "name",  'object element');
    }
});
/********************************************************************/
QUnit.test( 'getAllElementsArr', function ( assert ) {
    expect( 1 );
    // set fake values to fixture:
    document.getElementById("browTabName").value = "browTabName";
    document.getElementById("selRowIndex").value = "selRowIndex";
    var arr = {};
    var elemSet = [];
    var elem = {};
    arr.browTabName = "browTabName";
    arr.parent_id   = "";
    arr.selRowIndex = "selRowIndex";
    arr.sendMail    = undefined;
    var i;
    for ( i=0 ; i<10; i++ ) {
        elem = {};
        elem.id    = 'id';
        elem.model = 'model';
        elem.name  = i * 10 + 1;       // get value from 1-st column
        elemSet[i] = elem;
    }
    arr.elemSet = elemSet;

    qs_TR_arr = set0_qs_TR_arr();
    
    var res = getAllElementsArr( );

    assert.deepEqual( res, arr, 'getAllElementsArr should return prorer value' );
    });
//=============================================================================
QUnit.module( "users_browtab_ajax ajax", function( hooks ) { 
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
    QUnit.test( 'ajax_activateAllAccounts success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/adm/users/ajax-activate-all-accounts";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getAllElementsArr   = sinon.stub( window, "getAllElementsArr" ).returns( arr );

        var res = ajax_activateAllAccounts( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getAllElementsArr.calledOnce, 'getAllElementsArr should be called once' );
        assert.ok( stub.getAllElementsArr.calledWithExactly( ), 'getAllElementsArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_activateAllAccounts should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_activateAllAccounts error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/adm/users/ajax-activate-all-accounts";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getAllElementsArr   = sinon.stub( window, "getAllElementsArr" ).returns( arr );

        var res = ajax_activateAllAccounts( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getAllElementsArr.calledOnce, 'getAllElementsArr should be called once' );
        assert.ok( stub.getAllElementsArr.calledWithExactly( ), 'getAllElementsArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_activateAllAccounts should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_setMemberAllAccounts success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/adm/users/ajax-set-member-all-accounts";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getAllElementsArr   = sinon.stub( window, "getAllElementsArr" ).returns( arr );

        var res = ajax_setMemberAllAccounts( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getAllElementsArr.calledOnce, 'getAllElementsArr should be called once' );
        assert.ok( stub.getAllElementsArr.calledWithExactly( ), 'getAllElementsArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_setMemberAllAccounts should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_setMemberAllAccounts error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/adm/users/ajax-set-member-all-accounts";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getAllElementsArr   = sinon.stub( window, "getAllElementsArr" ).returns( arr );

        var res = ajax_setMemberAllAccounts( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getAllElementsArr.calledOnce, 'getAllElementsArr should be called once' );
        assert.ok( stub.getAllElementsArr.calledWithExactly( ), 'getAllElementsArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_setMemberAllAccounts should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_recognizeAccount success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/adm/users/ajax-recognize-account";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_recognizeAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_recognizeAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_recognizeAccount error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/adm/users/ajax-recognize-account";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_recognizeAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_recognizeAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_denyAccount success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/adm/users/ajax-deny-account";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_denyAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_denyAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_denyAccount error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55, 'name':'New name'};
        var expected_url = "/adm/users/ajax-deny-account";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_denyAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_denyAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_activateAccount success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/adm/users/ajax-activate-account";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_activateAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_activateAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_activateAccount error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/adm/users/ajax-activate-account";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_activateAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_activateAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_deactivateAccount success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/adm/users/ajax-deactivate-account";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_deactivateAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_deactivateAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_deactivateAccount error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/adm/users/ajax-deactivate-account";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_deactivateAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_deactivateAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_setMemberAccount success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/adm/users/ajax-set-member-account";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_setMemberAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_setMemberAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_setMemberAccount error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/adm/users/ajax-set-member-account";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_setMemberAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_setMemberAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_denyMemberAccount success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/adm/users/ajax-deny-member-account";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_denyMemberAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_denyMemberAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_denyMemberAccount error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/adm/users/ajax-deny-member-account";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_denyMemberAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_denyMemberAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_deleteAccount success', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/adm/users/ajax-delete-account";
        var response_status   = 200; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_deleteAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.ok( stub.success.calledOnce, 'success should be called once' );
        assert.notOk( stub.error.called, 'error should not be called' );

        assert.equal( res, false, 'ajax_deleteAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
    QUnit.test( 'ajax_deleteAccount error', function ( assert ) {
        expect( 11 );
        done = assert.async();  // Instruct QUnit to wait for an asynchronous operation. 
        var arr = {'id':55};
        var expected_url = "/adm/users/ajax-delete-account";
        var response_status   = 400; 
        var response_headers  = { "Content-Type": "application/json" };
        var response_body     = '[77]';

        var json_string = JSON.stringify( arr );
        var expected_requestBody = "client_request=" + json_string + "+&csrfmiddlewaretoken=" + csrf_token;

        // Attention! in this place stub is name for sinon.spy, not sinon.stub
        stub.ajax               = sinon.spy( $, "ajax" );
        stub.ajax_settings      = sinon.spy( window, "ajax_settings" );
        stub.success            = sinon.stub( window, "ajaxSuccessHandler" );
        stub.error              = sinon.stub( window, "xhrErrorHandler" );
        stub.getSelElementArr   = sinon.stub( window, "getSelElementArr" ).returns( arr );

        var res = ajax_deleteAccount( );

        var expected_as = {};
        expected_as.type    = "POST";
        expected_as.dataType= "json";
        expected_as.url = expected_url;
        expected_as.data = {
                            client_request : json_string,
                            csrfmiddlewaretoken: csrf_token
        };
        expected_as.success = ajaxSuccessHandler;
        expected_as.error   = xhrErrorHandler;

        assert.ok( stub.getSelElementArr.calledOnce, 'getSelElementArr should be called once' );
        assert.ok( stub.getSelElementArr.calledWithExactly( ), 'getSelElementArr should be called with arg' );
        assert.ok( stub.ajax_settings.calledOnce, 'ajax_settings should be called once' );
        assert.ok( stub.ajax_settings.calledWithExactly( ), 'ajax_settings should be called with arg' );
        assert.ok( stub.ajax.calledOnce, 'ajax should be called once' );
        assert.ok( stub.ajax.calledWithExactly( expected_as ), 'ajax should be called with arg' );
        assert.equal( requests.length, 1 , "requests length should be 1" );
        assert.equal( requests[0].url, expected_url, "request should have proper url" );
		
	    requests[0].respond( response_status, response_headers, response_body );

        assert.notOk( stub.success.called, 'success should not be called' );
        assert.ok( stub.error.calledOnce, 'error should be called' );

        assert.equal( res, false, 'ajax_deleteAccount should return false' );
        done(); // start QUnit runner after it was keep waiting until async operations executed. 
    });
} );
//=============================================================================
