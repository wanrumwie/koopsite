// jQuery UI Document
console.log('start loading user_browtab_ui.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

// document_ready_handler called from html:
function users_browtab_ui_document_ready_handler(){
    add_users_browtab_ui_buttons();
    set_users_browtab_ui_buttons_listeners();
}
// Adding UI buttons (only icons) to <button>:
function add_users_browtab_ui_buttons(){
    $( "#button-activate-all" ).button({
        icons: {
            primary:    "ui-icon-unlocked",
            secondary:  "ui-icon-folder-collapsed"
        }
    });
    $( "#button-set-member-all" ).button({
        icons: {
            primary:    "ui-icon-person",
            secondary:  "ui-icon-folder-collapsed"
        }
    });
    $( "#button-recognize-account" ).button({
        icons: {
            primary:    "ui-icon-check",
            secondary:  "ui-icon-tag"
        }
    });
    $( "#button-deny-account" ).button({
        icons: {
            primary:    "ui-icon-cancel",
            secondary:  "ui-icon-tag"
        }
    });
    $( "#button-activate-account" ).button({
        icons: {
            primary:    "ui-icon-unlocked",
            secondary:  "ui-icon-tag"
        }
    });
    $( "#button-deactivate-account" ).button({
        icons: {
            primary:    "ui-icon-locked",
            secondary:  "ui-icon-tag"
        }
    });
    $( "#button-set-member-account" ).button({
        icons: {
            primary:    "ui-icon-person",
            secondary:  "ui-icon-tag"
        }
    });
    $( "#button-deny-member-account" ).button({
        icons: {
            primary:    "ui-icon-cancel",
            secondary:  "ui-icon-tag"
        }
    });
    $( "#button-delete-account" ).button({
        icons: {
            primary:    "ui-icon-trash",
            secondary:  "ui-icon-tag"
        }
    });
}
// Opening dialogs
function set_users_browtab_ui_buttons_listeners( ){
    $( "#button-activate-all"       ).off( "click" ).on( "click", button_activate_all_handler );
    $( "#button-set-member-all"     ).off( "click" ).on( "click", button_set_member_all_handler );
    $( "#button-recognize-account"  ).off( "click" ).on( "click", button_recognize_account_handler );
    $( "#button-deny-account"       ).off( "click" ).on( "click", button_deny_account_handler );
    $( "#button-activate-account"   ).off( "click" ).on( "click", button_activate_account_handler );
    $( "#button-deactivate-account" ).off( "click" ).on( "click", button_deactivate_account_handler );
    $( "#button-set-member-account" ).off( "click" ).on( "click", button_set_member_account_handler );
    $( "#button-deny-member-account").off( "click" ).on( "click", button_deny_member_account_handler );
    $( "#button-delete-account"     ).off( "click" ).on( "click", button_delete_account_handler );
}
function button_activate_all_handler() {
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
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_set_member_all_handler() {
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
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_recognize_account_handler() {
    var ajax_Function   = ajax_recognizeAccount; 
    var dialogTitle     = "Підтвердження акаунту";
    var inputLabel      = "Підтвердити";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_deny_account_handler() {
    var ajax_Function   = ajax_denyAccount; 
    var dialogTitle     = "Відмова підтвердження акаунту";
    var inputLabel      = "Відмовити";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_activate_account_handler() {
    var ajax_Function   = ajax_activateAccount; 
    var dialogTitle     = "Активація акаунту";
    var inputLabel      = "Активувати";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = true;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_deactivate_account_handler() {
    var ajax_Function   = ajax_deactivateAccount; 
    var dialogTitle     = "Деактивація акаунту";
    var inputLabel      = "Деактивувати";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = true;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_set_member_account_handler() {
    var ajax_Function   = ajax_setMemberAccount; 
    var dialogTitle     = "Права доступу члена кооперативу";
    var inputLabel      = "Надати";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = true;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_deny_member_account_handler() {
    var ajax_Function   = ajax_denyMemberAccount; 
    var dialogTitle     = "Права доступу члена кооперативу";
    var inputLabel      = "Вилучити";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "Повідомити ч/з email";
    var condVal         = false;
    var confirmTitle    = "";
    var confirmMsg      = "";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}
function button_delete_account_handler() {
    var ajax_Function   = ajax_deleteAccount; 
    var dialogTitle     = "Видалення акаунту";
    var inputLabel      = "Видалити";
    var disabledInput   = true;
    var inputVal        = getLoginNameFlatbyIndex( selRowIndex );
    var condLabel       = "";
    var condVal         = false;
    var confirmTitle    = "Видалення акаунту";
    var confirmMsg      = "Замість видалення акаунт краще деактивувати. " + 
                                                            "Ви наполягаєте на видаленні?";
    var selectionCheck  = check_selRowIndex_range();
    buttonClickHandler( ajax_Function, dialogTitle, inputLabel, disabledInput, inputVal, 
                                                condLabel, condVal, confirmTitle, confirmMsg, selectionCheck );
    return false;
}

/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/


console.log('users_browtab_ui is loaded' );
