/*
 $ (?), $dialog_box_form (?), $dialog_confirm (?), $dialog_message (?), $tbody (?), QUnit (?), XMLHttpRequest (?), add_browtab_ui_dialogs (?), browtab_document_ready_handler (?), browtab_ui_document_ready_handler (?), buttonClickHandler (?), click_Ok_button_on_Enter (?), condFormInput (?), condFormLabel (?), condFormTR (?), confirm_dialog (?), defineAbortButton (?), defineConfirmButtons (?), dialogMessage (?), dialog_box_form_close (?), dialog_close (?), dialog_width (?), emptyFormTR (?), expect (?), fileFormInput (?), fileFormLabel (?), fileFormTR (?), folderEmptyMessage (?), functionOnDevelopeMessage (?), get_confirm_dialog_default_buttons (?), get_dialog_default_buttons (?), get_dlgClass (?), jQuery (?), loadEndHandler (?), nameFormInput (?), nameFormLabel (?), nameFormTR (?), noSelectionMessage (?), progressHandler (?), progressTR (?), progressbarShow (?), selRowFocus (?), setProgress (?), set_Ok_button_on_Enter (?), sinon (?), stub, trim_all_spaces, window (?) 
*/

//QUnit.config.reorder = false;

var stub;   // common for all tests, is set to {} before and restored after each test

