// JavaScript Document
console.log('start loading user_browtab.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

var columnsNumber   = 8;        // number of columns in table

function getLoginNameFlatbyIndex( i ) { 
    // return login+fulname+flat from qs_TR_arr: JohnW (Wood John, flat 15)
    var login = qs_TR_arr[i][1]; // [i][1] element is Login
    var fulln = qs_TR_arr[i][2]; // [i][2] element is full name
    var flatn = qs_TR_arr[i][3]; // [i][3] element is flat No
    var s = login;
    if ( fulln || flatn ) {
        s = s + ' (' + fulln;
        if ( fulln && flatn ) { s = s + ', '; }
        if ( flatn ) { s = s + 'кв.' + flatn; }
        s = s + ')';
    }
    return s;
}
function getElementNamebyIndex( i ) {
    var elName = getLoginNameFlatbyIndex( i );
    return elName;
}
/*
 *********************************************************************
 * Handlers of server response:
 *********************************************************************
 */
function setValToHTML( i, j, val, supplement ) {
    // Set val to the <td> in <tr> in <tbody>. i - row (start 0), j - column(start 1).
    var d;
    var s_date;
    var iconpath;
    var ii = i + 1; // selector nth-child is "1-indexed"
    var tr_selector = "#browtable tbody tr:nth-child(" + ii + ")";
    var td_selector = "td:nth-child(" + j + ")";
    var selector = tr_selector + " " + td_selector;
    j = parseInt( j, 10 );
    switch ( j ) {
        case 1:
            $( selector ).find( 'A' ).text( val );
            break;
        case 2:
        case 3:
        case 4:
            $( selector ).find( 'span' ).text( val );
            break;
        case 5:
            d = new Date( val );             // transform f_date (string) to js Date object
            s_date = d.toLocaleDateString();    // format date to dd.mm.yyyy
            $( selector ).find( 'span' ).text( s_date );
            break;
        case 6:
        case 7:
        case 8:
            iconpath = supplement.iconPath[j];
            $( selector ).find( 'img' ).attr( "src", iconpath );
            break;
        default:
            break;
    }
}
function changeAllElements( group ) {
    // Changing group of elements by the new one in html
    // and store its in selElement and qs_TR_arr global parameters.
    // group - list-array of elements data: { 'model': model, 'id': id, 'changes': changes, 'supplement': supplement }, 
    // where changes - array of changed only values {j: val}, j - column, val - new value;
    //       supplement - additional data to display in html, e.g. iconPath - array of icons for certain TD elements.
    var k, obj, id, model, changes, supplement, i, j, val, TR;
    for ( k in group ){ // group - 1D-array
        obj = group[k];
        model       = obj.model;
        id          = obj.id;
        changes     = obj.changes;    
        supplement  = obj.supplement;    

        i = getRowIndexbyID( model, id );

        // setting changes in group of rows in html:
        setValToHTMLrow( i, changes, supplement ); 

        // changing TR sub-element in group of rows of 2D-array:
        TR = getTRfromTbodyByIndex( i );
        qs_TR_arr[i][0].TR = TR;

        // changing columns in selected row of 2D-array:
        for ( j in changes ) {
            val = changes[j];    
            qs_TR_arr[i][j] = val;
        }
    }
    selRowFocus();
}
/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/


