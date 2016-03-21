/*
Global:  $ (?), QUnit (?), add_users_browtab_ui_buttons (?), ajax_activateAccount (?), ajax_activateAllAccounts (?), ajax_deactivateAccount (?), ajax_deleteAccount (?), ajax_denyAccount (?), ajax_denyMemberAccount (?), ajax_recognizeAccount (?), ajax_setMemberAccount (?), ajax_setMemberAllAccounts (?), button_activate_account_handler (?), button_activate_all_handler (?), button_deactivate_account_handler (?), button_delete_account_handler (?), button_deny_account_handler (?), button_deny_member_account_handler (?), button_recognize_account_handler (?), button_set_member_account_handler (?), button_set_member_all_handler (?), expect (?), jQuery (?), rowsNumber (?), selRowIndex (?), set_users_browtab_ui_buttons_listeners (?), sinon (?), stub, users_browtab_ui_document_ready_handler (?), window (?)
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

/*
QUnit.test( 'js file start assignments', function ( assert ) {
    expect( 4 );
    assert.deepEqual( TR_start, [], 'array for storing <tr> data immediately after page loaded');
    assert.deepEqual( selElement, {}, 'object = selElement.model , selElement.id , selElement.name');
    assert.equal( selectStyle, "selected", 'CSS style for selected row');
    assert.equal( normalStyle, "normal", 'CSS style for unselected row');
});
*/
//=============================================================================
QUnit.module( "users_browtab_ui document ready", function( hooks ) { 
    var $buttons;
    var handlers;
    var primary_icons;
    var secondary_icons;
    hooks.beforeEach( function( assert ) {
        stub = {};
        $buttons = [
            $( "#button-activate-all"       ),
            $( "#button-set-member-all"     ),
            $( "#button-recognize-account"  ),
            $( "#button-deny-account"       ),
            $( "#button-activate-account"   ),
            $( "#button-deactivate-account" ),
            $( "#button-set-member-account" ),
            $( "#button-deny-member-account"),
            $( "#button-delete-account"     )
        ];
        handlers = [
            button_activate_all_handler       ,
            button_set_member_all_handler     ,
            button_recognize_account_handler  ,
            button_deny_account_handler       ,
            button_activate_account_handler   ,
            button_deactivate_account_handler ,
            button_set_member_account_handler ,
            button_deny_member_account_handler,
            button_delete_account_handler
        ];
        primary_icons = [
            "ui-icon-unlocked",
            "ui-icon-person",
            "ui-icon-check",
            "ui-icon-cancel",
            "ui-icon-unlocked",
            "ui-icon-locked",
            "ui-icon-person",
            "ui-icon-cancel",
            "ui-icon-trash"
        ];
        secondary_icons = [
            "ui-icon-folder-collapsed",
            "ui-icon-folder-collapsed",
            "ui-icon-tag",
            "ui-icon-tag",
            "ui-icon-tag",
            "ui-icon-tag",
            "ui-icon-tag",
            "ui-icon-tag",
            "ui-icon-tag"
        ];
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'users_browtab_ui_document_ready_handler', function ( assert ) {
        expect( 5 );

        stub.add_users_browtab_ui_buttons = sinon.stub( window, "add_users_browtab_ui_buttons" );
        stub.set_users_browtab_ui_buttons_listeners = sinon.stub( window, "set_users_browtab_ui_buttons_listeners" );

        var res = users_browtab_ui_document_ready_handler( );

        assert.ok( stub.add_users_browtab_ui_buttons.calledOnce, 
                                                        'add_users_browtab_ui_buttons should be called once' );
        assert.ok( stub.add_users_browtab_ui_buttons.calledWithExactly( ), 
                                                        'add_users_browtab_ui_buttons should be called with arg' );
        assert.ok( stub.set_users_browtab_ui_buttons_listeners.calledOnce, 
                                                        'set_users_browtab_ui_buttons_listeners should be called once' );
        assert.ok( stub.set_users_browtab_ui_buttons_listeners.calledWithExactly( ), 
                                                        'set_users_browtab_ui_buttons_listeners should be called with arg' );

        assert.equal( res, undefined, 'users_browtab_ui_document_ready_handler should return false' );
    });
    QUnit.test( 'add_users_browtab_ui_buttons', function ( assert ) {
        expect( 29 );

        stub.button = sinon.stub( jQuery.prototype, "button" );

        var res = add_users_browtab_ui_buttons( );

        assert.equal( stub.button.callCount, 9, 'button should be called 9 times' );
        var i;
        for ( i=0 ; i<9 ; i++ ){
            assert.deepEqual( stub.button.thisValues[i], $buttons[i], i+': button called as method of proper this' );
            assert.deepEqual( stub.button.args[i][0].icons.primary, primary_icons[i], i+': button called with proper args' );
            assert.deepEqual( stub.button.args[i][0].icons.secondary, secondary_icons[i],i+': button called with proper args' );
        }

        assert.equal( res, undefined, 'add_users_browtab_ui_buttons should return false' );
    });
    QUnit.test( 'set_users_browtab_ui_buttons_listeners', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 39 );

        stub.off = sinon.spy( jQuery.prototype, "off" );
        stub.on  = sinon.spy( jQuery.prototype, "on" );

        var res = set_users_browtab_ui_buttons_listeners( );

        assert.equal( stub.off.callCount, 9, 'off should be called 9 times' );
        assert.equal( stub.on.callCount, 9, 'on should be called 9 times' );

        var i;
        for ( i=0 ; i<9 ; i++ ){
            assert.deepEqual( stub.off.thisValues[i], $buttons[i], i+': off called as method of proper this' );
            assert.deepEqual( stub.on.thisValues[i], $buttons[i], i+': on called as method of proper this' );
            assert.ok( stub.off.getCall( i ).calledWithExactly( "click" ), i+':on called with args' );
            assert.ok( stub.on.getCall( i ).calledWithExactly( "click", handlers[i] ), i+': off called with proper args' );
        }

        assert.equal( res, undefined, 'set_users_browtab_ui_buttons_listeners should return false' );
    });
} );
//=============================================================================
QUnit.module( "users_browtab_ui button handlers", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        selRowIndex = 55;
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'button_activate_all_handler', function ( assert ) {
        expect( 5 );
        var ajax_Function   = ajax_activateAllAccounts; 
        var dialogTitle     = "Активація ВСІХ обраних акаунтів";
        var inputLabel      = "Активувати";
        var disabledInput   = true;
        var inputVal        = rowsNumber + " акаунтів";
        var condLabel       = "Повідомити ч/з email";
        var condVal         = true;
        var confirmTitle    = "Групова дія";
        var confirmMsg      = "Ви намагаєтеся активувати одразу " + 
                                        rowsNumber + " акаунтів. Ви впевнені?";
        var selectionCheck  = "selectionCheck";
        
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_activate_all_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_activate_all_handler should return false' );
    });
    QUnit.test( 'button_set_member_all_handler', function ( assert ) {
        expect( 5 );
        var ajax_Function   = ajax_setMemberAllAccounts;
        var dialogTitle     =
            "Прова доступу члена кооперативу для ВСІХ обраних акаунтів";
        var inputLabel      = "Надати";
        var disabledInput   = true;
        var inputVal        = rowsNumber + " акаунтів";
        var condLabel       = "Повідомити ч/з email";
        var condVal         = true;
        var confirmTitle    = "Групова дія";
        var confirmMsg      = "Ви намагаєтеся надати права доступу одразу " +
                                        rowsNumber + " акаунтів. Ви впевнені?";
        var selectionCheck  = "selectionCheck";
        
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_set_member_all_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_set_member_all_handler should return false' );
    });
    QUnit.test( 'button_recognize_account_handler', function ( assert ) {
        expect( 7 );
        var ajax_Function   = ajax_recognizeAccount;
        var dialogTitle     = "Підтвердження акаунту";
        var inputLabel      = "Підтвердити";
        var disabledInput   = true;
        var inputVal        = "getLoginNameFlatbyIndex( selRowIndex )";
        var condLabel       = "Повідомити ч/з email";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";

        stub.getLoginNameFlatbyIndex = sinon.stub( window, "getLoginNameFlatbyIndex" ).returns( inputVal );
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_recognize_account_handler( );
        
        assert.ok( stub.getLoginNameFlatbyIndex.calledOnce, 'getLoginNameFlatbyIndex should be called once' );
        assert.ok( stub.getLoginNameFlatbyIndex.calledWithExactly( selRowIndex ), 'getLoginNameFlatbyIndex arg' );
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_recognize_account_handler should return false' );
    });
    QUnit.test( 'button_deny_account_handler', function ( assert ) {
        expect( 7 );
        var ajax_Function   = ajax_denyAccount;
        var dialogTitle     = "Відмова підтвердження акаунту";
        var inputLabel      = "Відмовити";
        var disabledInput   = true;
        var inputVal        = "getLoginNameFlatbyIndex( selRowIndex )";
        var condLabel       = "Повідомити ч/з email";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.getLoginNameFlatbyIndex = sinon.stub( window, "getLoginNameFlatbyIndex" ).returns( inputVal );
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_deny_account_handler( );
        
        assert.ok( stub.getLoginNameFlatbyIndex.calledOnce, 'getLoginNameFlatbyIndex should be called once' );
        assert.ok( stub.getLoginNameFlatbyIndex.calledWithExactly( selRowIndex ), 'getLoginNameFlatbyIndex arg' );
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_deny_account_handler should return false' );
    });
    QUnit.test( 'button_activate_account_handler', function ( assert ) {
        expect( 7 );
        var ajax_Function   = ajax_activateAccount;
        var dialogTitle     = "Активація акаунту";
        var inputLabel      = "Активувати";
        var disabledInput   = true;
        var inputVal        = "getLoginNameFlatbyIndex( selRowIndex )";
        var condLabel       = "Повідомити ч/з email";
        var condVal         = true;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.getLoginNameFlatbyIndex = sinon.stub( window, "getLoginNameFlatbyIndex" ).returns( inputVal );
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_activate_account_handler( );
        
        assert.ok( stub.getLoginNameFlatbyIndex.calledOnce, 'getLoginNameFlatbyIndex should be called once' );
        assert.ok( stub.getLoginNameFlatbyIndex.calledWithExactly( selRowIndex ), 'getLoginNameFlatbyIndex arg' );
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_activate_account_handler should return false' );
    });
    QUnit.test( 'button_deactivate_account_handler', function ( assert ) {
        expect( 7 );
        var ajax_Function   = ajax_deactivateAccount;
        var dialogTitle     = "Деактивація акаунту";
        var inputLabel      = "Деактивувати";
        var disabledInput   = true;
        var inputVal        = "getLoginNameFlatbyIndex( selRowIndex )";
        var condLabel       = "Повідомити ч/з email";
        var condVal         = true;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.getLoginNameFlatbyIndex = sinon.stub( window, "getLoginNameFlatbyIndex" ).returns( inputVal );
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_deactivate_account_handler( );
        
        assert.ok( stub.getLoginNameFlatbyIndex.calledOnce, 'getLoginNameFlatbyIndex should be called once' );
        assert.ok( stub.getLoginNameFlatbyIndex.calledWithExactly( selRowIndex ), 'getLoginNameFlatbyIndex arg' );
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_deactivate_account_handler should return false' );
    });
    QUnit.test( 'button_set_member_account_handler', function ( assert ) {
        expect( 7 );
        var ajax_Function   = ajax_setMemberAccount;
        var dialogTitle     = "Права доступу члена кооперативу";
        var inputLabel      = "Надати";
        var disabledInput   = true;
        var inputVal        = "getLoginNameFlatbyIndex( selRowIndex )";
        var condLabel       = "Повідомити ч/з email";
        var condVal         = true;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.getLoginNameFlatbyIndex = sinon.stub( window, "getLoginNameFlatbyIndex" ).returns( inputVal );
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_set_member_account_handler( );
        
        assert.ok( stub.getLoginNameFlatbyIndex.calledOnce, 'getLoginNameFlatbyIndex should be called once' );
        assert.ok( stub.getLoginNameFlatbyIndex.calledWithExactly( selRowIndex ), 'getLoginNameFlatbyIndex arg' );
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_set_member_account_handler should return false' );
    });
    QUnit.test( 'button_deny_member_account_handler', function ( assert ) {
        expect( 7 );
        var ajax_Function   = ajax_denyMemberAccount;
        var dialogTitle     = "Права доступу члена кооперативу";
        var inputLabel      = "Вилучити";
        var disabledInput   = true;
        var inputVal        = "getLoginNameFlatbyIndex( selRowIndex )";
        var condLabel       = "Повідомити ч/з email";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.getLoginNameFlatbyIndex = sinon.stub( window, "getLoginNameFlatbyIndex" ).returns( inputVal );
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_deny_member_account_handler( );
        
        assert.ok( stub.getLoginNameFlatbyIndex.calledOnce, 'getLoginNameFlatbyIndex should be called once' );
        assert.ok( stub.getLoginNameFlatbyIndex.calledWithExactly( selRowIndex ), 'getLoginNameFlatbyIndex arg' );
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_deny_member_account_handler should return false' );
    });
    QUnit.test( 'button_delete_account_handler', function ( assert ) {
        expect( 7 );
        var ajax_Function   = ajax_deleteAccount;
        var dialogTitle     = "Видалення акаунту";
        var inputLabel      = "Видалити";
        var disabledInput   = true;
        var inputVal        = "getLoginNameFlatbyIndex( selRowIndex )";
        var condLabel       = "";
        var condVal         = false;
        var confirmTitle    = "Видалення акаунту";
        var confirmMsg      = "Замість видалення акаунт краще деактивувати. " +
                                                                "Ви наполягаєте на видаленні?";
        var selectionCheck  = "selectionCheck";
        
        stub.getLoginNameFlatbyIndex = sinon.stub( window, "getLoginNameFlatbyIndex" ).returns( inputVal );
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_delete_account_handler( );
        
        assert.ok( stub.getLoginNameFlatbyIndex.calledOnce, 'getLoginNameFlatbyIndex should be called once' );
        assert.ok( stub.getLoginNameFlatbyIndex.calledWithExactly( selRowIndex ), 'getLoginNameFlatbyIndex arg' );
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_delete_account_handler should return false' );
    });
} );
//=============================================================================
