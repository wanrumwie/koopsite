// jQuery UI Document
console.log('start loading folder_browtab_ui.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

// document_ready_handler called from html:
function folder_browtab_ui_document_ready_handler(){
    add_tree_dialog();
    add_folder_browtab_ui_buttons();
    set_folder_browtab_ui_buttons_listeners();
}
// Adding UI buttons (only icons) to <button>:
function add_folder_browtab_ui_buttons(){
    $( "#button-create-folder" ).button({
        icons: {
            primary:    "ui-icon-plus",
            secondary:  "ui-icon-folder-collapsed"
        }
    });
    $( "#button-upload-report" ).button({
        icons: {
            primary:    "ui-icon-arrowthickstop-1-n",
            secondary:  "ui-icon-document"
        }
    });
    $( "#button-download-element" ).button({
        icons: {
            primary:    "ui-icon-arrowthickstop-1-s",
            secondary:  "ui-icon-tag"
        }
    });
    $( "#button-rename-element" ).button({
        icons: {
            primary:    "ui-icon-pencil",
            secondary:  "ui-icon-tag"
        }
    });
    $( "#button-move-element" ).button({
        icons: {
            primary:    "ui-icon-cart",
            secondary:  "ui-icon-tag"
        }
    });
    $( "#button-delete-element" ).button({
        icons: {
            primary:    "ui-icon-trash",
            secondary:  "ui-icon-tag"
        }
    });
}
// Opening dialogs
function set_folder_browtab_ui_buttons_listeners( ){
    $( "#button-create-folder"      ).off( "click" ).on( "click", button_create_folder_handler );
    $( "#button-upload-report"      ).off( "click" ).on( "click", button_upload_report_handler );
    $( "#button-download-element"   ).off( "click" ).on( "click", button_download_element_handler );
    $( "#button-rename-element"     ).off( "click" ).on( "click", button_rename_element_handler );
    $( "#button-move-element"       ).off( "click" ).on( "click", button_move_element_handler );
    $( "#button-delete-element"     ).off( "click" ).on( "click", button_delete_element_handler );
}
function button_create_folder_handler() {
    var ajax_Function   = ajax_folderCreate; 
    var dialogTitle     = "Нова тека";
    var inputLabel      = "Назва теки";
    var disabledInput   = false;
    var inputVal        = "Тека без назви";
    var condLabel       = "";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_upload_report_handler() {
    var ajax_Function   = xhr_reportUpload; 
    var dialogTitle     = "Новий файл";
    var inputLabel      = "Назва файла";
    var disabledInput   = false;
    var inputVal        = "Тека без назви";
    var condLabel       = "";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    var inputType       = 'file';
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck,
                                                inputType );
    return false;
}
function button_download_element_handler() {
    var ajax_Function;
    var dialogTitle;
    var inputLabel;
    if ( selElement.model == "folder" ) {
        ajax_Function   = xhr_folderDownload;
        dialogTitle     = "Завантаження теки";
        inputLabel      = "Завантажити";
    }
    else if ( selElement.model == "report" ) {
        ajax_Function   = xhr_reportDownload; 
        dialogTitle     = "Завантаження файла";
        inputLabel      = "Завантажити";
    }
    var disabledInput   = true;
    var inputVal        = selElement.name;
    var condLabel       = "";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_rename_element_handler() {
    var ajax_Function;
    var dialogTitle;
    var inputLabel;
    if ( selElement.model == "folder" ) {
        ajax_Function   = ajax_folderRename;
        dialogTitle     = "Перейменування теки";
        inputLabel      = "Нова назва";
    }
    else if ( selElement.model == "report" ) {
        ajax_Function   = ajax_reportRename; 
        dialogTitle     = "Перейменування файла";
        inputLabel      = "Нова назва";
    }
    var disabledInput   = false;
    var inputVal        = selElement.name;
    var condLabel       = "";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_delete_element_handler() {
    var ajax_Function;
    var dialogTitle;
    var inputLabel;
    if ( selElement.model == "folder" ) {
        ajax_Function   = ajax_folderDelete;
        dialogTitle     = "Видалення теки";
        inputLabel      = "Видалити";
    }
    else if ( selElement.model == "report" ) {
        ajax_Function   = ajax_reportDelete; 
        dialogTitle     = "Видалення файла";
        inputLabel      = "Видалити";
    }
    var disabledInput   = true;
    var inputVal        = selElement.name;
    var condLabel       = "";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_move_element_handler() {
    var f_name;
    var selectionCheck  = check_selRowIndex_range();
    if ( selectionCheck ) {
        ajax_FoldersTreeFromBase(); // in case of success transform this ajax function 
                                    // will call dialogFoldersTreeHTML(sr) 
    }
    else {
        f_name = get_thisfolder_name();    // parent folder name
        noSelectionMessage( f_name );
    }
    return false;
}
// Adding UI dialog form (with common properties) to div:
function add_tree_dialog(){
    $( "#dialog-box-tree" ).dialog({
        dialogClass:    "no-close",
        autoOpen:       false,
        modal:          true,
        closeOnEscape:  true,
        height:         Math.round( 1.2 * dialog_width() ),
        width:          Math.round( 1.5 * dialog_width() ),
        close:          tree_onClose_handler,
        buttons:        get_dialog_default_buttons()   // no comma - last item in array
    });
}
function tree_onClose_handler(){
    selRowFocus();
    $.jstree.destroy();
    return false;
}
function dialogFoldersTreeHTML( sr ) {    // callse by ajax_FoldersTreeFromBase() if success
    var parent_id = $( "#parent_id" ).val();
    var target_id = parent_id;              // id of target folder to move selected element
    var dialogTitle;
    $( '#folders-tree-container' ).html( sr );
    $( '#folders-tree-container' ).jstree();
    $( '#folders-tree-container' ).jstree( "set_theme", "koopstyle" ); 
    $( '#folders-tree-container' ).jstree( 'show_node', parent_id );
    $( '#folders-tree-container' ).jstree( 'select_node', parent_id );
    $( '#folders-tree-container' ).on( 'changed.jstree', function( e, data ) {
            target_id = data.selected[0];  // selected taget is the first element of data.selected 1D array
    });
    $( "#dialog-box-tree" ).dialog( "open" );
    if ( selElement.model == "folder" ) {
        dialogTitle = "Перемістити виділену теку до теки...";
    }
    else if ( selElement.model == "report" ) {
        dialogTitle = "Перемістити файл до теки...";
    }
    $( "#dialog-box-tree" ).dialog( "option", "title", dialogTitle );
    // Redefine function on click for button nr 0:
    var buttons = get_dialog_default_buttons();
    buttons[0].click = function( e ) {
        $( "#dialog-box-tree" ).dialog( "close" );
        ajax_elementMove( target_id );
        return false;
    };
    buttons[1].click = function( e ) {
        $( this ).dialog( "close" );
        return false;
    };
    $( "#dialog-box-tree" ).dialog( "option", "buttons", buttons ); // new buttons
}


/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/




console.log('folder_browtab_ui is loaded' );