//=============================================================================
QUnit.module( "browtab_ui document ready", function( hooks ) { 
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
    QUnit.test( 'browtab_ui_document_ready_handler', function ( assert ) {
        expect( 6 );
        stub.add_browtab_ui_dialogs = sinon.stub( window, "add_browtab_ui_dialogs" );
        var res = browtab_ui_document_ready_handler( );
        assert.deepEqual( $dialog_box_form , $( "#dialog-box-form" ), "js file set proper value to $dialog_box_form" );
        assert.deepEqual( $dialog_confirm  , $( "#dialog-confirm" ), "js file set proper value to $dialog_confirm" );
        assert.deepEqual( $dialog_message  , $( "#dialog-message" ), "js file set proper value to $dialog_message" );
        assert.ok( stub.add_browtab_ui_dialogs.calledOnce, 'add_browtab_ui_dialogs should be called once' );
        assert.ok( stub.add_browtab_ui_dialogs.calledWithExactly( ), 'add_browtab_ui_dialogs should be called with arg' );
        assert.equal( res, undefined, 'browtab_ui_document_ready_handler should return false' );
    });
    QUnit.test( 'add_browtab_ui_dialogs', function ( assert ) {
        expect( 11 );
        browtab_ui_document_ready_handler( );

        stub.dialog_box_form = sinon.stub( $dialog_box_form, "dialog" );
        stub.dialog_confirm  = sinon.stub( $dialog_confirm, "dialog" );
        stub.dialog_message  = sinon.stub( $dialog_message, "dialog" );

        stub.dialog_width                       = sinon.stub( window, "dialog_width" ).returns( 400 );
        stub.get_dialog_default_buttons         = sinon.stub( window, "get_dialog_default_buttons" ).returns( 'buttons' );
        stub.get_confirm_dialog_default_buttons = 
                                    sinon.stub( window, "get_confirm_dialog_default_buttons" ).returns('confirm_buttons');   

        var arr1 = {    // main dialog
            dialogClass:    "no-close",
            autoOpen:       false,
            modal:          true,
            closeOnEscape:  true,
            width:          400,
            open:           set_Ok_button_on_Enter,
            close:          selRowFocus,
            buttons:        "buttons"   // no comma - last item in array
        };
        var arr2 = {     // confirm dialog
            dialogClass:    "no-close",
            autoOpen:       false,
            modal:          true,
            closeOnEscape:  true,
            width:          320
            // buttons:        "confirm_buttons"   // no comma - last item in array
        };
        var arr3 = {     // message dialog
            dialogClass:    "no-close",
            autoOpen:       false,
            modal:          true,
            closeOnEscape:  true,
            close:          selRowFocus,
            buttons:        { Ok: dialog_close }   // no comma - last item in array
        };

        var res = add_browtab_ui_dialogs( );

        assert.ok( stub.dialog_box_form.calledOnce, 'dialog_box_form should be called once' );
        assert.ok( stub.dialog_confirm.calledOnce, 'dialog_confirm should be called once' );
        assert.ok( stub.dialog_message.calledOnce, 'dialog_message should be called once' );

        assert.ok( stub.dialog_box_form.calledWithExactly( arr1 ), 'dialog_box_form should be called with arg' );
        assert.ok( stub.dialog_confirm.calledWithExactly( arr2 ), 'dialog_confirm should be called with arg' );
        assert.ok( stub.dialog_message.calledWithExactly( arr3 ), 'dialog_message should be called with arg' );

        assert.ok( stub.dialog_width.calledTwice, 'dialog_width should be called twice' );
        assert.ok( stub.dialog_width.alwaysCalledWithExactly( ), 'dialog_width should be called with arg' );
        assert.ok( stub.get_dialog_default_buttons.calledOnce, 'get_dialog_default_buttons should be called once' );
        assert.ok( stub.get_dialog_default_buttons.calledWithExactly( ), 
                                                                'get_dialog_default_buttons should be called with arg' );

        assert.equal( res, undefined, 'add_browtab_ui_dialogs should return false' );
    });
} );
//=============================================================================
QUnit.module( "browtab_ui functions", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        // stubbing callback functions before they will be setted as parameters in dialogs:
        stub.set_Ok_button_on_Enter = sinon.stub( window, "set_Ok_button_on_Enter" );
        stub.selRowFocus            = sinon.stub( window, "selRowFocus" );
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'dialog_width 400px', function ( assert ) {
        expect( 3 );
        stub.width = sinon.stub( $tbody, "width" ).returns( 400 );
        var res = dialog_width();
        assert.ok( stub.width.calledOnce, 'width should be called once' );
        assert.ok( stub.width.calledWithExactly( ), 'width should be called with arg' );
        assert.equal( res, 400 * 0.75, 'width should return proper value' );
    });
    QUnit.test( 'dialog_width 399px', function ( assert ) {
        expect( 3 );
        stub.width = sinon.stub( $tbody, "width" ).returns( 400.5 );
        var res = dialog_width();
        assert.ok( stub.width.calledOnce, 'width should be called once' );
        assert.ok( stub.width.calledWithExactly( ), 'width should be called with arg' );
        assert.equal( res, 400 * 0.75, 'width should return proper value' );
    });
    QUnit.test( 'dialog_width 600px', function ( assert ) {
        expect( 3 );
        stub.width = sinon.stub( $tbody, "width" ).returns( 600 );
        var res = dialog_width();
        assert.ok( stub.width.calledOnce, 'width should be called once' );
        assert.ok( stub.width.calledWithExactly( ), 'width should be called with arg' );
        assert.equal( res, 450, 'width should return proper value' );
    });
    QUnit.test( 'dialog_close', function ( assert ) {
        expect( 4 );

        stub.dialog = sinon.spy( jQuery.prototype, "dialog" );

        var res = dialog_close.call( $dialog_box_form );

        assert.deepEqual( stub.dialog.thisValues[0], $dialog_box_form, 'dialog called as method of proper this' );
        assert.equal( stub.dialog.callCount, 1, 'dialog should be called once' );
        assert.ok( stub.dialog.calledWithExactly( 'close' ), 'dialog should be called with args' );

        assert.equal( res, undefined, 'dialog_close should return undefined' );
    });
    QUnit.test( 'dialog_close functional test', function ( assert ) {
        // Check if onClose callback function, i.e. selRowFocus() is called and dialog is really closed.
        expect( 5 );
	    $dialog_box_form.dialog( "open" );
	    var isOpen  = $dialog_box_form.dialog( "isOpen" );
        assert.ok( isOpen, 'dialog should be open before test' );
        assert.ok( stub.set_Ok_button_on_Enter.calledOnce, 'set_Ok_button_on_Enter should be called once' );
        
        var res = dialog_close.call( $dialog_box_form );

        isOpen  = $dialog_box_form.dialog( "isOpen" );
        assert.notOk( isOpen, 'dialog should be closed after dialog_close.call' );
        assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
        assert.equal( res, undefined, 'dialog_close should return undefined' );
    });
    QUnit.test( 'dialog_box_form_close', function ( assert ) {
        expect( 2 );
        
        stub.dialog = sinon.spy( $dialog_box_form, "dialog" );

        var res = dialog_box_form_close( );

        assert.equal( stub.dialog.callCount, 1, 'dialog should be called once' );
        assert.ok( stub.dialog.calledWithExactly( 'close' ), 'dialog should be called with args' );

    });
    QUnit.test( 'defineAbortButton', function ( assert ) {
        expect( 13 );
        var buttons = [
            {
                text  : "Abort loading",
                click : function( e ) {
                            dialog_box_form_close();
                            xhr.abort();
                            return false;
                }
            }
        ];

        var xhr = new XMLHttpRequest();
	    $dialog_box_form.dialog( "open" );
	    var isOpen  = $dialog_box_form.dialog( "isOpen" );
        assert.ok( isOpen, 'dialog should be open before test' );
        assert.ok( stub.set_Ok_button_on_Enter.calledOnce, 'set_Ok_button_on_Enter should be called once' );

        stub.dialog                 = sinon.spy( $dialog_box_form, "dialog" );
        stub.dialog_box_form_close  = sinon.spy( window, "dialog_box_form_close" );
        stub.abort                  = sinon.stub( xhr, "abort" );

        var res = defineAbortButton( xhr );

        assert.equal( stub.dialog.callCount, 1, 'dialog should be called once' );
        assert.ok( stub.dialog.calledWith( "option", "buttons" ), 'dialog should be called with arg' );
        assert.deepEqual( stub.dialog.args[0][2][0].text, buttons[0].text, 'dialog should be called with text arg' );
        assert.equal( trim_all_spaces( stub.dialog.args[0][2][0].click ), 
                      trim_all_spaces( buttons[0].click ), 'dialog should be called with click arg' );

        assert.equal( res, undefined, 'defineAbortButton should return proper value' );

        // Simulation of button click:
        $dialog_box_form.parent().find( "button:contains('Abort loading')" ).trigger( "click" );
        assert.ok( stub.dialog_box_form_close.calledOnce, 'dialog_box_form_close should be called once' );
        assert.ok( stub.dialog_box_form_close.calledWithExactly( ), 
                                                                'dialog_box_form_close should be called with arg' );
        assert.ok( stub.abort.calledOnce, 'abort should be called once' );
        assert.ok( stub.abort.calledWithExactly( ), 'abort should be called with arg' );

        isOpen  = $dialog_box_form.dialog( "isOpen" );
        assert.notOk( isOpen, 'dialog should be closed after dialog_box_form_close() call' );
        assert.ok( stub.selRowFocus.calledOnce, 'selRowFocus should be called once' );
    });
    QUnit.test( 'defineConfirmButtons click Ok', function ( assert ) {
        expect( 14 );

	    $dialog_confirm.dialog( "open" );
	    var isOpen  = $dialog_confirm.dialog( "isOpen" );
        assert.ok( isOpen, 'dialog should be open before test' );

        var ajax_Function   = sinon.stub( );
        stub.dialog         = sinon.spy( $dialog_confirm, "dialog" );
        stub.dialog_close   = sinon.spy( window, "dialog_close" );

        var buttons = [
            {
                text: "Ok",
                click: function( e ) {
                        $dialog_confirm.dialog( "close" );
                        ajax_Function();
                        return false;
                }
            },
            {
                text: "Cancel",
                click: dialog_close
            }
        ];

        var res = defineConfirmButtons( ajax_Function );

        assert.equal( stub.dialog.callCount, 1, 'dialog should be called once' );
        assert.ok( stub.dialog.calledWith( "option", "buttons" ), 'dialog should be called with arg' );
        assert.deepEqual( stub.dialog.args[0][2][0].text, buttons[0].text, 'dialog should be called with text arg' );
        assert.deepEqual( stub.dialog.args[0][2][1].text, buttons[1].text, 'dialog should be called with text arg' );
        assert.deepEqual( stub.dialog.args[0][2][1].click, buttons[1].click, 'dialog should be called with click arg' );
        assert.equal( trim_all_spaces( stub.dialog.args[0][2][0].click ), 
                      trim_all_spaces( buttons[0].click ), 'dialog should be called with click arg' );

        assert.equal( res, undefined, 'defineConfirmButtons should return proper value' );

        // Simulation of button click:
        $dialog_confirm.parent().find( "button:contains('Ok')" ).trigger( "click" );
        assert.ok( stub.dialog.calledTwice, 'dialog should be called once' );
        assert.ok( stub.dialog.args[1], [ "close" ], 'dialog should be called with arg' );
        assert.ok( ajax_Function.calledOnce, 'ajax_Function should be called once' );
        assert.ok( ajax_Function.calledWithExactly( ), 'ajax_Function should be called with arg' );
        assert.notOk( dialog_close.called, 'dialog_close should not be called' );

        isOpen  = $dialog_confirm.dialog( "isOpen" );
        assert.notOk( isOpen, 'dialog should be closed after dialog("close") call' );
    });
    QUnit.test( 'defineConfirmButtons click Cancel', function ( assert ) {
        expect( 11 );

	    $dialog_confirm.dialog( "open" );
	    var isOpen  = $dialog_confirm.dialog( "isOpen" );
        assert.ok( isOpen, 'dialog should be open before test' );

        var ajax_Function   = sinon.stub( );
        stub.dialog         = sinon.spy( $dialog_confirm, "dialog" );
        stub.dialog_close   = sinon.spy( window, "dialog_close" );

        var buttons = [
            {
                text: "Ok",
                click: function( e ) {
                        $dialog_confirm.dialog( "close" );
                        ajax_Function();
                        return false;
                }
            },
            {
                text: "Cancel",
                click: dialog_close
            }
        ];

        var res = defineConfirmButtons( ajax_Function );

        assert.equal( stub.dialog.callCount, 1, 'dialog should be called once' );
        assert.ok( stub.dialog.calledWith( "option", "buttons" ), 'dialog should be called with arg' );
        assert.deepEqual( stub.dialog.args[0][2][0].text, buttons[0].text, 'dialog should be called with text arg' );
        assert.deepEqual( stub.dialog.args[0][2][1].text, buttons[1].text, 'dialog should be called with text arg' );
        assert.deepEqual( stub.dialog.args[0][2][1].click, buttons[1].click, 'dialog should be called with click arg' );
        assert.equal( trim_all_spaces( stub.dialog.args[0][2][0].click ), 
                      trim_all_spaces( buttons[0].click ), 'dialog should be called with click arg' );

        assert.equal( res, undefined, 'defineConfirmButtons should return proper value' );

        // Simulation of button click:
        $dialog_confirm.parent().find( "button:contains('Cancel')" ).trigger( "click" );
        assert.ok( stub.dialog_close.calledOnce, 'dialog_close should be called once' );
        assert.notOk( ajax_Function.called, 'ajax_Function should not be called' );

        isOpen  = $dialog_confirm.dialog( "isOpen" );
        assert.notOk( isOpen, 'dialog should be closed after dialog_close() call' );
    });
    QUnit.test( 'confirm_dialog', function ( assert ) {
        expect( 18 );

        stub.dialog                 = sinon.stub( jQuery.prototype, "dialog" );
        stub.find                   = sinon.spy( jQuery.prototype, "find" );
        stub.focus                  = sinon.spy( jQuery.prototype, "focus" );
        stub.html                   = sinon.spy( jQuery.prototype, "html" );
        stub.siblings               = sinon.spy( jQuery.prototype, "siblings" );
        stub.defineConfirmButtons   = sinon.stub( window, "defineConfirmButtons" );

        var ajax_Function   = sinon.stub( );
        var confirmTitle    = "confirmTitle";
        var confirmMsg      = "confirmMsg";

        var res = confirm_dialog( ajax_Function, confirmTitle, confirmMsg );

        assert.equal( stub.dialog.callCount, 2, 'dialog should be called 2 times' );
        assert.deepEqual( stub.dialog.thisValues[0], $dialog_confirm, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.thisValues[1], $dialog_confirm, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[0], [ "open" ], 'dialog should be called with text arg' );
        assert.deepEqual( stub.dialog.args[1], [ "option", "title", confirmTitle ], 'dialog should be called with text arg' );

        assert.equal( stub.html.callCount, 1, 'html should be called 1 times' );
        assert.deepEqual( stub.html.thisValues[0], $dialog_confirm, 'find called as method of proper this' );
        assert.deepEqual( stub.html.args[0], [ confirmMsg ], 'html should be called with args' );

        assert.equal( stub.defineConfirmButtons.callCount, 1, 'defineConfirmButtons should be called 1 times' );
        assert.deepEqual( stub.defineConfirmButtons.args[0], [ ajax_Function ], 
                                                                'defineConfirmButtons should be called with args' );

        assert.equal( stub.siblings.callCount, 1, 'siblings should be called 1 times' );
        assert.equal( stub.find.callCount, 1, 'find should be called 1 times' );
        assert.equal( stub.focus.callCount, 1, 'focus should be called 1 times' );
        assert.deepEqual( stub.siblings.thisValues[0], $dialog_confirm, 'siblings called as method of proper this' );
        assert.deepEqual( stub.siblings.args[0], [ ], 'siblings should be called with args' );
        assert.deepEqual( stub.find.args[0], [ "button:eq(0)" ], 'find should be called with args' );
        assert.deepEqual( stub.focus.args[0], [ ], 'focus should be called with args' );

        assert.equal( res, undefined, 'confirm_dialog should return proper value' );

    });
} );
function trim_all_spaces( f ){
    var s = String( f ).replace( / /g, '' );
    return s;
}
//=============================================================================
QUnit.module( "browtab_ui functions 2", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'get_dialog_default_buttons', function ( assert ) {
        expect( 1 );
        var expected = [
            { text: "Ok",       click: undefined },
            { text: "Cancel",   click: dialog_close }
        ];
        var res = get_dialog_default_buttons();
        assert.deepEqual( res, expected, 'get_dialog_default_buttons should return proper value' );
    });
    QUnit.test( 'get_confirm_dialog_default_buttons', function ( assert ) {
        expect( 1 );
        var expected = [
            { text: "Ok",       click: undefined },
            { text: "Cancel",   click: dialog_close }
        ];
        var res = get_confirm_dialog_default_buttons();
        assert.deepEqual( res, expected, 'get_confirm_dialog_default_buttons should return proper value' );
    });
} );
//=============================================================================
QUnit.module( "browtab_ui click_Ok_button_on_Enter", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );
        $dialog_box_form.dialog( "open" );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
        $dialog_box_form.dialog( "close" );
    } );
    QUnit.test( 'Enter key', function ( assert ) {
        expect( 8 );
        var e = {};
        e.keyCode = $.ui.keyCode.ENTER;

        var buttons = { Ok: undefined };
        $dialog_box_form.dialog( "option", "buttons", buttons );

        stub.parent = sinon.spy( jQuery.prototype, "parent" );
        stub.find   = sinon.spy( jQuery.prototype, "find" );
        stub.trigger = sinon.stub( jQuery.prototype, "trigger" );

        var res = click_Ok_button_on_Enter.call( $dialog_box_form, e );

        assert.deepEqual( stub.parent.thisValues[0], $dialog_box_form, 'parent called as method of proper this' );
        assert.equal( stub.parent.callCount, 1, 'parent should be called once' );
        assert.ok( stub.parent.calledWithExactly( ), 'parent should be called with arg' );
        assert.equal( stub.find.callCount, 1, 'find should be called once' );
        assert.ok( stub.find.calledWithExactly( "button:contains('Ok')" ), 'find should be called with arg' );
        assert.equal( stub.trigger.callCount, 1, 'trigger should be called once' );
        assert.ok( stub.trigger.calledWithExactly( "click" ), 'trigger should be called with arg' );

        assert.equal( res, false, 'click_Ok_button_on_Enter should return false' );
    });
    QUnit.test( 'Not Enter key', function ( assert ) {
        expect( 4 );
        var e = {};
        e.keyCode = $.ui.keyCode.LEFT;

        var buttons = { Ok: undefined };
        $dialog_box_form.dialog( "option", "buttons", buttons );

        stub.parent = sinon.spy( jQuery.prototype, "parent" );
        stub.find   = sinon.spy( jQuery.prototype, "find" );
        stub.trigger = sinon.stub( jQuery.prototype, "trigger" );

        var res = click_Ok_button_on_Enter.call( $dialog_box_form, e );

        assert.equal( stub.parent.callCount, 0, 'parent should not be called' );
        assert.equal( stub.find.callCount, 0, 'find should not be called' );
        assert.equal( stub.trigger.callCount, 0, 'trigger should not be called' );

        assert.equal( res, undefined, 'click_Ok_button_on_Enter should return undefined' );
    });
    QUnit.test( 'Enter key functional', function ( assert ) {
        expect( 2 );
        var e = {};
        e.keyCode = $.ui.keyCode.ENTER;

        var callback = sinon.spy();

        var buttons = { Ok: callback };
        $dialog_box_form.dialog( "option", "buttons", buttons );

        var res = click_Ok_button_on_Enter.call( $dialog_box_form, e );

        assert.ok( callback.calledOnce, 'callback should be called once' );
        assert.equal( res, false, 'click_Ok_button_on_Enter should return false' );
        $dialog_box_form.dialog( "close" );
    });
    QUnit.test( 'not Enter key functional', function ( assert ) {
        expect( 2 );
        var e = {};
        e.keyCode = $.ui.keyCode.LEFT;

        var callback = sinon.spy();

        var buttons = { Ok: callback };
        $dialog_box_form.dialog( "option", "buttons", buttons );

        var res = click_Ok_button_on_Enter.call( $dialog_box_form, e );

        assert.notOk( callback.called, 'callback should not be called' );
        assert.equal( res, undefined, 'click_Ok_button_on_Enter should return undefined' );
    });
    QUnit.test( 'set_Ok_button_on_Enter', function ( assert ) {
        expect( 3 );

        stub.keypress = sinon.spy( $dialog_box_form, "keypress" );
        stub.click_Ok_button_on_Enter = sinon.stub( window, "click_Ok_button_on_Enter" );

        var res = set_Ok_button_on_Enter.call( $dialog_box_form );
        $dialog_box_form.keypress();

        assert.ok( stub.keypress.calledOnce, 'keypress should be called once' );
        assert.ok( stub.click_Ok_button_on_Enter.calledOnce, 'click_Ok_button_on_Enter should be called once' );
        assert.equal( res, undefined, 'set_Ok_button_on_Enter should return undefined' );
    });
} );
//=============================================================================
QUnit.test( 'js file start assignments', function ( assert ) {
    assert.equal( nameFormLabel , '<label for="id_name">Тека:</label>');
    assert.equal( nameFormInput , '<input id="id_name" maxlength="256" name="name" type="text" autofocus/>');
    assert.equal( nameFormTR    , '<td>' + nameFormLabel + '</td>' +
                                  '<td>' + nameFormInput + '</td>');
    assert.equal( fileFormLabel , '<label for="id_file">Файл:</label>');
    assert.equal( fileFormInput , '<input id="id_file" maxlength="256" name="file" type="file" autofocus/>');
    assert.equal( fileFormTR    , '<td>' + fileFormLabel + '</td>' +
                                  '<td>' + fileFormInput + '</td>');
    assert.equal( condFormLabel , '<label for="id_cond">Повідомити ч/з email</label>');
    assert.equal( condFormInput , '<input id="id_cond" name="cond" type="checkbox"/>');
    assert.equal( condFormTR    , '<td>' + '</td>' +
                                  '<td>' + condFormLabel + condFormInput + '</td>');
    assert.equal( progressTR    , '<td>Progress:</td><td><div id="progressbar"></div></td>');
    assert.equal( emptyFormTR   , '<td></td><td></td>');
});
//=============================================================================
QUnit.module( "browtab_ui progress", function( hooks ) { 
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'progressbarShow', function ( assert ) {
        expect( 7 );
    
        stub.find        = sinon.spy( jQuery.prototype, "find" );
        stub.html        = sinon.spy( jQuery.prototype, "html" );
        stub.progressbar = sinon.spy( jQuery.prototype, "progressbar" );

        var res = progressbarShow();

        assert.equal( stub.find.callCount, 1, 'find should be called once' );
        assert.ok( stub.find.calledWithExactly( "tr:nth-child(2)" ), 'find should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called once' );
        assert.ok( stub.html.calledWithExactly( progressTR ), 'html should be called with arg' );
        assert.equal( stub.progressbar.callCount, 1, 'progressbar should be called once' );
        assert.ok( stub.progressbar.calledWithExactly( { value: 0 } ), 'html should be called with arg' );
        assert.equal( res, undefined, 'progressbarShow should return undefined' );
    });
    QUnit.test( 'setProgress #1', function ( assert ) {
        expect( 6 );
        var x = 5;
        var max = 200;
        var pmax = 300;
        var arr = { value: 5, max: 200 };

        stub.progressbar = sinon.stub( jQuery.prototype, "progressbar" );
        stub.progressbar.withArgs( "option", "max" ).returns( pmax );

        var res = setProgress( x, max );

        assert.deepEqual( stub.progressbar.thisValues[0], $( "#progressbar" ), 
                                                                            '0 progressbar called as method of proper this' );
        assert.deepEqual( stub.progressbar.thisValues[1], $( "#progressbar" ), 
                                                                            '1 progressbar called as method of proper this' );
        assert.equal( stub.progressbar.callCount, 2, 'progressbar should be called 2 times' );
        assert.ok( stub.progressbar.getCall( 0 ).calledWithExactly( "option", "max" ), 
                                                                            '0 progressbar should be called with arg' );
        assert.ok( stub.progressbar.getCall( 1 ).calledWithExactly( arr ), 
                                                                            '1 progressbar should be called with arg' );
        assert.equal( res, undefined, 'setProgress should return undefined' );
    });
    QUnit.test( 'setProgress #2', function ( assert ) {
        expect( 6 );
        var x = 5;
        var max = 200;
        var pmax = undefined;
        var arr = { value: 5, max: 200 };

        stub.progressbar = sinon.stub( jQuery.prototype, "progressbar" );
        stub.progressbar.withArgs( "option", "max" ).returns( pmax );

        var res = setProgress( x, max );

        assert.deepEqual( stub.progressbar.thisValues[0], $( "#progressbar" ), 
                                                                            '0 progressbar called as method of proper this' );
        assert.deepEqual( stub.progressbar.thisValues[1], $( "#progressbar" ), 
                                                                            '1 progressbar called as method of proper this' );
        assert.equal( stub.progressbar.callCount, 2, 'progressbar should be called 2 times' );
        assert.ok( stub.progressbar.getCall( 0 ).calledWithExactly( "option", "max" ), 
                                                                            '0 progressbar should be called with arg' );
        assert.ok( stub.progressbar.getCall( 1 ).calledWithExactly( arr ), 
                                                                            '1 progressbar should be called with arg' );
        assert.equal( res, undefined, 'setProgress should return undefined' );
    });
    QUnit.test( 'setProgress #3', function ( assert ) {
        expect( 6 );
        var x = 5;
        var max = undefined;
        var pmax = 300;
        var arr = { value: 5, max: 300 };

        stub.progressbar = sinon.stub( jQuery.prototype, "progressbar" );
        stub.progressbar.withArgs( "option", "max" ).returns( pmax );

        var res = setProgress( x, max );

        assert.deepEqual( stub.progressbar.thisValues[0], $( "#progressbar" ), 
                                                                            '0 progressbar called as method of proper this' );
        assert.deepEqual( stub.progressbar.thisValues[1], $( "#progressbar" ), 
                                                                            '1 progressbar called as method of proper this' );
        assert.equal( stub.progressbar.callCount, 2, 'progressbar should be called 2 times' );
        assert.ok( stub.progressbar.getCall( 0 ).calledWithExactly( "option", "max" ), 
                                                                            '0 progressbar should be called with arg' );
        assert.ok( stub.progressbar.getCall( 1 ).calledWithExactly( arr ), 
                                                                            '1 progressbar should be called with arg' );
        assert.equal( res, undefined, 'setProgress should return undefined' );
    });
    QUnit.test( 'setProgress #4', function ( assert ) {
        expect( 6 );
        var x = 5;
        var max = undefined;
        var pmax = undefined;
        var arr = { value: 5, max: 100 };

        stub.progressbar = sinon.stub( jQuery.prototype, "progressbar" );
        stub.progressbar.withArgs( "option", "max" ).returns( pmax );

        var res = setProgress( x, max );

        assert.deepEqual( stub.progressbar.thisValues[0], $( "#progressbar" ),'0 progressbar called as method of proper this' );
        assert.deepEqual( stub.progressbar.thisValues[1], $( "#progressbar" ),'1 progressbar called as method of proper this' );
        assert.equal( stub.progressbar.callCount, 2, 'progressbar should be called 2 times' );
        assert.ok( stub.progressbar.getCall( 0 ).calledWithExactly( "option", "max" ), 
                                                                            '0 progressbar should be called with arg' );
        assert.ok( stub.progressbar.getCall( 1 ).calledWithExactly( arr ), '1 progressbar should be called with arg' );
        assert.equal( res, undefined, 'setProgress should return undefined' );
    });
    QUnit.test( 'progressHandler true', function ( assert ) {
        expect( 3 );
        var pe = {};
        pe.lengthComputable = true;
        pe.loaded = 'load';
        pe.total  = 'total';

        stub.setProgress = sinon.stub( window, "setProgress" );

        var res = progressHandler( pe );

        assert.equal( stub.setProgress.callCount, 1, 'setProgress should be called ones' );
        assert.ok( stub.setProgress.calledWithExactly( pe.loaded, pe.total ), 'setProgress should be called with arg' );
        assert.equal( res, undefined, 'progressHandler should return undefined' );
    });
    QUnit.test( 'progressHandler false', function ( assert ) {
        expect( 3 );
        var pe = {};
        pe.lengthComputable = false;
        pe.loaded = 'load';
        pe.total  = 'total';

        stub.setProgress = sinon.stub( window, "setProgress" );

        var res = progressHandler( pe );

        assert.equal( stub.setProgress.callCount, 1, 'setProgress should be called ones' );
        assert.ok( stub.setProgress.calledWithExactly( false ), 'setProgress should be called with arg' );
        assert.equal( res, undefined, 'progressHandler should return undefined' );
    });
    QUnit.test( 'loadEndHandler', function ( assert ) {
        expect( 3 );
        var pe = {};
        pe.loaded = 'load';

        stub.setProgress = sinon.stub( window, "setProgress" );

        var res = loadEndHandler( pe );

        assert.equal( stub.setProgress.callCount, 1, 'setProgress should be called ones' );
        assert.ok( stub.setProgress.calledWithExactly( pe.loaded ), 'setProgress should be called with arg' );
        assert.equal( res, undefined, 'loadEndHandler should return undefined' );
    });
} );
//=============================================================================
QUnit.module( "browtab_ui dialogMessage", function( hooks ) { 
    var clock;
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( 'get_dlgClass', function ( assert ) {
        expect( 5 );
        assert.equal( get_dlgClass( "IncorrectData") , "no-close ui-state-error" );
        assert.equal( get_dlgClass( "Forbidden"    ) , "no-close ui-state-error" );
        assert.equal( get_dlgClass( "Error"        ) , "no-close ui-state-error" );
        assert.equal( get_dlgClass( "Normal"       ) , "no-close ui-state-highlight" );
        assert.equal( get_dlgClass( ""             ) , "no-close ui-state-highlight" );
    });
    QUnit.test( '#1', function ( assert ) {
        expect( 13 );
        clock = sinon.useFakeTimers();
        var msg = "msg";
        var type = "type";
        var title = "title";
        var time = 100;
        var dlgClass = "dlgClass";
        var timeout_arg = function(){ $dialog_message.dialog( "close" ); };

        stub.setTimeout   = sinon.spy( window, "setTimeout" );
        stub.get_dlgClass = sinon.stub( window, "get_dlgClass" ).returns( dlgClass );
        stub.html         = sinon.spy( $dialog_message, "html" );
        stub.dialog       = sinon.spy( $dialog_message, "dialog" );

        var res = dialogMessage( msg, type, title, time );

        clock.tick( 100 );

        assert.equal( stub.setTimeout.callCount, 2, 'setTimeout should be called 1 + 1 times' ); 
        // zero call of setTimeout is probably associated with spying
        assert.deepEqual( trim_all_spaces( stub.setTimeout.args[1][0] ), 
                          trim_all_spaces( timeout_arg ), 'setTimeout should be called with 0. arg' );
        assert.deepEqual( stub.setTimeout.args[1][1], time, 'setTimeout should be called with 1. arg' );
        assert.equal( stub.get_dlgClass.callCount, 1, 'get_dlgClass should be called ones' );
        assert.ok( stub.get_dlgClass.calledWithExactly( type ), 'get_dlgClass should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called ones' );
        assert.ok( stub.html.calledWithExactly( msg ), 'html should be called with arg' );
        assert.equal( stub.dialog.callCount, 4, 'dialog should be called 4 times' );
        assert.ok( stub.dialog.getCall( 0 ).calledWithExactly( "option", "dialogClass", dlgClass ), '0 dialog arg' );
        assert.ok( stub.dialog.getCall( 1 ).calledWithExactly( "open" ),                            '1 dialog arg' );
        assert.ok( stub.dialog.getCall( 2 ).calledWithExactly( "option", "title", title ),          '2 dialog arg' );
        assert.ok( stub.dialog.getCall( 3 ).calledWithExactly( "close" ),                           '3 dialog arg' );
        assert.equal( res, undefined, 'dialogMessage should return undefined' );
        clock.restore();
    });
    QUnit.test( '#2', function ( assert ) {
        expect( 12 );
        clock = sinon.useFakeTimers();
        var msg = "msg";
        var type = "type";
        var title = undefined;
        var time = 100;
        var dlgClass = "dlgClass";
        var timeout_arg = function(){ $dialog_message.dialog( "close" ); };

        stub.setTimeout   = sinon.spy( window, "setTimeout" );
        stub.get_dlgClass = sinon.stub( window, "get_dlgClass" ).returns( dlgClass );
        stub.html         = sinon.spy( $dialog_message, "html" );
        stub.dialog       = sinon.spy( $dialog_message, "dialog" );

        var res = dialogMessage( msg, type, title, time );

        clock.tick( 100 );

        assert.equal( stub.setTimeout.callCount, 2, 'setTimeout should be called 1 + 1 times' ); 
        // zero call of setTimeout is probably associated with spying
        assert.deepEqual( trim_all_spaces( stub.setTimeout.args[1][0] ), 
                          trim_all_spaces( timeout_arg ), 'setTimeout should be called with 0. arg' );
        assert.deepEqual( stub.setTimeout.args[1][1], time, 'setTimeout should be called with 1. arg' );
        assert.equal( stub.get_dlgClass.callCount, 1, 'get_dlgClass should be called ones' );
        assert.ok( stub.get_dlgClass.calledWithExactly( type ), 'get_dlgClass should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called ones' );
        assert.ok( stub.html.calledWithExactly( msg ), 'html should be called with arg' );
        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 4 times' );
        assert.ok( stub.dialog.getCall( 0 ).calledWithExactly( "option", "dialogClass", dlgClass ), '0 dialog arg' );
        assert.ok( stub.dialog.getCall( 1 ).calledWithExactly( "open" ),                            '1 dialog arg' );
        assert.ok( stub.dialog.getCall( 2 ).calledWithExactly( "close" ),                           '3 dialog arg' );
        assert.equal( res, undefined, 'dialogMessage should return undefined' );
        clock.restore();
    });
    QUnit.test( '#3', function ( assert ) {
        expect( 10 );
        clock = sinon.useFakeTimers();
        var msg = "msg";
        var type = "type";
        var title = "title";
        var time = undefined;
        var dlgClass = "dlgClass";
        var timeout_arg = function(){ $dialog_message.dialog( "close" ); };

        stub.setTimeout   = sinon.spy( window, "setTimeout" );
        stub.get_dlgClass = sinon.stub( window, "get_dlgClass" ).returns( dlgClass );
        stub.html         = sinon.spy( $dialog_message, "html" );
        stub.dialog       = sinon.spy( $dialog_message, "dialog" );

        var res = dialogMessage( msg, type, title, time );

        clock.tick( 100 );

        assert.equal( stub.setTimeout.callCount, 1, 'setTimeout should be called 1 + 0 times' ); 
        // zero call of setTimeout is probably associated with spying
        assert.equal( stub.get_dlgClass.callCount, 1, 'get_dlgClass should be called ones' );
        assert.ok( stub.get_dlgClass.calledWithExactly( type ), 'get_dlgClass should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called ones' );
        assert.ok( stub.html.calledWithExactly( msg ), 'html should be called with arg' );
        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 4 times' );
        assert.ok( stub.dialog.getCall( 0 ).calledWithExactly( "option", "dialogClass", dlgClass ), '0 dialog arg' );
        assert.ok( stub.dialog.getCall( 1 ).calledWithExactly( "open" ),                            '1 dialog arg' );
        assert.ok( stub.dialog.getCall( 2 ).calledWithExactly( "option", "title", title ),          '2 dialog arg' );
        assert.equal( res, undefined, 'dialogMessage should return undefined' );
        clock.restore();
        $dialog_message.dialog( "close" );
    });
    QUnit.test( '#4', function ( assert ) {
        expect( 10 );
        clock = sinon.useFakeTimers();
        var msg = "msg";
        var type = "type";
        var title = "title";
        var time = -1;
        var dlgClass = "dlgClass";
        var timeout_arg = function(){ $dialog_message.dialog( "close" ); };

        stub.setTimeout   = sinon.spy( window, "setTimeout" );
        stub.get_dlgClass = sinon.stub( window, "get_dlgClass" ).returns( dlgClass );
        stub.html         = sinon.spy( $dialog_message, "html" );
        stub.dialog       = sinon.spy( $dialog_message, "dialog" );

        var res = dialogMessage( msg, type, title, time );

        clock.tick( 100 );

        assert.equal( stub.setTimeout.callCount, 1, 'setTimeout should be called 1 + 0 times' ); 
        // zero call of setTimeout is probably associated with spying
        assert.equal( stub.get_dlgClass.callCount, 1, 'get_dlgClass should be called ones' );
        assert.ok( stub.get_dlgClass.calledWithExactly( type ), 'get_dlgClass should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called ones' );
        assert.ok( stub.html.calledWithExactly( msg ), 'html should be called with arg' );
        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 4 times' );
        assert.ok( stub.dialog.getCall( 0 ).calledWithExactly( "option", "dialogClass", dlgClass ), '0 dialog arg' );
        assert.ok( stub.dialog.getCall( 1 ).calledWithExactly( "open" ),                            '1 dialog arg' );
        assert.ok( stub.dialog.getCall( 2 ).calledWithExactly( "option", "title", title ),          '2 dialog arg' );
        assert.equal( res, undefined, 'dialogMessage should return undefined' );
        clock.restore();
        $dialog_message.dialog( "close" );
    });
    QUnit.test( '#5', function ( assert ) {
        expect( 9 );
        clock = sinon.useFakeTimers();
        var msg = "msg";
        var type = "type";
        var title = undefined;
        var time = undefined;
        var dlgClass = "dlgClass";
        var timeout_arg = function(){ $dialog_message.dialog( "close" ); };

        stub.setTimeout   = sinon.spy( window, "setTimeout" );
        stub.get_dlgClass = sinon.stub( window, "get_dlgClass" ).returns( dlgClass );
        stub.html         = sinon.spy( $dialog_message, "html" );
        stub.dialog       = sinon.spy( $dialog_message, "dialog" );

        var res = dialogMessage( msg, type, title, time );

        clock.tick( 100 );

        assert.equal( stub.setTimeout.callCount, 1, 'setTimeout should be called 1 + 0 times' ); 
        // zero call of setTimeout is probably associated with spying
        assert.equal( stub.get_dlgClass.callCount, 1, 'get_dlgClass should be called ones' );
        assert.ok( stub.get_dlgClass.calledWithExactly( type ), 'get_dlgClass should be called with arg' );
        assert.equal( stub.html.callCount, 1, 'html should be called ones' );
        assert.ok( stub.html.calledWithExactly( msg ), 'html should be called with arg' );
        assert.equal( stub.dialog.callCount, 2, 'dialog should be called 4 times' );
        assert.ok( stub.dialog.getCall( 0 ).calledWithExactly( "option", "dialogClass", dlgClass ), '0 dialog arg' );
        assert.ok( stub.dialog.getCall( 1 ).calledWithExactly( "open" ),                            '1 dialog arg' );
        assert.equal( res, undefined, 'dialogMessage should return undefined' );
        clock.restore();
        $dialog_message.dialog( "close" );
    });
    QUnit.test( 'folderEmptyMessage', function ( assert ) {
        expect( 3 );

        var f_name = "f_name";
        stub.dialogMessage = sinon.stub( window, "dialogMessage" );

        var res = folderEmptyMessage( f_name );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( "Ця тека порожня.", "", f_name, 1000 ), 
                                                                        'dialogMessage should be called with arg' );
        assert.equal( res, undefined, 'folderEmptyMessage should return undefined' );
    });
    QUnit.test( 'noSelectionMessage', function ( assert ) {
        expect( 3 );

        var f_name = "f_name";
        stub.dialogMessage = sinon.stub( window, "dialogMessage" );

        var res = noSelectionMessage( f_name );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( "Нічого не вибрано!", "Error", f_name, 1000 ), 
                                                                        'dialogMessage should be called with arg' );
        assert.equal( res, undefined, 'noSelectionMessage should return undefined' );
    });
    QUnit.test( 'functionOnDevelopeMessage', function ( assert ) {
        expect( 3 );

        stub.dialogMessage = sinon.stub( window, "dialogMessage" );

        var res = functionOnDevelopeMessage( );

        assert.ok( stub.dialogMessage.calledOnce, 'dialogMessage should be called once' );
        assert.ok( stub.dialogMessage.calledWithExactly( 
                                        "Ця процедура ще розробляється...", "", "", 2000 ), 
                                                                        'dialogMessage should be called with arg' );
        assert.equal( res, undefined, 'functionOnDevelopeMessage should return undefined' );
    });
} );
//=============================================================================
QUnit.module( "browtab_ui buttonClickHandler", function( hooks ) { 
    var ajax_Function;
    var dialogTitle;
    var inputLabel;
    var disabledInput;
    var inputVal;
    var condLabel;
    var condVal;
    var confirmTitle;
    var confirmMsg;
    var selectionCheck;
    var inputType;
    var buttons;
    hooks.beforeEach( function( assert ) {
        stub = {};
        browtab_document_ready_handler( );
        browtab_ui_document_ready_handler( );

        // expected values:
        buttons = [
            {
                text: "Ok",
                click: function( e ) {
                        confirm_dialog( ajax_Function, confirmTitle, confirmMsg );
                        return false;
                }
            },
            {
                text: "Cancel",
                click: dialog_close
            }
        ];

        stub.dialog                              = sinon.stub( jQuery.prototype, "dialog" );
        stub.siblings                            = sinon.spy( jQuery.prototype, "siblings" );
        stub.find                                = sinon.spy( jQuery.prototype, "find" );
        stub.focus                               = sinon.spy( jQuery.prototype, "focus" );
        stub.prop                                = sinon.spy( jQuery.prototype, "prop" );
        stub.val                                 = sinon.spy( jQuery.prototype, "val" );
        stub.text                                = sinon.spy( jQuery.prototype, "text" );
        stub.html                                = sinon.spy( jQuery.prototype, "html" );
        stub.get_dialog_default_buttons          = sinon.stub( window, "get_dialog_default_buttons" ).returns( buttons );
        stub.get_thisfolder_name                 = sinon.stub( window, "get_thisfolder_name" ).returns( 'f_name' );
        stub.noSelectionMessage                  = sinon.stub( window, "noSelectionMessage" );

        // parameters for button-activate-all:
        ajax_Function   = sinon.stub( );
        dialogTitle     = "dialogtitle";
        inputLabel      = "inputlabel";
        inputVal        = "inputVal";
        condVal         = true;
        confirmMsg      = "confirmMsg";
        // ... including parameters which can change function fall:
        selectionCheck  = true;
        condLabel       = "condLabel";
        confirmTitle    = "confirmTitle";
        disabledInput   = true;
        inputType       = undefined;
    } );
    hooks.afterEach( function( assert ) {
        var meth;
        for ( meth in stub ) {
            stub[meth].restore();
        }
    } );
    QUnit.test( '#1: all true', function ( assert ) {
        expect( 44 );

        var res = buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );

        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 3 times' );
        assert.equal( stub.siblings.callCount, 1, 'siblings should be called 1 times' );
        assert.equal( stub.find.callCount, 5, 'find should be called 5 times' );
        assert.equal( stub.focus.callCount, 1, 'focus should be called 1 times' );
        assert.equal( stub.prop.callCount, 2, 'prop should be called 2 times' );
        assert.equal( stub.val.callCount, 1, 'val should be called 1 times' );
        assert.equal( stub.text.callCount, 2, 'text should be called 2 times' );
        assert.equal( stub.html.callCount, 2, 'html should be called 2 times' );
        assert.equal( ajax_Function.callCount, 0, 'ajax_Function should be called 0 times' );
        assert.equal( stub.get_dialog_default_buttons.callCount, 1, 'get_dialog_default_buttons should be called once' );
        assert.equal( stub.get_thisfolder_name.callCount, 0, 'get_thisfolder_name should be called 0 times' );
        assert.equal( stub.noSelectionMessage.callCount, 0, 'noSelectionMessage should be called 0 times' );

        // if ( selectionCheck ) {

        assert.deepEqual( stub.find.thisValues[0], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[0], [ "tr:nth-child(1)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[0], [ nameFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[0], $( "#id_name" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[0], [ "disabled", disabledInput ], 'prop should be called with args' );

        assert.deepEqual( stub.val.thisValues[0], $( "#id_name" ), 'val called as method of proper this' );
        assert.deepEqual( stub.val.args[0], [ inputVal ], 'val should be called with args' );

        assert.deepEqual( stub.text.thisValues[0], $( "label[for='id_name']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[1], [ "label[for='id_name']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[0], [ inputLabel ], 'text should be called with args' );

        // if ( condLabel ){

        assert.deepEqual( stub.find.thisValues[2], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[2], [ "tr:nth-child(2)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[1], [ condFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[1], $( "#id_cond" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[1], [ 'checked', condVal ], 'prop should be called with args' );

        assert.deepEqual( stub.text.thisValues[1], $( "label[for='id_cond']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[3], [ "label[for='id_cond']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[1], [ condLabel ], 'text should be called with args' );

        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[0], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[0], [ "open" ], 'dialog should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[1], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[1], [ "option", "title", dialogTitle ], 'dialog should be called with args' );

        assert.deepEqual( stub.get_dialog_default_buttons.args[0], [ ], 
                                                                'get_dialog_default_buttons should be called with args' );

        // if ( confirmTitle ){                                        // confirmation dialog needed
        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[2], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[2][0], "option", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][1], "buttons", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][2], buttons, 'dialog should be called with args' );
console.log('stub.dialog.args[2][2]=', stub.dialog.args[2][2]);
console.log('               buttons=', buttons);

        // if ( disabledInput ) {                                              // because input field disabled

        assert.deepEqual( stub.siblings.thisValues[0], $dialog_box_form, 'siblings called as method of proper this' );
        assert.deepEqual( stub.siblings.args[0], [ ], 'siblings should be called with args' );
        assert.deepEqual( stub.find.args[4], [ "button:eq(0)" ], 'find should be called with args' );
        assert.deepEqual( stub.focus.args[0], [ ], 'focus should be called with args' );

        //    }
        // }
        // else {

        assert.equal( res, undefined, 'dialogMessage should return undefined' );
    });
    QUnit.test( '#2: selectionCheck = false', function ( assert ) {
        expect( 15 );
        selectionCheck  = false;
        
        var res = buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );

        assert.equal( stub.dialog.callCount, 0, 'dialog should be called 0 times' );
        assert.equal( stub.siblings.callCount, 0, 'siblings should be called 0 times' );
        assert.equal( stub.find.callCount, 0, 'find should be called 0 times' );
        assert.equal( stub.focus.callCount, 0, 'focus should be called 0 times' );
        assert.equal( stub.prop.callCount, 0, 'prop should be called 0 times' );
        assert.equal( stub.val.callCount, 0, 'val should be called 0 times' );
        assert.equal( stub.text.callCount, 0, 'text should be called 0 times' );
        assert.equal( stub.html.callCount, 0, 'html should be called 0 times' );
        assert.equal( ajax_Function.callCount, 0, 'ajax_Function should be called once' );
        assert.equal( stub.get_dialog_default_buttons.callCount, 0, 'get_dialog_default_buttons should not be called' );
        assert.equal( stub.get_thisfolder_name.callCount, 1, 'get_thisfolder_name should be called once' );
        assert.equal( stub.noSelectionMessage.callCount, 1, 'noSelectionMessage should be called once' );

        // if ( selectionCheck ) {
        // else {

        assert.deepEqual( stub.get_thisfolder_name.args[0], [ ], 'get_thisfolder_name should be called with args' );
        assert.deepEqual( stub.noSelectionMessage.args[0], [ "f_name" ], 'noSelectionMessage should be called with args' );

        assert.equal( res, undefined, 'dialogMessage should return undefined' );
    });
    QUnit.test( '#3: condLabel = ""', function ( assert ) {
        expect( 39 );
        condLabel = "";

        var res = buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );

        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 3 times' );
        assert.equal( stub.siblings.callCount, 1, 'siblings should be called 1 times' );
        assert.equal( stub.find.callCount, 4, 'find should be called 4 times' );
        assert.equal( stub.focus.callCount, 1, 'focus should be called 1 times' );
        assert.equal( stub.prop.callCount, 1, 'prop should be called 1 times' );
        assert.equal( stub.val.callCount, 1, 'val should be called 1 times' );
        assert.equal( stub.text.callCount, 1, 'text should be called 1 times' );
        assert.equal( stub.html.callCount, 2, 'html should be called 2 times' );
        assert.equal( ajax_Function.callCount, 0, 'ajax_Function should be called 0 times' );
        assert.equal( stub.get_dialog_default_buttons.callCount, 1, 'get_dialog_default_buttons should be called once' );
        assert.equal( stub.get_thisfolder_name.callCount, 0, 'get_thisfolder_name should be called 0 times' );
        assert.equal( stub.noSelectionMessage.callCount, 0, 'noSelectionMessage should be called 0 times' );

        // if ( selectionCheck ) {

        assert.deepEqual( stub.find.thisValues[0], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[0], [ "tr:nth-child(1)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[0], [ nameFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[0], $( "#id_name" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[0], [ "disabled", disabledInput ], 'prop should be called with args' );

        assert.deepEqual( stub.val.thisValues[0], $( "#id_name" ), 'val called as method of proper this' );
        assert.deepEqual( stub.val.args[0], [ inputVal ], 'val should be called with args' );

        assert.deepEqual( stub.text.thisValues[0], $( "label[for='id_name']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[1], [ "label[for='id_name']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[0], [ inputLabel ], 'text should be called with args' );

        // if ( condLabel ){
        // else {
        
        assert.deepEqual( stub.find.thisValues[2], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[2], [ "tr:nth-child(2)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[1], [ emptyFormTR ], 'html should be called with args' );

        // }

        assert.deepEqual( stub.dialog.thisValues[0], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[0], [ "open" ], 'dialog should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[1], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[1], [ "option", "title", dialogTitle ], 'dialog should be called with args' );

        assert.deepEqual( stub.get_dialog_default_buttons.args[0], [ ], 
                                                                'get_dialog_default_buttons should be called with args' );

        // if ( confirmTitle ){                                        // confirmation dialog needed
        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[2], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[2][0], "option", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][1], "buttons", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][2], buttons, 'dialog should be called with args' );

        // if ( disabledInput ) {                                              // because input field disabled

        assert.deepEqual( stub.siblings.thisValues[0], $dialog_box_form, 'siblings called as method of proper this' );
        assert.deepEqual( stub.siblings.args[0], [ ], 'siblings should be called with args' );
        assert.deepEqual( stub.find.args[3], [ "button:eq(0)" ], 'find should be called with args' );
        assert.deepEqual( stub.focus.args[0], [ ], 'focus should be called with args' );

        //    }
        // }
        // else {

        assert.equal( res, undefined, 'dialogMessage should return undefined' );
    });
    QUnit.test( '#4: confirmTitle = ""', function ( assert ) {
        expect( 44 );
        confirmTitle    = "";
        // expected values:
        buttons[0].click = function( e ) {
            ajax_Function();
            return false;
        };

        var res = buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );

        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 3 times' );
        assert.equal( stub.siblings.callCount, 1, 'siblings should be called 1 times' );
        assert.equal( stub.find.callCount, 5, 'find should be called 5 times' );
        assert.equal( stub.focus.callCount, 1, 'focus should be called 1 times' );
        assert.equal( stub.prop.callCount, 2, 'prop should be called 2 times' );
        assert.equal( stub.val.callCount, 1, 'val should be called 1 times' );
        assert.equal( stub.text.callCount, 2, 'text should be called 2 times' );
        assert.equal( stub.html.callCount, 2, 'html should be called 2 times' );
        assert.equal( ajax_Function.callCount, 0, 'ajax_Function should be called 0 times' );
        assert.equal( stub.get_dialog_default_buttons.callCount, 1, 'get_dialog_default_buttons should be called once' );
        assert.equal( stub.get_thisfolder_name.callCount, 0, 'get_thisfolder_name should be called 0 times' );
        assert.equal( stub.noSelectionMessage.callCount, 0, 'noSelectionMessage should be called 0 times' );

        // if ( selectionCheck ) {

        assert.deepEqual( stub.find.thisValues[0], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[0], [ "tr:nth-child(1)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[0], [ nameFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[0], $( "#id_name" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[0], [ "disabled", disabledInput ], 'prop should be called with args' );

        assert.deepEqual( stub.val.thisValues[0], $( "#id_name" ), 'val called as method of proper this' );
        assert.deepEqual( stub.val.args[0], [ inputVal ], 'val should be called with args' );

        assert.deepEqual( stub.text.thisValues[0], $( "label[for='id_name']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[1], [ "label[for='id_name']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[0], [ inputLabel ], 'text should be called with args' );

        // if ( condLabel ){

        assert.deepEqual( stub.find.thisValues[2], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[2], [ "tr:nth-child(2)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[1], [ condFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[1], $( "#id_cond" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[1], [ 'checked', condVal ], 'prop should be called with args' );

        assert.deepEqual( stub.text.thisValues[1], $( "label[for='id_cond']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[3], [ "label[for='id_cond']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[1], [ condLabel ], 'text should be called with args' );

        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[0], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[0], [ "open" ], 'dialog should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[1], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[1], [ "option", "title", dialogTitle ], 'dialog should be called with args' );

        assert.deepEqual( stub.get_dialog_default_buttons.args[0], [ ], 
                                                                'get_dialog_default_buttons should be called with args' );

        // if ( confirmTitle ){                                        // confirmation dialog needed
        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[2], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[2][0], "option", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][1], "buttons", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][2], buttons, 'dialog should be called with args' );

        // if ( disabledInput ) {                                              // because input field disabled

        assert.deepEqual( stub.siblings.thisValues[0], $dialog_box_form, 'siblings called as method of proper this' );
        assert.deepEqual( stub.siblings.args[0], [ ], 'siblings should be called with args' );
        assert.deepEqual( stub.find.args[4], [ "button:eq(0)" ], 'find should be called with args' );
        assert.deepEqual( stub.focus.args[0], [ ], 'focus should be called with args' );

        //    }
        // }
        // else {

        assert.equal( res, undefined, 'dialogMessage should return undefined' );
    });
    QUnit.test( '#5: disabledInput = false', function ( assert ) {
        expect( 40 );
        disabledInput   = false;

        var res = buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );

        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 3 times' );
        assert.equal( stub.siblings.callCount, 0, 'siblings should be called 0 times' );
        assert.equal( stub.find.callCount, 4, 'find should be called 4 times' );
        assert.equal( stub.focus.callCount, 0, 'focus should be called 0 times' );
        assert.equal( stub.prop.callCount, 2, 'prop should be called 2 times' );
        assert.equal( stub.val.callCount, 1, 'val should be called 1 times' );
        assert.equal( stub.text.callCount, 2, 'text should be called 2 times' );
        assert.equal( stub.html.callCount, 2, 'html should be called 2 times' );
        assert.equal( ajax_Function.callCount, 0, 'ajax_Function should be called 0 times' );
        assert.equal( stub.get_dialog_default_buttons.callCount, 1, 'get_dialog_default_buttons should be called once' );
        assert.equal( stub.get_thisfolder_name.callCount, 0, 'get_thisfolder_name should be called 0 times' );
        assert.equal( stub.noSelectionMessage.callCount, 0, 'noSelectionMessage should be called 0 times' );

        // if ( selectionCheck ) {

        assert.deepEqual( stub.find.thisValues[0], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[0], [ "tr:nth-child(1)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[0], [ nameFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[0], $( "#id_name" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[0], [ "disabled", disabledInput ], 'prop should be called with args' );

        assert.deepEqual( stub.val.thisValues[0], $( "#id_name" ), 'val called as method of proper this' );
        assert.deepEqual( stub.val.args[0], [ inputVal ], 'val should be called with args' );

        assert.deepEqual( stub.text.thisValues[0], $( "label[for='id_name']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[1], [ "label[for='id_name']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[0], [ inputLabel ], 'text should be called with args' );

        // if ( condLabel ){

        assert.deepEqual( stub.find.thisValues[2], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[2], [ "tr:nth-child(2)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[1], [ condFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[1], $( "#id_cond" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[1], [ 'checked', condVal ], 'prop should be called with args' );

        assert.deepEqual( stub.text.thisValues[1], $( "label[for='id_cond']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[3], [ "label[for='id_cond']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[1], [ condLabel ], 'text should be called with args' );

        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[0], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[0], [ "open" ], 'dialog should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[1], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[1], [ "option", "title", dialogTitle ], 'dialog should be called with args' );

        assert.deepEqual( stub.get_dialog_default_buttons.args[0], [ ], 
                                                                'get_dialog_default_buttons should be called with args' );

        // if ( confirmTitle ){                                        // confirmation dialog needed
        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[2], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[2][0], "option", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][1], "buttons", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][2], buttons, 'dialog should be called with args' );

        // if ( disabledInput ) {                                              // because input field disabled
        //    }
        // }
        // else {

        assert.equal( res, undefined, 'dialogMessage should return undefined' );
    });
    QUnit.test( '#6: all true inputType=text', function ( assert ) {
        expect( 44 );
        inputType = 'qwerty';

        var res = buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck, 
                                                inputType );

        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 3 times' );
        assert.equal( stub.siblings.callCount, 1, 'siblings should be called 1 times' );
        assert.equal( stub.find.callCount, 5, 'find should be called 5 times' );
        assert.equal( stub.focus.callCount, 1, 'focus should be called 1 times' );
        assert.equal( stub.prop.callCount, 2, 'prop should be called 2 times' );
        assert.equal( stub.val.callCount, 1, 'val should be called 1 times' );
        assert.equal( stub.text.callCount, 2, 'text should be called 2 times' );
        assert.equal( stub.html.callCount, 2, 'html should be called 2 times' );
        assert.equal( ajax_Function.callCount, 0, 'ajax_Function should be called 0 times' );
        assert.equal( stub.get_dialog_default_buttons.callCount, 1, 'get_dialog_default_buttons should be called once' );
        assert.equal( stub.get_thisfolder_name.callCount, 0, 'get_thisfolder_name should be called 0 times' );
        assert.equal( stub.noSelectionMessage.callCount, 0, 'noSelectionMessage should be called 0 times' );

        // if ( selectionCheck ) {

        assert.deepEqual( stub.find.thisValues[0], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[0], [ "tr:nth-child(1)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[0], [ nameFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[0], $( "#id_name" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[0], [ "disabled", disabledInput ], 'prop should be called with args' );

        assert.deepEqual( stub.val.thisValues[0], $( "#id_name" ), 'val called as method of proper this' );
        assert.deepEqual( stub.val.args[0], [ inputVal ], 'val should be called with args' );

        assert.deepEqual( stub.text.thisValues[0], $( "label[for='id_name']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[1], [ "label[for='id_name']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[0], [ inputLabel ], 'text should be called with args' );

        // if ( condLabel ){

        assert.deepEqual( stub.find.thisValues[2], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[2], [ "tr:nth-child(2)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[1], [ condFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[1], $( "#id_cond" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[1], [ 'checked', condVal ], 'prop should be called with args' );

        assert.deepEqual( stub.text.thisValues[1], $( "label[for='id_cond']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[3], [ "label[for='id_cond']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[1], [ condLabel ], 'text should be called with args' );

        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[0], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[0], [ "open" ], 'dialog should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[1], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[1], [ "option", "title", dialogTitle ], 'dialog should be called with args' );

        assert.deepEqual( stub.get_dialog_default_buttons.args[0], [ ], 
                                                                'get_dialog_default_buttons should be called with args' );

        // if ( confirmTitle ){                                        // confirmation dialog needed
        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[2], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[2][0], "option", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][1], "buttons", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][2], buttons, 'dialog should be called with args' );

        // if ( disabledInput ) {                                              // because input field disabled

        assert.deepEqual( stub.siblings.thisValues[0], $dialog_box_form, 'siblings called as method of proper this' );
        assert.deepEqual( stub.siblings.args[0], [ ], 'siblings should be called with args' );
        assert.deepEqual( stub.find.args[4], [ "button:eq(0)" ], 'find should be called with args' );
        assert.deepEqual( stub.focus.args[0], [ ], 'focus should be called with args' );

        //    }
        // }
        // else {

        assert.equal( res, undefined, 'dialogMessage should return undefined' );
    });
    QUnit.test( '#7: all true inputType=file', function ( assert ) {
        expect( 41 );
        inputType = 'file';

        var res = buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck, 
                                                inputType );

        assert.equal( stub.dialog.callCount, 3, 'dialog should be called 3 times' );
        assert.equal( stub.siblings.callCount, 1, 'siblings should be called 1 times' );
        assert.equal( stub.find.callCount, 5, 'find should be called 5 times' );
        assert.equal( stub.focus.callCount, 1, 'focus should be called 1 times' );
        assert.equal( stub.prop.callCount, 2, 'prop should be called 2 times' );
//        assert.equal( stub.val.callCount, 1, 'val should be called 1 times' );
        assert.equal( stub.text.callCount, 2, 'text should be called 2 times' );
        assert.equal( stub.html.callCount, 2, 'html should be called 2 times' );
        assert.equal( ajax_Function.callCount, 0, 'ajax_Function should be called 0 times' );
        assert.equal( stub.get_dialog_default_buttons.callCount, 1, 'get_dialog_default_buttons should be called once' );
        assert.equal( stub.get_thisfolder_name.callCount, 0, 'get_thisfolder_name should be called 0 times' );
        assert.equal( stub.noSelectionMessage.callCount, 0, 'noSelectionMessage should be called 0 times' );

        // if ( selectionCheck ) {

        assert.deepEqual( stub.find.thisValues[0], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[0], [ "tr:nth-child(1)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[0], [ fileFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[0], $( "#id_file" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[0], [ "disabled", disabledInput ], 'prop should be called with args' );

//        assert.deepEqual( stub.val.thisValues[0], $( "#id_file" ), 'val called as method of proper this' );
//        assert.deepEqual( stub.val.args[0], [ inputVal ], 'val should be called with args' );

        assert.deepEqual( stub.text.thisValues[0], $( "label[for='id_file']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[1], [ "label[for='id_file']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[0], [ inputLabel ], 'text should be called with args' );

        // if ( condLabel ){

        assert.deepEqual( stub.find.thisValues[2], $dialog_box_form, 'find called as method of proper this' );
        assert.deepEqual( stub.find.args[2], [ "tr:nth-child(2)" ], 'find should be called with args' );
        assert.deepEqual( stub.html.args[1], [ condFormTR ], 'html should be called with args' );

        assert.deepEqual( stub.prop.thisValues[1], $( "#id_cond" ), 'prop called as method of proper this' );
        assert.deepEqual( stub.prop.args[1], [ 'checked', condVal ], 'prop should be called with args' );

        assert.deepEqual( stub.text.thisValues[1], $( "label[for='id_cond']" ), 'text called as method of proper this' );
        assert.deepEqual( stub.find.args[3], [ "label[for='id_cond']" ], 'find should be called with args implicitly' );
        assert.deepEqual( stub.text.args[1], [ condLabel ], 'text should be called with args' );

        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[0], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[0], [ "open" ], 'dialog should be called with args' );

        assert.deepEqual( stub.dialog.thisValues[1], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[1], [ "option", "title", dialogTitle ], 'dialog should be called with args' );

        assert.deepEqual( stub.get_dialog_default_buttons.args[0], [ ], 
                                                                'get_dialog_default_buttons should be called with args' );

        // if ( confirmTitle ){                                        // confirmation dialog needed
        // else {
        // }

        assert.deepEqual( stub.dialog.thisValues[2], $dialog_box_form, 'dialog called as method of proper this' );
        assert.deepEqual( stub.dialog.args[2][0], "option", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][1], "buttons", 'dialog should be called with args' );
        assert.deepEqual( stub.dialog.args[2][2], buttons, 'dialog should be called with args' );

        // if ( disabledInput ) {                                              // because input field disabled

        assert.deepEqual( stub.siblings.thisValues[0], $dialog_box_form, 'siblings called as method of proper this' );
        assert.deepEqual( stub.siblings.args[0], [ ], 'siblings should be called with args' );
        assert.deepEqual( stub.find.args[4], [ "button:eq(0)" ], 'find should be called with args' );
        assert.deepEqual( stub.focus.args[0], [ ], 'focus should be called with args' );

        //    }
        // }
        // else {

        assert.equal( res, undefined, 'dialogMessage should return undefined' );
    });
} );

//=============================================================================
