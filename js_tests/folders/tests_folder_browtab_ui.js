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
QUnit.module( "folder_browtab_ui document ready", function( hooks ) { 
    var $buttons;
    var handlers;
    var primary_icons;
    var secondary_icons;
    hooks.beforeEach( function( assert ) {
        stub = {};
        $buttons = [
            $( "#button-create-folder"      ),
            $( "#button-upload-report"      ),
            $( "#button-download-element"   ),
            $( "#button-rename-element"     ),
            $( "#button-move-element"       ),
            $( "#button-delete-element"     )
        ];
        handlers = [
            button_create_folder_handler,
            button_upload_report_handler,
            button_download_element_handler,
            button_rename_element_handler,
            button_move_element_handler,
            button_delete_element_handler
        ];
        primary_icons = [
            "ui-icon-plus",
            "ui-icon-arrowthickstop-1-n",
            "ui-icon-arrowthickstop-1-s",
            "ui-icon-pencil",
            "ui-icon-cart",
            "ui-icon-trash"
        ];
        secondary_icons = [
            "ui-icon-folder-collapsed",
            "ui-icon-document",
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
    QUnit.test( 'folder_browtab_ui_document_ready_handler', function ( assert ) {
        expect( 7 );

        stub.add_folder_browtab_ui_buttons = sinon.stub( window, "add_folder_browtab_ui_buttons" );
        stub.set_folder_browtab_ui_buttons_listeners = sinon.stub( window, "set_folder_browtab_ui_buttons_listeners" );
        stub.add_tree_dialog = sinon.stub( window, "add_tree_dialog" );

        var res = folder_browtab_ui_document_ready_handler( );

        assert.ok( stub.add_folder_browtab_ui_buttons.calledOnce, 
                                                        'add_folder_browtab_ui_buttons should be called once' );
        assert.ok( stub.add_folder_browtab_ui_buttons.calledWithExactly( ), 
                                                        'add_folder_browtab_ui_buttons should be called with arg' );
        assert.ok( stub.set_folder_browtab_ui_buttons_listeners.calledOnce, 
                                                        'set_folder_browtab_ui_buttons_listeners should be called once' );
        assert.ok( stub.set_folder_browtab_ui_buttons_listeners.calledWithExactly( ), 
                                                        'set_folder_browtab_ui_buttons_listeners should be called with arg' );
        assert.ok( stub.add_tree_dialog.calledOnce, 
                                                        'add_tree_dialog should be called once' );
        assert.ok( stub.add_tree_dialog.calledWithExactly( ), 
                                                        'add_tree_dialog should be called with arg' );

        assert.equal( res, undefined, 'folder_browtab_ui_document_ready_handler should return false' );
    });
    QUnit.test( 'add_folder_browtab_ui_buttons', function ( assert ) {
        expect( 20 );

        stub.button = sinon.stub( jQuery.prototype, "button" );

        var res = add_folder_browtab_ui_buttons( );

        assert.equal( stub.button.callCount, 6, 'button should be called 6 times' );
        var i;
        for ( i=0 ; i<6 ; i++ ){
            assert.deepEqual( stub.button.thisValues[i], $buttons[i], i+': button called as method of proper this' );
            assert.deepEqual( stub.button.args[i][0].icons.primary, primary_icons[i], i+': button called with proper args' );
            assert.deepEqual( stub.button.args[i][0].icons.secondary, secondary_icons[i],i+': button called with proper args' );
        }
        assert.equal( res, undefined, 'add_folder_browtab_ui_buttons should return false' );
    });
    QUnit.test( 'set_folder_browtab_ui_buttons_listeners', function ( assert ) {
        // Attention! in this test stub is name for sinon.spy, not sinon.stub
        expect( 27 );

        stub.off = sinon.spy( jQuery.prototype, "off" );
        stub.on  = sinon.spy( jQuery.prototype, "on" );

        var res = set_folder_browtab_ui_buttons_listeners( );

        assert.equal( stub.off.callCount, 6, 'off should be called 6 times' );
        assert.equal( stub.on.callCount, 6, 'on should be called 6 times' );

        var i;
        for ( i=0 ; i<6 ; i++ ){
            assert.deepEqual( stub.off.thisValues[i], $buttons[i], i+': off called as method of proper this' );
            assert.deepEqual( stub.on.thisValues[i], $buttons[i], i+': on called as method of proper this' );
            assert.ok( stub.off.getCall( i ).calledWithExactly( "click" ), i+':off called with args' );
            assert.ok( stub.on.getCall( i ).calledWithExactly( "click", handlers[i] ), i+': on called with proper args' );
        }
        assert.equal( res, undefined, 'set_folder_browtab_ui_buttons_listeners should return false' );
    });
} );
//=============================================================================
QUnit.module( "folder_browtab_ui button handlers", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        selElement = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'button_create_folder_handler', function ( assert ) {
        expect( 5 );
        var ajax_Function   = ajax_folderCreate; 
        var dialogTitle     = "Нова тека";
        var inputLabel      = "Назва теки";
        var disabledInput   = false;
        var inputVal        = "Тека без назви";
        var condLabel       = "";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_create_folder_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_create_folder_handler should return false' );
    });
    QUnit.test( 'button_upload_report_handler', function ( assert ) {
        expect( 5 );
        var ajax_Function   = xhr_reportUpload; 
        var dialogTitle     = "Заладувати файл";
        var inputLabel      = "Назва файла";
        var disabledInput   = false;
        var inputVal        = "Тека без назви";
        var condLabel       = "";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        var inputType       = 'file';
        
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_upload_report_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck,
                            inputType ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_upload_report_handler should return false' );
    });
    QUnit.test( 'button_download_element_handler folder', function ( assert ) {
        expect( 5 );
        selElement.model = "folder";
        selElement.name = "NAME";

        var ajax_Function   = xhr_folderDownload;
        var dialogTitle     = "Завантаження теки";
        var inputLabel      = "Завантажити";
        var disabledInput   = true;
        var inputVal        = "NAME";
        var condLabel       = "";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_download_element_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.deepEqual( stub.buttonClickHandler.args[0], [ ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ], 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_download_element_handler should return false' );
    });
    QUnit.test( 'button_download_element_handler report', function ( assert ) {
        expect( 5 );
        selElement.model = "report";
        selElement.name = "NAME";

        var ajax_Function   = xhr_reportDownload;
        var dialogTitle     = "Завантаження файла";
        var inputLabel      = "Завантажити";
        var disabledInput   = true;
        var inputVal        = "NAME";
        var condLabel       = "";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_download_element_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_download_element_handler should return false' );
    });
    QUnit.test( 'button_rename_element_handler folder', function ( assert ) {
        expect( 5 );
        selElement.model = "folder";
        selElement.name = "NAME";

        var ajax_Function   = ajax_folderRename;
        var dialogTitle     = "Перейменування теки";
        var inputLabel      = "Нова назва";
        var disabledInput   = false;
        var inputVal        = "NAME";
        var condLabel       = "";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_rename_element_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_rename_element_handler should return false' );
    });
    QUnit.test( 'button_rename_element_handler report', function ( assert ) {
        expect( 5 );
        selElement.model = "report";
        selElement.name = "NAME";

        var ajax_Function   = ajax_reportRename;
        var dialogTitle     = "Перейменування файла";
        var inputLabel      = "Нова назва";
        var disabledInput   = false;
        var inputVal        = "NAME";
        var condLabel       = "";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_rename_element_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.deepEqual( stub.buttonClickHandler.args[0], [ ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ], 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_rename_element_handler should return false' );
    });

    QUnit.test( 'button_delete_element_handler folder', function ( assert ) {
        expect( 5 );
        selElement.model = "folder";
        selElement.name = "NAME";

        var ajax_Function   = ajax_folderDelete;
        var dialogTitle     = "Видалення теки";
        var inputLabel      = "Видалити";
        var disabledInput   = true;
        var inputVal        = "NAME";
        var condLabel       = "";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_delete_element_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_delete_element_handler should return false' );
    });
    QUnit.test( 'button_delete_element_handler report', function ( assert ) {
        expect( 5 );
        selElement.model = "report";
        selElement.name = "NAME";

        var ajax_Function   = ajax_reportDelete;
        var dialogTitle     = "Видалення файла";
        var inputLabel      = "Видалити";
        var disabledInput   = true;
        var inputVal        = "NAME";
        var condLabel       = "";
        var condVal         = false;
        var confirmTitle    = "";
        var confirmMsg      = "";
        var selectionCheck  = "selectionCheck";
        
        stub.check_selRowIndex_range = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.buttonClickHandler = sinon.stub( window, "buttonClickHandler" );
   
        var res = button_delete_element_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.buttonClickHandler.calledOnce, 'buttonClickHandler should be called once' );
        assert.ok( stub.buttonClickHandler.calledWithExactly( ajax_Function, dialogTitle, inputLabel, 
                            disabledInput, inputVal, condLabel, condVal, confirmTitle, confirmMsg, selectionCheck ), 
                            'buttonClickHandler should be called with arg' );

        assert.equal( res, false, 'button_delete_element_handler should return false' );
    });
    QUnit.test( 'button_move_element_handler', function ( assert ) {
        expect( 7 );

        var selectionCheck  = true;
        var f_name          = "f_name";
        
        stub.check_selRowIndex_range    = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.ajax_FoldersTreeFromBase   = sinon.stub( window, "ajax_FoldersTreeFromBase" );
        stub.get_thisfolder_name        = sinon.stub( window, "get_thisfolder_name" ).returns( f_name );
        stub.noSelectionMessage         = sinon.stub( window, "noSelectionMessage" );
   
        var res = button_move_element_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.ok( stub.ajax_FoldersTreeFromBase.calledOnce, 'ajax_FoldersTreeFromBase should be called once' );
        assert.ok( stub.ajax_FoldersTreeFromBase.calledWithExactly( ), 'ajax_FoldersTreeFromBase should be called with arg' );

        assert.notOk( stub.get_thisfolder_name.called, 'get_thisfolder_name should not be called' );
        assert.notOk( stub.noSelectionMessage.called, 'noSelectionMessage should not be called' );

        assert.equal( res, false, 'button_move_element_handler should return false' );
    });
    QUnit.test( 'button_move_element_handler no selection', function ( assert ) {
        expect( 8 );

        var selectionCheck  = false;
        var f_name          = "f_name";
        
        stub.check_selRowIndex_range    = sinon.stub( window, "check_selRowIndex_range" ).returns( selectionCheck );
        stub.ajax_FoldersTreeFromBase   = sinon.stub( window, "ajax_FoldersTreeFromBase" );
        stub.get_thisfolder_name        = sinon.stub( window, "get_thisfolder_name" ).returns( f_name );
        stub.noSelectionMessage         = sinon.stub( window, "noSelectionMessage" );
   
        var res = button_move_element_handler( );
        
        assert.ok( stub.check_selRowIndex_range.calledOnce, 'check_selRowIndex_range should be called once' );
        assert.ok( stub.check_selRowIndex_range.calledWithExactly( ), 'check_selRowIndex_range should be called with arg' );
        assert.notOk( stub.ajax_FoldersTreeFromBase.called, 'ajax_FoldersTreeFromBase should not be called' );

        assert.ok( stub.get_thisfolder_name.calledOnce, 'get_thisfolder_name should be called once' );
        assert.ok( stub.get_thisfolder_name.calledWithExactly( ), 'get_thisfolder_name should be called with arg' );
        assert.ok( stub.noSelectionMessage.calledOnce, 'noSelectionMessage should be called once' );
        assert.ok( stub.noSelectionMessage.calledWithExactly( f_name ), 'noSelectionMessage should be called with arg' );

        assert.equal( res, false, 'button_move_element_handler should return false' );
    });
} );
//=============================================================================
QUnit.module( "folder_browtab_ui tree", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'add_tree_dialog', function ( assert ) {
        expect( 7 );

        stub.dialog                     = sinon.stub( jQuery.prototype, "dialog" );
        stub.dialog_width               = sinon.stub( window, "dialog_width" ).returns( 400 );
        stub.get_dialog_default_buttons = sinon.stub( window, "get_dialog_default_buttons" ).returns( 'buttons' );

        var arr1 = {    // tree dialog
            dialogClass:    "no-close",
            autoOpen:       false,
            modal:          true,
            closeOnEscape:  true,
            height:         480,
            width:          600,
            close:          tree_onClose_handler,
            buttons:        "buttons"   // no comma - last item in array
        };

        var res = add_tree_dialog( );

        assert.ok( stub.dialog.calledOnce, 'dialog should be called once' );
        assert.deepEqual( stub.dialog.args[0][0], arr1, 'dialog should be called with arg' );

        assert.ok( stub.dialog_width.calledTwice, 'dialog_width should be called twice' );
        assert.ok( stub.dialog_width.alwaysCalledWithExactly( ), 'dialog_width should be called with arg' );
        assert.ok( stub.get_dialog_default_buttons.calledOnce, 'get_dialog_default_buttons should be called once' );
        assert.ok( stub.get_dialog_default_buttons.calledWithExactly( ), 
                                                                'get_dialog_default_buttons should be called with arg' );

        assert.equal( res, undefined, 'add_tree_dialog should return undefined' );
    });
    QUnit.test( 'tree_onClose_handler', function ( assert ) {
        expect( 5 );

        stub.selRowFocus    = sinon.stub( window, "selRowFocus" );
        stub.destroy        = sinon.stub( $.jstree, "destroy" );
   
        var res = tree_onClose_handler( );
        
        assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
        assert.ok( stub.selRowFocus.calledWithExactly( ), 'selRowFocus should be called with arg' );
        assert.ok( stub.destroy.calledOnce, 'destroy should be called once' );
        assert.ok( stub.destroy.calledWithExactly( ), 'destroy should be called with arg' );

        assert.equal( res, false, 'tree_onClose_handler should return false' );
    });
} );
//=============================================================================
QUnit.module( "folder_browtab_ui dialogFoldersTreeHTML", function( hooks ) { 
    var sr;
    var parent_id;
    var on_func;
    var buttons;
    var dialogTitle;
    hooks.beforeEach( function( assert ) {
        stub = {};
        selElement = {};
        sr = { 'sr': 'sr' };
        parent_id = '77';

        // expected values:
        on_func = function( e, data ) {
                            target_id = data.selected[0];  // selected taget is the first element of data.selected 1D array
                            console.log("jsTree: data.selected=", data.selected);
        };
        buttons = [
            {
                text: "Ok",
                click: function( e ) {
                            ajax_elementMove( target_id );
                            return false;
                }
            },
            {
                text: "Cancel",
                click: function( e ) {
                            $( this ).dialog( "close" );
                            return false;
                }
            }
        ];
        stub.dialog                     = sinon.stub( jQuery.prototype, "dialog" );
        stub.jstree                     = sinon.stub( jQuery.prototype, "jstree" );
        stub.val                        = sinon.stub( jQuery.prototype, "val" ).returns( parent_id );
        stub.html                       = sinon.stub( jQuery.prototype, "html" );
        stub.on                         = sinon.spy( jQuery.prototype, "on" );
        stub.get_dialog_default_buttons = sinon.spy( window, "get_dialog_default_buttons" );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'folder', function ( assert ) {
        expect( 29 );

        selElement.model = "folder";
        dialogTitle  = "Перемістити виділену теку до теки...";

        var res = dialogFoldersTreeHTML( sr );

        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 3 times' );
        assert.equal( stub.jstree.callCount, 4, 'jstree should be called 4 times' );
        assert.equal( stub.val.callCount, 1, 'val should be called 1 times' );
        assert.equal( stub.html.callCount, 1, 'html should be called 1 times' );
        assert.equal( stub.on.callCount, 1, 'on should be called 1 times' );
        assert.equal( stub.get_dialog_default_buttons.callCount, 1, 'get_dialog_default_buttons should be called once' );

        assert.deepEqual( stub.val.thisValues[0], $( "#parent_id" ), 'val called as method of proper this' );
        assert.deepEqual( stub.val.args[0], [ ], 'val should be called with args' );

        assert.deepEqual( stub.html.thisValues[0], $( '#folders-tree-container' ), 'html called as method of proper this' );
        assert.deepEqual( stub.html.args[0], [ sr ], 'html should be called with args' );

        assert.deepEqual( stub.jstree.thisValues[0], $( '#folders-tree-container' ), 'jstree called as method of proper this' );
        assert.deepEqual( stub.jstree.args[0], [ ], 'jstree should be called with args' );

        assert.deepEqual( stub.jstree.thisValues[1], $( '#folders-tree-container' ), 'jstree called as method of proper this' );
        assert.deepEqual( stub.jstree.args[1], [ "set_theme", "koopstyle" ], 'jstree should be called with args' );

        assert.deepEqual( stub.jstree.thisValues[2], $( '#folders-tree-container' ), 'jstree called as method of proper this' );
        assert.deepEqual( stub.jstree.args[2], [ 'show_node', parent_id ], 'jstree should be called with args' );

        assert.deepEqual( stub.jstree.thisValues[3], $( '#folders-tree-container' ), 'jstree called as method of proper this' );
        assert.deepEqual( stub.jstree.args[3], [ 'select_node', parent_id ], 'jstree should be called with args' );

        assert.deepEqual( stub.on.thisValues[0], $( '#folders-tree-container' ), 'on called as method of proper this' );
        assert.deepEqual( stub.on.args[0][0], 'changed.jstree', 'on should be called with args' );
        // TODO-Qunit test for .on() failed but result value did not show, only expected: 
        // assert.deepEqual( stub.on.args[0], [ "changed.jstree",  on_func ], 'on should be called with args' );
        // assert.deepEqual( stub.on.calledWithExactly, ( "changed.jstree",  on_func ), 'on should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[0], $( "#dialog-box-tree" ), 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[0], [ "open" ], 'dialog should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[1], $( "#dialog-box-tree" ), 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[1], [ "option", "title", dialogTitle ], 'dialog should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[2], $( "#dialog-box-tree" ), 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[2][0], "option", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][1], "buttons", 'dialog should be called with args' );
        // TODO-Qunit test for .dialog() failed but result value did not show, only expected: 
        // assert.deepEqual( stub.dialog.args[2][2], buttons, 'dialog should be called with args' );

        assert.deepEqual( stub.get_dialog_default_buttons.args[0], [ ], 
                                                                'get_dialog_default_buttons should be called with args' );

        assert.equal( res, undefined, 'dialogFoldersTreeHTML should return undefined' );
    });
    QUnit.test( 'report', function ( assert ) {
        expect( 29 );

        selElement.model = "report";
        dialogTitle  = "Перемістити файл до теки...";

        var res = dialogFoldersTreeHTML( sr );

        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 3 times' );
        assert.equal( stub.jstree.callCount, 4, 'jstree should be called 4 times' );
        assert.equal( stub.val.callCount, 1, 'val should be called 1 times' );
        assert.equal( stub.html.callCount, 1, 'html should be called 1 times' );
        assert.equal( stub.on.callCount, 1, 'on should be called 1 times' );
        assert.equal( stub.get_dialog_default_buttons.callCount, 1, 'get_dialog_default_buttons should be called once' );

        assert.deepEqual( stub.val.thisValues[0], $( "#parent_id" ), 'val called as method of proper this' );
        assert.deepEqual( stub.val.args[0], [ ], 'val should be called with args' );

        assert.deepEqual( stub.html.thisValues[0], $( '#folders-tree-container' ), 'html called as method of proper this' );
        assert.deepEqual( stub.html.args[0], [ sr ], 'html should be called with args' );

        assert.deepEqual( stub.jstree.thisValues[0], $( '#folders-tree-container' ), 'jstree called as method of proper this' );
        assert.deepEqual( stub.jstree.args[0], [ ], 'jstree should be called with args' );

        assert.deepEqual( stub.jstree.thisValues[1], $( '#folders-tree-container' ), 'jstree called as method of proper this' );
        assert.deepEqual( stub.jstree.args[1], [ "set_theme", "koopstyle" ], 'jstree should be called with args' );

        assert.deepEqual( stub.jstree.thisValues[2], $( '#folders-tree-container' ), 'jstree called as method of proper this' );
        assert.deepEqual( stub.jstree.args[2], [ 'show_node', parent_id ], 'jstree should be called with args' );

        assert.deepEqual( stub.jstree.thisValues[3], $( '#folders-tree-container' ), 'jstree called as method of proper this' );
        assert.deepEqual( stub.jstree.args[3], [ 'select_node', parent_id ], 'jstree should be called with args' );

        assert.deepEqual( stub.on.thisValues[0], $( '#folders-tree-container' ), 'on called as method of proper this' );
        assert.deepEqual( stub.on.args[0][0], 'changed.jstree', 'on should be called with args' );
        // TODO-Qunit test for .on() failed but result value did not show, only expected: 
        // assert.deepEqual( stub.on.args[0], [ "changed.jstree",  on_func ], 'on should be called with args' );
        // assert.deepEqual( stub.on.calledWithExactly, ( "changed.jstree",  on_func ), 'on should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[0], $( "#dialog-box-tree" ), 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[0], [ "open" ], 'dialog should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[1], $( "#dialog-box-tree" ), 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[1], [ "option", "title", dialogTitle ], 'dialog should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[2], $( "#dialog-box-tree" ), 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[2][0], "option", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][1], "buttons", 'dialog should be called with args' );
        // TODO-Qunit test for .dialog() failed but result value did not show, only expected: 
        // assert.deepEqual( stub.dialog.args[2][2], buttons, 'dialog should be called with args' );

        assert.deepEqual( stub.get_dialog_default_buttons.args[0], [ ], 
                                                                'get_dialog_default_buttons should be called with args' );

        assert.equal( res, undefined, 'dialogFoldersTreeHTML should return undefined' );
    });
} );
//=============================================================================
QUnit.module( "folder_browtab_ui dialogFoldersTreeHTML anonimous functions", function( hooks ) { 
    // testing anonymous functions
    var sr;
    var parent_id;
    hooks.beforeEach( function( assert ) {
        stub = {};
        selElement = {};
        selElement.model = "folder";
        parent_id = '77';
        $( "#parent_id" ).val( parent_id );
        sr = { 'sr': 'sr' };

        // stubbing common function before handlers:
        stub.dialog_width       = sinon.stub( window, "dialog_width" ).returns( 400 );

        // dialogs creation
        browtab_ui_document_ready_handler();
        folder_browtab_ui_document_ready_handler();

        // stubbing interesting functions:
        stub.dialog             = sinon.spy( jQuery.prototype, "dialog" );
        stub.ajax_elementMove   = sinon.stub( window, "ajax_elementMove" );

    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
        $( "#dialog-box-tree" ).dialog( "destroy" );
    } );
    QUnit.test( 'click Ok', function ( assert ) {
        expect( 5 );

        dialogFoldersTreeHTML( sr );

        var buttons = $( "#dialog-box-tree" ).dialog( "option", "buttons" );    // Get the buttons
        buttons[0].click();                                                     // Calls the event

        assert.equal( stub.ajax_elementMove.callCount, 1, 'ajax_elementMove should be called once' );
        assert.deepEqual( stub.ajax_elementMove.args[0], [ '77' ], 'ajax_elementMove should be called with args' );

        assert.equal( stub.dialog.callCount, 4+1, 'dialog should be called 4+1 times' );
        assert.deepEqual( stub.dialog.thisValues[4], $( "#dialog-box-tree" ), '4+1 dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[4], [ "close" ], '4+1 dialog should be called with args' );
    });
    QUnit.test( 'click Cancel', function ( assert ) {
        expect( 4 );

        dialogFoldersTreeHTML( sr );

        var buttons = $( "#dialog-box-tree" ).dialog( "option", "buttons" );    // Get the buttons
        buttons[1].click.apply( $( "#dialog-box-tree" ) );                    // Calls the event

        assert.equal( stub.ajax_elementMove.callCount, 0, 'ajax_elementMove should not be called' );

        assert.equal( stub.dialog.callCount, 4+1, 'dialog should be called 4+1 times' );
        assert.deepEqual( stub.dialog.thisValues[4], $( "#dialog-box-tree" ), '4+1 dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[4], [ "close" ], '4+1 dialog should be called with args' );
    });
} );
