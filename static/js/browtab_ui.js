// jQuery UI Document
console.log('start loading browtab_ui.js');

var $dialog_box_form;
var $dialog_confirm;
var $dialog_message;

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

// document_ready_handler called from html:
function browtab_ui_document_ready_handler(){
    $dialog_box_form = $( "#dialog-box-form" );
    $dialog_confirm  = $( "#dialog-confirm" );
    $dialog_message  = $( "#dialog-message" );
    add_browtab_ui_dialogs(); 
}
// Adding UI dialog form (with common properties) to div:
function add_browtab_ui_dialogs(){
    $dialog_box_form.dialog({    // main dialog
        dialogClass:    "no-close",
        autoOpen:       false,
        modal:          true,
        closeOnEscape:  true,
        width:          dialog_width(),
        open:           set_Ok_button_on_Enter,
        close:          selRowFocus,
        buttons:        get_dialog_default_buttons()   // no comma - last item in array
    });
    $dialog_confirm.dialog({     // confirm dialog
        dialogClass:    "no-close",
        autoOpen:       false,
        modal:          true,
        closeOnEscape:  true,
        width:          0.8 * dialog_width()
        // buttons:        get_confirm_dialog_default_buttons()   // no comma - last item in array
    });
    $dialog_message.dialog({     // message dialog
        dialogClass:    "no-close",
        autoOpen:       false,
        modal:          true,
        closeOnEscape:  true,
        close:          selRowFocus,
        buttons:        { Ok: dialog_close }   // no comma - last item in array
    });
}
/*
 *********************************************************************
 * Width for dialog widgets:
 *********************************************************************
 */
function dialog_width() {
    var tw = $tbody.width();
    var w = ( tw > 600 ) ? 450 : tw *0.75;
	w = Math.round( w );
    return w;
}
/*
 *********************************************************************
 *  Defining functions returning default "buttons" and "open" options 
 *  common for all UI dialog calls. 
 *********************************************************************
 */
