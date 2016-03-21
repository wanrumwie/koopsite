// JavaScript Document
console.log('start loading browtab.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

var qs_TR_arr;       // 2D Array of queryset data from server + TR DOM object for each table row.
var qs_TR_arr_start; // the same, obtained from view at start of loaded ppage end still unchanged.
var rowsNumber;		 // rows number in current qs_TR_arr (e.g. after filter applied)
var rowsNumber_start;// rows number in qs_TR_arr_start
var TR_start;   	 // array for storing <tr> data immediately after page loaded
var selTR;           // selected <tr> DOM in <tbody>
var selRowIndex;     // index of currently selected row
var selElement; 	 // object = selElement.model , selElement.id , selElement.name
var selectStyle;
var normalStyle;
var $tbody;

// document_ready_handler called from html:
function browtab_document_ready_handler(){
	TR_start = [];   // array for storing <tr> data immediately after page loaded
	selElement = {}; // object = selElement.model , selElement.id , selElement.name
	selectStyle = "selected";
	normalStyle = "normal";
	$tbody = $( "#browtable tbody" );
    set_browtab_listeners(); 
}

function set_browtab_listeners( ){
    $tbody.off( "click",    "td").on( "click",    "td", onClick_handler );
    $tbody.off( "dblclick", "td").on( "dblclick", "td", onDblclick_handler );
    $tbody.off( "keydown",  "td").on( "keydown",  "td", onKeydown_handler );
}
function onClick_handler( event ) {
    selectRow( event.currentTarget );
    return false; // - acts as event.preventDefault() and event.stopPropagation() both.
}
function onDblclick_handler( event ) {
    selectRow( event.currentTarget );
    runhref();
    return false;
}
function onKeydown_handler( event ) {
    onKeyDown( event.which );
    return false;
}

/*
Event handlers are bound only to the currently selected elements; 
they must exist at the time your code makes the call to .on()
Thus, Click event doesn't trigger the event on dynamically created elements.
We must use on() method with selector to refer handler as delegated to inner elements (even yet not existing).
*/
/*
This not works for dynamically created elements:
$(document).ready(function(){
    $('table.browtable tbody td').click(function(event){
        event.preventDefault();
        selectRow(this);
    });
});
*/

function setStartRow() {    // select row with startRowIndex from template
    var model = $( "#selElementModel" ).val();
    var id    = $( "#selElementID" ).val();
    id = Number( id );
    selRowIndex = $( "#selRowIndex" ).val();
    selRowIndex = Number( selRowIndex );
    if ( selRowIndex === undefined ) {
        selRowIndex = 0;    
    }
    setSelRow( selRowIndex );
}
function setSelRow( i ){
    selRowIndex = getSelRowIndexLimited( i );
    if ( rowsNumber > 0 ) {
        // selTR = rowList[selRowIndex];
        selTR = getTRbyIndex( selRowIndex );
        scrollToRow( selRowIndex );
        markSelRow();
    }
}
function getSelRowIndexLimited( i ){
    if ( rowsNumber > 0 ) {
        if ( i < 0 )           { i = 0; }
        if ( i >= rowsNumber ) { i = rowsNumber - 1; }
        selRowIndex = i;
    }
    else {
        selRowIndex = 0;
    }
    return selRowIndex;
}
function check_selRowIndex_range(){
    var bool = selRowIndex >= 0 && selRowIndex < rowsNumber;
	return bool;
}
function get_thisfolder_name(){
    var f_name = $( "#thisfolder span" ).text();    // name of parent folder or users table
	return f_name;
}
function selRowFocus(){
    // set focus to href in selected row
	if ( selTR !== undefined ) {
		selTR.find( 'A' ).focus();
	}
}
function markSelRow() {
    $( '.' + selectStyle ).toggleClass( selectStyle );  // set row elements to normal style
    $( selTR ).toggleClass( selectStyle );             // change Style of all selected row children
    selElement = get_m_id_n_ByIndex( selRowIndex );     // Get model, name & id of selected element
    storeSelRowIndex();                                 // Store selRowIndex in template form:
    selRowFocus();              // set focus to Anchor tag, otherwise BODY will be an active element,
                                // and we can't activate onkeydown in template.
    return false;
}
function runhref() {            // runhref can be tested by functional tests only!
    location.href = $( selTR ).find( 'A' ).attr( 'href' );
}
function storeSelRowIndex() {
    var change = false;
    if ( $( '#selRowIndex' ).val() != selRowIndex ) {
         $( '#selRowIndex' ).val( selRowIndex );
        change = true;
    }
    if ( $( '#selElementModel' ).val() != selElement.model ) {
         $( '#selElementModel' ).val( selElement.model );
        change = true;
    }
    if ( $( '#selElementID' ).val() != selElement.id ) {
         $( '#selElementID' ).val( selElement.id );
        change = true;
    }
    if ( change ) {
        $( '#selRowIndex' ).trigger( 'change' );  // actibation of data exchange with session
    }
}
function selectRow( targ ) {    // select row in case of mouse click on it
    // targ - element clicked directly, selTR - closest TR element:
    selTR = $( targ ).closest( "tr" );
    selRowIndex = $( selTR )[0].sectionRowIndex; // within section, i.e. TBODY in this case
    markSelRow();
    return false;
}
function onKeyDown( k ) {       // select row in case of keyboard arrows pressed
    var s = '';
    var iShift;
    var arr;
    switch( k ) {     // look for k - code of pressed key
        case 13:    iShift =     0; s = 'Enter key';        break;
        case 33:    iShift =    -9; s = 'Page up';          break;
        case 34:    iShift =     9; s = 'Page down';        break;
        case 35:    iShift =  1000; s = 'End key';          break;
        case 36:    iShift = -1000; s = 'Home key';         break;
        case 37:    iShift =    -1; s = 'Left arrow key';   break;
        case 38:    iShift =    -1; s = 'Up arrow key';     break;
        case 39:    iShift =     1; s = 'Right arrow key';  break;
        case 40:    iShift =     1; s = 'Down arrow key';   break;
        default:    iShift = undefined;  s = undefined;     break;
    }
    if ( iShift !== undefined ) {
        if ( iShift === 0 ) { // Enter key
            runhref();
        }
        else { // Arrow keys 
          switch ( iShift ) {
            case 9:
                arr = getVisibleIndex( "#browtable tbody tr" );
                if ( selRowIndex < arr.i_bot ) {
                    iShift = arr.i_bot - selRowIndex;   // PgDn to the bottom of visible area
                }
                else {
                    iShift = arr.i_bot - arr.i_top;     // PgDn to the next screen
                }
                break;
            case -9:
                arr = getVisibleIndex( "#browtable tbody tr" );
                if ( selRowIndex > arr.i_top ) {
                    iShift = arr.i_top - selRowIndex;   // PgUp to the top of visible area
                }
                else {
                    iShift = arr.i_top - arr.i_bot;     // PgUp to the next screen
                }
                break;
            case 1000:
                iShift = rowsNumber;     // to the end of list (with stock)
                break;
            case -1000:
                iShift = -rowsNumber;     // to the begin of list (with stock)
                break;
            default:
                break;
          }
          setSelRow( selRowIndex + iShift ); 
        }
    }
//console.log('onKeyDown:', 'k =', k, 'selRowIndex =', selRowIndex, ' iShift =', iShift);
    return false;
}

/*
 *********************************************************************
 * Create array of queryset data + <TR> object from json_arr for further manipulations:
 *********************************************************************
 */
// TODO-replace value stored in $( "#json_arr" ) in case of any change of records: add, delete, update - needed for restoring before new filter apply
function create_qs_TR_arr() {
    // Create array from #json_arr and + <TR> objects for further ordering:
    qs_TR_arr = get_qs_TR_arr( true );
	rowsNumber_start = rowsNumber;
}
function restore_qs_TR_arr() {
    // Restore array from the same #json_arr and TR_start[]:
    qs_TR_arr = get_qs_TR_arr( false );
}
function getTRfromTbodyByIndex( i ) {
    var TR = $( "#browtable" ).find( "tbody>tr:eq(" + i + ")" );
    return TR;
}
function get_qs_TR_arr( is_start ) {
    var i, j, ob, TR;
    var arr = [];   // 2D array - table
    var json_arr = $( "#json_arr" ).val();
//consile.log('json_arr =', json_arr);  // TODO-this operator terminate function!!!
    var qs_obj = JSON.parse( json_arr ); // Object not Array, because JSON parse num indexes as str
//consile.log('qs_obj =', qs_obj);      // TODO-this operator terminate function!!!
    for ( i in qs_obj ) {
        arr[i] = [];
        if ( is_start ) { // store TR_start for further restoring.
            TR = getTRfromTbodyByIndex( i );
            TR_start[i] = TR;
        }
        else { // restoring from TR_start, eg before new filter apply or filter cancel.
            TR = TR_start[i];
        }
        /*  // old method:
        ob = {};
        ob.TR     = TR;  // add DOM TR object to array as 0th column 
        ob.model  = qs_obj[i][0].model;  
        ob.id     = qs_obj[i][0].id;
        ob.name   = qs_obj[i][0].name;
        arr[i][0] = ob;
        */
        arr[i][0] = qs_obj[i][0];   // arr[i][0] = {model:..., id:..., name:...}
        arr[i][0].TR = TR;          // add DOM TR object: {model:..., id:..., name:..., TR:...}
        for ( j = 1 ; j <= columnsNumber; j++ ) { // simple storing from {} to []
            arr[i][j] = qs_obj[i][j];
        }
    }
    rowsNumber = arr.length;
    return arr;
}

/*
 *********************************************************************
 * Get different data from qs_TR_arr:
 *********************************************************************
 */
function getTRbyIndex( i ) {      // return TR object by index in tbody (start 0)
    var TR = qs_TR_arr[i][0].TR;
    return TR;
}
function get_m_id_n_ByIndex( i ) {      // return TR object by index in tbody (start 0)
    var elem    = {};
    elem.model  = qs_TR_arr[i][0].model;
    elem.id     = qs_TR_arr[i][0].id;
    elem.name   = qs_TR_arr[i][0].name;
    return elem;
}
function getRowIndexbyID( model, id ) { // return row index by model & id
    var i, ind, elem;
    var found = false;
    for ( i = 0 ; i < qs_TR_arr.length; i++ ) {
        elem = get_m_id_n_ByIndex( i ); // [i][0] element is object
        if ( ( id == elem.id ) && ( model == elem.model ) ) {
            ind = i;
            found = true;
            break;
        }
    }
    if ( !found ) { ind = 0; }
    return ind;
}
function getTRbyID( model, id ) { // return TR object by model & id
    var i, TR, elem;
    var found = false;
    for ( i = 0 ; i < qs_TR_arr.length; i++ ) {
        elem = get_m_id_n_ByIndex( i ); // [i][0] element is object
        if ( ( id == elem.id ) && ( model == elem.model ) ) {
            TR = getTRbyIndex( i );
            found = true;
            break;
        }
    }
    if ( !found ) { TR = undefined; }
    return TR;
}

/*
 *********************************************************************
 * Replace <tbody> by qs_TR_arr 2D-array:
 *********************************************************************
 */
function display_qs_TR_arr(){
    var i, TR;
    // removing all <TR> from table
    $( "#browtable tbody tr" ).remove();
    // adding all new <TR> to table
    for ( i = 0 ; i < rowsNumber ; i++ ) {
        TR = getTRbyIndex( i );
        $tbody.append( TR ); 
    }
    selRowIndex = getRowIndexbyID( selElement.model, selElement.id ); // new selRowIndex by unchainged selElement model & id
    setSelRow( selRowIndex );                           // setting new selTR & selElement for just chainged selRowIndex
}

/*
 *********************************************************************
 * Scrolling:
 *********************************************************************
 */
function getSelectorTR( qq, i ){
    // return selector like "#browtable tbody tr:eq(5)" 
    var s = "#browtable tbody tr:" + qq + "(" + i + ")" ;
    return s;
}
function getVisibleIndex( selector ){
    // return object arr.i_top, arr.i_bot - index of top and bottom visible rows respectively
    var hi,
        top_edge_visible,
        bot_edge_visible;
    var arr = {};
    var h_hidden = $tbody.scrollTop();// hidden part above tbody in px
    var h_tbody  = $tbody.height();    // visible tbody height in px
    var h = 0;
    var i = 0;
    var top_found = false;  
    var bot_found = false;  
    var i_top = 0;
    var i_bot = 0;
    $( selector ).each( function() {
            hi = $( this ).outerHeight();   // height of i-th element
            // determining whether top edge of row No i is visible:
            if ( h_hidden === 0 ) { // special case of no hidden area
                top_edge_visible = h >= h_hidden && h + hi*0.45 <= h_hidden + h_tbody;
            }
            else {
                top_edge_visible = h > h_hidden && h + hi*0.45 <= h_hidden + h_tbody;
            }
            h += hi;                        // total height of i+1 elements from 0 to i
            // determining whether bottom edge of row No i is visible:
            bot_edge_visible = h - hi*0.45 > h_hidden && h <= h_hidden + h_tbody;
            if ( !top_found ) { // top visible row still not found:
                top_found = top_edge_visible || bot_edge_visible;
                if ( top_found ) { // top visible row just found:
                    i_top = i;
                    i_bot = i;
                }
            }
            else if ( !bot_found )  { // top visible row is found, but bottom no yet:
                bot_found = !top_edge_visible && !bot_edge_visible; // first hidden row under visible row is found
                if ( !bot_found ) { // row No i is still visible
                    i_bot = i;
                }
            }
            i += 1;
    });
    arr.i_top = i_top;
    arr.i_bot = i_bot;
    return arr;
}
function totalOuterHeight( selector ){
    // total height (outer) of all elements in selector
    var h = 0;
    $( selector ).each( function() {
            h += $( this ).outerHeight();
    });
    return h;
}
function scrollToRow( i ) {
    // scroll tbody to row index i to be visible
    var selectorLtI = getSelectorTR( "lt", i );
    var selectorEqI = getSelectorTR( "eq", i );
    var h_tbody     = $tbody.height();             // visible tbody height in px
    var h_tr        = totalOuterHeight( selectorEqI );               // i-th tr    height in px
    var h_aboveSel  = totalOuterHeight( selectorLtI );      // part of common height above i-th tr
    var h_uptoSel   = h_aboveSel + h_tr;                    // -//- including i-th tr height
    var h_hidden    = $tbody.scrollTop();  // hidden part above tbody in px
    if ( h_hidden >= h_aboveSel ) {                         // i-th row is in hidden area above tbody?
        h_hidden = h_aboveSel;                              // we allow to hide this part of common height
    } else if ( h_uptoSel >= h_hidden + h_tbody ) {         // i-th row is not visible below tbody?
        h_hidden = h_uptoSel - h_tbody;                     // we allow to hide this part of common heiight
    }
    $tbody.scrollTop( h_hidden );   
    return h_hidden;
}

/*
 *********************************************************************
 * Changing both <tbody> and qs_TR_arr 2D-array (functions called from xhrSuccessHandler:
 *********************************************************************
 */
function deleteElement() {
     // Delete selected element from html
     // and select its neighbour using selElement global value.
    qs_TR_arr.splice( selRowIndex, 1 );  // remove 1 element at index selRowIndex in qs_TR_arr  
    $( selTR ).remove();    // remove TR and child elements. 
    rowsNumber = qs_TR_arr.length;
    setSelRow( selRowIndex ); // former selRowIndex of deleted row will point the next (or last) element
    selRowFocus();
}
function setValToHTMLrow( i, changes, supplement ){
    // setting changes in i-th row in html with supplement data:
    // setValToHTML function must be defined for each browtable, i.e. folder_content, user_rable etc.
    var j, val;
    for ( j in changes ) {
        val = changes[j];    
        setValToHTML( i, j, val, supplement ); 
    }
}
function changeSelElement( changes, supplement ) {
    // Changing selected element by the new one in html
    // and store it in selElement and qs_TR_arr global parameters.
    // changes - array of changed only values {j: val}, j - column, val - new value.
    // supplement - array of additional data needed for html, eg iconpath.
    var j;
    for ( j in changes ) {  // changing columns in selected row of 2D-array: 0-column changed too
        qs_TR_arr[selRowIndex][j] = changes[j];
    }
    setValToHTMLrow( selRowIndex, changes, supplement );    // setting changes in selected row in html
    var TR = getTRfromTbodyByIndex( selRowIndex );          // changing TR sub-element in selected row of 2D-array
    qs_TR_arr[selRowIndex][0].TR = TR;
    selRowFocus();
}

/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/

/*
 *********************************************************************
 * Accessory functions for output debug information:
 *********************************************************************
 */
function demoPrint(i, s, append) {
    // Print on html page
    var demoN = "demo" + i;
    if (append === undefined){
        document.getElementById(demoN).innerHTML = i + ": " + s;
    }
    else {
        document.getElementById(demoN).innerHTML =
            document.getElementById(demoN).innerHTML + s;
    }
}

function sList(eList) {
    // eList - list of elements, given by $(...)...
    // Return sList - string consist of all elements id and tagname
    var i;
    var s = '';
    for (i = 0; i < eList.length; i++) {
        s = s + eList[i].tagName + ' ' + eList[i].id + '; ';
    }
    return s;
}

function formatTimeOfDay(millisSinceEpoch) {
  var secondsSinceEpoch = (millisSinceEpoch / 1000) | 0;
  var secondsInDay = ((secondsSinceEpoch % 86400) + 86400) % 86400;
  var seconds = secondsInDay % 60;
  var minutes = ((secondsInDay / 60) | 0) % 60;
  var hours = (secondsInDay / 3600) | 0;
  return hours + (minutes < 10 ? ":0" : ":" ) + minutes + (seconds < 10 ? ":0" : ":" ) + seconds;
}


function test_addNewElement() {
    var ne = {};
    ne.f_model = 'report';
    ne.f_id = '99';
    ne.f_name = 'newname.ext';
    ne.f_ext = '.doc';
    ne.f_type = 'docx';
    ne.f_date = '14.09.2015p.';
    ne.f_size = '123456kB';
    ne.iconpath = '/static/img/word.png';
    addNewElement(ne);
}
