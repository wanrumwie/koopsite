// JavaScript Document
console.log('start loading folder_browtab_sort.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/
// document_ready_handler called from html:
function folder_browtab_sort_document_ready_handler(){
	appendOrderButtons( 1, columnsNumber );
	changeOrderIcon( 2, 2, columnsNumber );
	changeOrderGroupIcon( 1 );
	set_folder_browtab_sort_buttons_listeners();
}
// Set listener for ordering buttons:
function set_folder_browtab_sort_buttons_listeners( ){
    var selector, i;
    for ( i = 1 ; i <= columnsNumber ; i++ ) {
        selector = "#button-sort-" + i;
        $( selector ).off( "click" ).on( "click", function() {
			var s = 'button-sort-';
			var len = s.length;
			var col = this.id.slice( len );
			col = parseInt( col, 10 );
			if ( col == 1 ) { grouping( col ); }
			else 			{ ordering( col ); }
		});
    }
}
function grouping( col ){
    changeOrderGroupIcon( col );
    // searching ordered column:
    var ordered_col = orderAsc.indexOf(1); // searching index of asc.ordered column  
    ordered_col = ( ordered_col == -1 ) ? orderAsc.indexOf(-1) : ordered_col;   // probably order is descending
    // reorder column with changed group parameter
    qs_TR_arr = sort_table( qs_TR_arr, ordered_col, orderAsc[ordered_col] );
    display_qs_TR_arr();
}
function ordering( col ){
    changeOrderIcon( col, 2, columnsNumber );
    qs_TR_arr = sort_table( qs_TR_arr, col, orderAsc[col] );
    display_qs_TR_arr();
}
// Sort 2D-array: queryset data + <TR> object:
function sort_table( arr, col, asc ){
    var x, y, dif;
    // sort the array by the specified column number (col) and order (asc)
    arr.sort( function( a, b ){
        if ( ( a[1] == b[1] ) || !orderGroup ) {   
            // model names match or ordering with mixed folders and reports
            x = a[col];     // rename comparison fields for simplisity
            y = b[col];
            switch ( col ) {
                case 2:         // string -> lower case for comparison
                    x = x.toLowerCase();
                    y = y.toLowerCase();
                    break;
                default:        // unknown field ?
                    break;
            }
			dif = ( x == y ) ? 0 : (( x > y ) ? asc : -1*asc );
        }
        else {                      // model names mismatch ang orderGroup==True
            dif = ( a[1] > b[1] ) ? 1 : -1 ;    // "folders" first, then "reports"
        }
        return dif;
    });
    return arr;
}
 

/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/