function dialog_close() {
    $( this ).dialog( "close" );
}
function dialog_box_form_close() {
    $dialog_box_form.dialog( "close" );
}
function get_dialog_default_buttons() {
    var buttons = [
        {
            text: "Ok",
            click: undefined // buttons[0].click will be redefined when dialog open
        },
        {
            text: "Cancel",
            click: dialog_close
        }
    ];
    return buttons;
}
function get_confirm_dialog_default_buttons() {
    var buttons = [
        {
            text: "Ok",
            click: undefined // buttons[0].click will be redefined when dialog open
        },
        {
            text: "Cancel",
            click: dialog_close
        }
    ];
    return buttons;
}
function click_Ok_button_on_Enter( e ) {
    if ( e.keyCode == $.ui.keyCode.ENTER ) {
        $( this ).parent().find( "button:contains('Ok')" ).trigger( "click" );
        return false;
    }
}
function set_Ok_button_on_Enter() {
    $( this ).keypress( click_Ok_button_on_Enter );
}
function defineAbortButton( xhr ){
    // Define text and function for the only button during upload file:
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
    $dialog_box_form.dialog( "option", "buttons", buttons );
}
function defineConfirmButtons( ajax_Function ){
    // Define text and function for the confirm dialog buttons in the case of ajax_Function needs confirmation:
    var confirm_buttons = [
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
    $dialog_confirm.dialog( "option", "buttons", confirm_buttons );      // new confirm_buttons
}
// TODO-change confirm_dialog() by decorator for ajax_Function
function confirm_dialog( ajax_Function, confirmTitle, confirmMsg ){
    $dialog_confirm.dialog( "open" );
    $dialog_confirm.dialog( "option", "title", confirmTitle );
    $dialog_confirm.html( confirmMsg );
    defineConfirmButtons( ajax_Function );
    $dialog_confirm.siblings().find( "button:eq(0)" ).focus(); 
}

/*
 *********************************************************************
 * HTML for dynamically created dialogs:
 *********************************************************************
 */
var nameFormLabel = '<label for="id_name">Тека:</label>';
var nameFormInput = '<input id="id_name" maxlength="256" name="name" type="text" autofocus/>';
var nameFormTR    = '<td>' + nameFormLabel + '</td>' +
                    '<td>' + nameFormInput + '</td>';
var fileFormLabel = '<label for="id_file">Файл:</label>';
var fileFormInput = '<input id="id_file" maxlength="256" name="file" type="file" autofocus/>';
var fileFormTR    = '<td>' + fileFormLabel + '</td>' +
                    '<td>' + fileFormInput + '</td>';
var condFormLabel = '<label for="id_cond">Повідомити ч/з email</label>';
var condFormInput = '<input id="id_cond" name="cond" type="checkbox"/>';
var condFormTR    = '<td>' + '</td>' +
                    '<td>' + condFormLabel + condFormInput + '</td>';
var progressTR    = '<td>Progress:</td><td><div id="progressbar"></div></td>';
var emptyFormTR   = '<td></td><td></td>';
/*
 *********************************************************************
 * Progress bar
 *********************************************************************
 */
function progressbarShow(){
    $dialog_box_form.find( "tr:nth-child(2)" ).html( progressTR );
    $( "#progressbar" ).progressbar( { value: 0 } );
}
function setProgress( x, max ){
    var pmax = $( "#progressbar" ).progressbar( "option", "max" );
    if ( pmax === undefined ) { pmax = 100; }
    if ( max === undefined ) { max = pmax; }
    $( "#progressbar" ).progressbar({ 
        value:  x,
        max:    max         
    });
}
function setProgress__TimeOut( x, max ){
    setTimeout( function(){
        var pmax = $( "#progressbar" ).progressbar( "option", "max" );
        if ( pmax === undefined ) { pmax = 100; }
        if ( max === undefined ) { max = pmax; }
            $( "#progressbar" ).progressbar({ 
                value:  x,
                max:    max         
                });
    }, 1000 ); // delay for test purpose
//    alert('progress: x =' + x + '   max =' + max);
}
function progressHandler( pe ) {
    if ( pe.lengthComputable )  { setProgress( pe.loaded, pe.total ); } 
    else                        { setProgress( false ); }
}
function loadEndHandler( pe ) {
    setProgress( pe.loaded );
}
/*
 *********************************************************************
 * Messages
 *********************************************************************
 */
function get_dlgClass( type ){
    var dlgClass = "";
    switch ( type ) {
        case "IncorrectData":   dlgClass = "ui-state-error";        break;
        case "Forbidden":       dlgClass = "ui-state-error";        break;
        case "Error":           dlgClass = "ui-state-error";        break;
        case "Normal":          dlgClass = "ui-state-highlight";    break;
        default:                dlgClass = "ui-state-highlight";    break;
    }
    dlgClass = "no-close" + " " + dlgClass;
    return dlgClass;
}
function dialogMessage( msg, type, title, time ) {
    // Open message dialog of given type
    var dlgClass = get_dlgClass( type );
    $dialog_message.dialog( "option", "dialogClass", dlgClass );
	$dialog_message.dialog( "open" );
	$dialog_message.html( msg );
    if ( title !== undefined ) {
        $dialog_message.dialog( "option", "title", title );
    }
    if ( time !== undefined && time > 0 ) {
        setTimeout( function(){ $dialog_message.dialog( "close" ); }, time );
    }
}
function folderEmptyMessage( f_name ) {
    // This function called from ...ajax.js
	dialogMessage( "Ця тека порожня.", "", f_name, 1000 );
}
function noSelectionMessage( f_name ) {
    // This function called on event dblClick or EnterKey
	dialogMessage( "Нічого не вибрано!", "Error", f_name, 1000 );
}
function functionOnDevelopeMessage() {
	dialogMessage( "Ця процедура ще розробляється...", "", "", 2000 );
}
/*
 *********************************************************************
 * Common body function for opening dialogs
 *********************************************************************
 */
function buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck,
												inputType='text' ) {
    var f_name, inputFormTR, inputID;
    if ( selectionCheck ) {
		if ( inputType == "file" ) {
			inputFormTR = fileFormTR;
			inputID = 'id_file';
		} else {
			inputFormTR = nameFormTR;
			inputID = 'id_name';
		}
		$dialog_box_form.find( "tr:nth-child(1)" ).html( inputFormTR );
		$( "label[for='"+inputID+"']" ).text( inputLabel );
		$( "#"+inputID ).prop( "disabled", disabledInput );          // input field disabled or not
		if ( inputType != "file" ) {
			$( "#"+inputID ).val( inputVal );
		}
        if ( condLabel ){
            $dialog_box_form.find( "tr:nth-child(2)" ).html( condFormTR );
            $( "#id_cond" ).prop('checked', condVal );
            $( "label[for='id_cond']" ).text( condLabel );
        }
        else {
            $dialog_box_form.find( "tr:nth-child(2)" ).html( emptyFormTR );
        }
        $dialog_box_form.dialog( "open" );
        $dialog_box_form.dialog( "option", "title", dialogTitle );
		var buttons = get_dialog_default_buttons();
        if ( confirmTitle ){                                        // confirmation dialog needed
            buttons[0].click = function( e ) {  // ajax "decorated" by confirm_dialog 
                confirm_dialog( ajax_Function, confirmTitle, confirmMsg );
                return false;
            };
        }
        else {                                                      // run ajax without confirmation
            buttons[0].click = function( e ) {
                ajax_Function();
                return false;
            };
        }
        $dialog_box_form.dialog( "option", "buttons", buttons );     // new buttons
        if ( disabledInput ) {                                              // because input field disabled
            $dialog_box_form.siblings().find( "button:eq(0)" ).focus(); 
        }
    }
    else {
        f_name = get_thisfolder_name();    // name of parent folder or users table
        noSelectionMessage( f_name );
    }
}


/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/


// Temporary buttons to open widgets for test purposes

$( "#button-service" ).text("Check Focus");
$( "#button-service" ).on( "click", function() {
    $dialog_box_form.dialog( "open" );
    $dialog_box_form.dialog( "option", "Check Focus" );
    var buttons = get_dialog_default_buttons();
    // Redefine function on click for button nr 0:
    buttons[0].click =
        function(e) {
            $( this ).dialog( "close" );
            selRowFocus();
            return false;
        };
    $dialog_box_form.dialog( "option", "buttons", buttons );
});


$( "#button-service2" ).text("Select child_node");
$( "#button-service2" ).on( "click", function() {
    $(function () {
        $('#folders-tree-container').jstree(true).select_node('child_node');
    }); 
});


    function supportFileAPI() {
        var fi = document.createElement('INPUT');
        fi.type = 'file';
        return 'files' in fi;
    }

    function supportAjaxUploadProgressEvents() {
        var xhr = new XMLHttpRequest();
        return !! (xhr && ('upload' in xhr) && ('onprogress' in xhr.upload));
    }

function supportAjaxUploadWithProgress() {
    return supportFileAPI() && supportAjaxUploadProgressEvents();

}

/*
    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        alert('The File APIs are not fully supported in this browser.');
    } else {
        alert( "The File APIs are fully supported in this browser." );
        }

    if (supportAjaxUploadWithProgress()) {
        alert('AjaxUploadWithProgress is fully supported in this browser.');
    } else {
        alert( "AjaxUploadWithProgress is NOT supported in this browser" );
    }
*/

console.log('browtab_ui is loaded' );
