// JavaScript Document
console.log('start loading browtab_sort.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

var orderAsc = [];        // set of values: ascending (+1) or decsendind (-1) order for columns  
var orderGroup = false;   // if true - ordering with Folders first, otherwise - mixed

// Order buttons:
function appendOrderButtons( ifirst, ilast ){
    var col, s;
    for ( col = ifirst ; col <= ilast ; col++ ){
        s = "#button-sort-" + col;
        $( s ).button();
        orderAsc[col] = 0;
    }
}
function clearOrderIcons( ifirst, ilast ){
    var col, s;
    var img = "ui-icon-blank";
    for ( col = ifirst ; col <= ilast ; col++ ){
        s = "#button-sort-" + col;
        $( s ).button( "option", "icons", { secondary: img } );
        orderAsc[col] = 0;
    }
}
function changeOrderIcon( col, ifirst, ilast ){
    var img;
    var asc = orderAsc[col];
    clearOrderIcons( ifirst, ilast );
    if ( asc === 0 ) { asc  =  1; }
    else             { asc *= -1; }
    switch ( asc ){
        case -1: img = "ui-icon-carat-1-s"; break;
        case  0: img = "ui-icon-blank";     break;
        case  1: img = "ui-icon-carat-1-n"; break;
        default: img = "ui-icon-blank";     break;
    }
    var s = "#button-sort-" + col;
    $( s ).button( "option", "icons", { secondary: img } );
    orderAsc[col] = asc;
}
function changeOrderGroupIcon( col ){
    orderGroup = !orderGroup;
    var img = ( orderGroup ) ? "ui-icon-transfer-e-w" : "ui-icon-shuffle";
    var s = "#button-sort-" + col;
    $( s ).button( "option", "icons", { secondary: img } );
}
function get_ordered_col(){
    var i;
	var col = 0;
    for ( i = 1 ; i < orderAsc.length ; i++ ){
		if ( orderAsc[i] != 0 ){
			col = i;
			break;
		}
    }
	return col;
}
 


/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/

