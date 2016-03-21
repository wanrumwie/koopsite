// JavaScript Document
console.log('start loading folder_browtab.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

var columnsNumber   = 4;        // number of columns in table

/*
 *********************************************************************
 * Handling with HTML for server response handlers:
 *********************************************************************
 */
function setValToHTML( i, j, val, supplement ) {
    // Set val to the <td> in <tr> in <tbody>. i - row (start 0), j - column(start 1).
    // supplement - additional data from server, eg iconpath
    var iconpath = supplement.iconPath;
    var d;
    var s_date, s_size;
    var ii = i + 1; // selector nth-child is "1-indexed"
    var tr_selector = "#browtable tbody tr:nth-child(" + ii + ")";
    var td_selector = "td:nth-child(" + j + ")";
    var selector = tr_selector + " " + td_selector;
    j = parseInt( j, 10 );
    switch ( j ) {
        case 1:
            $( selector ).find( 'img' ).attr( "src", iconpath );
            break;
        case 2:
            $( selector ).find( 'A' ).text( val );
            // icon can change if file ext changes
            if ( $( tr_selector ).find( 'img' ).attr( "src" ) != iconpath ){
                 $( tr_selector ).find( 'img' ).attr( "src", iconpath );
            }
            break;
        case 3:
            d = new Date( val );             // transform f_date (string) to js Date object
            s_date = d.toLocaleDateString();    // format date to dd.mm.yyyy
            $( selector ).find( 'span' ).text( s_date );
            break;
        case 4:
            if ( val === "" ){ s_size = ""; }
            else { s_size = filesize( val ); } // format f_size to "human readable file size String" (c)
            $( selector ).find( 'span' ).text( s_size );
            break;
        default:
            break;
    }
}
/*
 *********************************************************************
 * Handlers of server response:
 *********************************************************************
 */
function set_name_to_selElement( newName ) {
     // Set new name to qs_TR_arr[selRowIndex][0].name and to selElement.name for selected element
    selElement.name = newName;
    qs_TR_arr[selRowIndex][0].name = newName;
}
function addNewElement( changes, supplement  ) {
    // Add new element to html after last row in table
    // and store it in selElement and qs_TR_arr global parameters.
    // changes - array of all values of new row {j: val}, j - column, val - new value.
    // supplement - array of additional data needed for html, eg iconpath.
    // creating empty <tr> in <tbody>:
    var j, TR;
    var f_model = changes[0].model; 
    var f_id    = changes[0].id; 
    var f_name  = changes[0].name;
    var tr_pattern = createEmptyTR( f_model, f_id, f_name);
    $tbody.append( tr_pattern );
    qs_TR_arr.splice( rowsNumber, 0, [] );  // add 1 element at the end of qs_TR_arr  
    rowsNumber = qs_TR_arr.length;          // new number of rows
    selRowIndex = rowsNumber - 1; // start - 0
    // fill <tr> by values:
    setValToHTMLrow( selRowIndex, changes, supplement );
    // changing columns in selected row of 2D-array:
    for ( j in changes ) {  // 0-column changed too
        qs_TR_arr[selRowIndex][j] = changes[j];
    }
    TR = getTRfromTbodyByIndex( selRowIndex );
    qs_TR_arr[selRowIndex][0].TR = TR;
    setSelRow( rowsNumber );
    scrollToRow( selRowIndex );
    selRowFocus();
}
function moveElement() {
     // Remove selected element from html (after moving in another folder)
     // and select its neighbour using selElement global value.
    qs_TR_arr.splice( selRowIndex, 1);  // remove 1 element at index selRowIndex in qs_TR_arr  
    $( selTR ).remove();    // remove TR and child elements. 
    rowsNumber = qs_TR_arr.length;
    setSelRow( selRowIndex ); // former selRowIndex of moved row will point the next (or last) element
    selRowFocus();
}
function createEmptyTR( f_model, f_id, f_name ) {
    // creating blanc <tr ... >...</tr> with f_model and f_id data only :
    var s = '<tr id="tr-#" >';
    for ( var i = 1; i <= columnsNumber; i++ ) { s = s + '<td id="td' + i + '-#" ><<' + i + '>></td>'; }
    s = s + '</tr>';
    s = s.replace( /#/g, f_model + '#' + f_id );    // global replace of # by #12 (e.g.)
    // preparing href:
    var hr;
    switch ( f_model ) {
        case "folder": hr = "/folders/" + f_id + "/contents/"; break;
        case "report": hr = "/folders/report/" + f_id + "/"; break;
    }
    // replacing respective elements :
    s = s.replace( '<<1>>', '<img src="" alt="' + f_model + '"/>' );
    s = s.replace( '<<2>>', '<a id="' + f_model + '#' + f_id + '" href="' + hr + '"></a>' );
    s = s.replace( '<<3>>', '<span></span>' );
    s = s.replace( '<<4>>', '<span></span>' );
    return s;
}

/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/

