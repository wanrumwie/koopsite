// JavaScript Document
console.log('start loading folder_browtab_ajax.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

/*
 *********************************************************************
 *  Actions in case of success server responce for AJAX or XMLHttpRequest:
 *********************************************************************
 */
function ajaxSuccessHandler( sr ) {
    xhrSuccessHandler( sr );
}
function xhrSuccessHandler( sr ) {
    dialogMessage( sr.message, sr.type, sr.title, 2000 );
    switch ( sr.type ) {
        case 'IncorrectData':
            // dialog remains open, message - red
            break;
        case 'Error': // transfer success, but server tell about error in data
        case 'Forbidden':
        case 'Normal':
        case 'NoChange':
            dialog_box_form_close();
            break;
        case 'NewRow':
            dialog_box_form_close();
            addNewElement( sr.changes, sr.supplement ); // add new element; changes has all values of new element
            break;
        case 'Rename':
            dialog_box_form_close();
            changeSelElement( sr.changes, sr.supplement ); // change row
            set_name_to_selElement( sr.changes[0].name ); // new name must be stored in selElement & qs_TR_arr
            break;
        case 'MoveElement':
//            $.jstree.destroy();
            dialog_box_form_close();
            moveElement(); // remove selected element from current folder
            break;
        case 'DeleteRow':
            dialog_box_form_close();
            deleteElement(); // delete selected element
            break;
        default:
            dialog_box_form_close();
            break;
    }
//console.log('after: xhrSuccessHandler( sr )  : ========================');
//console.log('selTR =', selTR);
//console.log('selRowIndex =', selRowIndex);
//console.log('selElement =', selElement);
//console.log('qs_TR_arr[selRowIndex] =', qs_TR_arr[selRowIndex]);
}
/*
 *********************************************************************
 *  Defining data array for send by AJAX:
 *********************************************************************
 */
function getSelElementArr(){
    var arr = {};
    arr.browTabName = $( "#browTabName" ).val(); // name of table for session dictionary
    arr.parent_id   = $( "#parent_id" ).val();   // parent folder id
    arr.selRowIndex = $( "#selRowIndex" ).val(); // selected row index
    arr.model       = selElement.model;          // selected element model name
    arr.id          = selElement.id;             // selected element id
    arr.name        = selElement.name;           // selected element name
//    console.log('arr=', arr);
    return arr;
}
/*
 *********************************************************************
 *  AJAX receiving Folders Tree HTML code:
 *********************************************************************
 */
function ajax_FoldersTreeFromBase_success_handler( json ) {
    var sr = json.server_response;
    dialogFoldersTreeHTML( sr );
}
function ajax_FoldersTreeFromBase_error_handler( xhr ) {
    setStartRow(); // select row for startRowIndex from previous load of this page
    xhrErrorAlert( xhr, 'ajax_FoldersTreeFromBase' );
}
function ajax_FoldersTreeFromBase() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-folders-tree-from-base";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    // dataType = "html";
    as.success  = ajax_FoldersTreeFromBase_success_handler;            
    as.error    = ajax_FoldersTreeFromBase_error_handler;
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Folder Create form:
 *********************************************************************
 */
function ajax_folderCreate() {
    var arr = getSelElementArr();
    arr.name = $( "#id_name" ).val();  // redefine: new folder name
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-folder-create";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Folder Rename form:
 *********************************************************************
 */
function ajax_folderRename() {
    var arr = getSelElementArr();
    arr.name = $( "#id_name" ).val();    // redefine: folder new name
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-folder-rename";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Report Rename form:
 *********************************************************************
 */
function ajax_reportRename() {
    var arr = getSelElementArr();
    arr.name = $( "#id_name" ).val();    // redefine: report new name
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-report-rename";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Element Move dialog:
 *********************************************************************
 */
function ajax_elementMove( target_id ) {
    var arr = getSelElementArr();
    arr.target_id = target_id;                  // additional element in arr
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-element-move";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Folder Delete form:
 *********************************************************************
 */
function ajax_folderDelete() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-folder-delete";
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  AJAX rendering Report Delete form:
 *********************************************************************
 */
function ajax_reportDelete() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    // Changing ajax settings:
    var as = ajax_settings();
    as.url = "/folders/ajax-report-delete" + "/" + arr.id + "/";    // pk added to url as argument for decorator
    as.data = {
            client_request : json_string,
            csrfmiddlewaretoken: csrf_token
        };
    $.ajax( as );
    return false;
}
/*
 *********************************************************************
 *  XMLHttpRequest rendering Report and Folder Download forms:
 *********************************************************************
 */
function xhr_reportDownload() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    var encoded_json_string = encodeURIComponent( json_string );
    var url = "/folders/ajax-report-download";
    var listeners = listeners_setting();
    listeners.load   = transferSuccessDownload;
    xhr_POST( url, encoded_json_string, listeners );
}
function xhr_folderDownload() {
    var arr = getSelElementArr();
    var json_string = JSON.stringify( arr );
    var encoded_json_string = encodeURIComponent( json_string );
    var url = "/folders/ajax-folder-download";
    var listeners = listeners_setting();
    listeners.load   = transferSuccessDownload;
    xhr_POST( url, encoded_json_string, listeners );
}
/*
 *********************************************************************
 *  XMLHttpRequest rendering Report Upload form:
 *********************************************************************
 */
function xhr_reportUpload() {
//    var input = document.getElementById( 'id_file' );
    var input = $( '#id_file' );
    var file = input[0].files[0];
    if ( !file ){
        dialogMessage( "File name empty", "Error", "File name empty title", 2000 );
        return;
    }
    var arr = getSelElementArr();
    arr.fileName = file.name;
    arr.fileSize = file.size;
    arr.fileType = file.type;
    arr.fileLastModifiedDate = file.lastModifiedDate;
    var json_string = JSON.stringify( arr );
    var encoded_json_string = encodeURIComponent( json_string );
    var url = "/folders/ajax-report-upload";
    var listeners = listeners_setting();
    xhr_POST( url, encoded_json_string, listeners, file );
}


/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/
