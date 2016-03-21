// JavaScript Document
console.log('start loading user_browtab_ajax.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

/*
 *********************************************************************
 *  Actions in case of success server responce for AJAX or XMLHttpRequest:
 *********************************************************************
 */
function ajaxSuccessHandler( sr ) {
//    console.log('ajax: sr=', sr);
    xhrSuccessHandler( sr );
}
function xhrSuccessHandler( sr ) {
    dialogMessage( sr.message, sr.type, sr.title, 2000  );
    switch ( sr.type ) {
        case 'IncorrectData':
            // dialog remains open, message - red
            break;
        case 'Error': // transfer success, but server tell about error in data
        case 'Forbidden':
        case 'Normal':
        case 'Rename':
        case 'NoChange':
            dialog_box_form_close();
            break;
        case 'Group':
            dialog_box_form_close();
            changeAllElements( sr.group ); // change row
            break;
        case 'Change':
            dialog_box_form_close();
            changeSelElement( sr.changes, sr.supplement ); // change row
            break;
        case 'DeleteRow':
            dialog_box_form_close();
            deleteElement(); // delete selected element
            break;
        default:
            dialog_box_form_close();
            break;
    }
}
/*
 *********************************************************************
 *  Defining data array for send by AJAX:
 *********************************************************************
 */
function getSelElementArr(){
    // only selected element in table
    var arr = {};
    arr.browTabName = $( "#browTabName" ).val(); // name of table for session dictionary
    arr.parent_id   = '';                        // parent folder id - for compatibility with Folders model
    arr.sendMail    = $( "#id_cond" ).prop( "checked" );  // send mail to user condition
    arr.selRowIndex = $( "#selRowIndex" ).val(); // selected row index
    arr.model       = selElement.model;          // selected element model name
    arr.id          = selElement.id;             // selected element id
    arr.name        = selElement.name;           // selected element name
//    console.log('arr=', arr);
    return arr;
}
function getAllElementsArr(){
    // all elements in filtered table
    /* Structure of arr:
    arr = { 'browTabName' : browTabName,
            'parent_id'   : parent_id,
            'selRowIndex' : selRowIndex,
            'elemSet'     : [ elem1, elem1, ... elemN ]
            }
    where elemSet[i] = {'id'    : id,
                        'model' : model,
                        'name'  : name
                        }
    */
    var arr = {};
    var elemSet = [];
    var elem = {};
    arr.browTabName = $( "#browTabName" ).val(); // name of table for session dictionary
    arr.parent_id   = '';   // parent folder id
    arr.sendMail    = $( "#id_cond" ).prop( "checked" );  // send mail to user condition
    arr.selRowIndex = $( "#selRowIndex" ).val(); // selected row index
    var i;
    for ( i=0 ; i<qs_TR_arr.length; i++ ) {
        elem = {};
        elem.id    = qs_TR_arr[i][0].id;
        elem.model = qs_TR_arr[i][0].model;
        elem.name  = qs_TR_arr[i][1];       // get login from 1-st column
        elemSet[i] = elem;
    }
    arr.elemSet = elemSet;
console.log('getAllElementsArr=', arr);
    return arr;
}
/*
 *********************************************************************
 *  AJAX rendering Activate All Accounts form:
 *********************************************************************
 */
function ajax_activateAllAccounts() {
    var arr = getAllElementsArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-activate-all-accounts";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_setMemberAllAccounts() {
    var arr = getAllElementsArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-set-member-all-accounts";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Single Account forms:
 *********************************************************************
 */
function ajax_recognizeAccount() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-recognize-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_denyAccount() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-deny-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_activateAccount() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-activate-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_deactivateAccount() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-deactivate-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_setMemberAccount() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-set-member-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_denyMemberAccount() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-deny-member-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
function ajax_deleteAccount() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/adm/users/ajax-delete-account";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}

/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/

