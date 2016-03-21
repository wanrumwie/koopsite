// JavaScript Document
console.log('start loading user_browtab_sort.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/
 
// document_ready_handler called from html:
function users_browtab_sort_document_ready_handler(){
	appendOrderButtons( 1, columnsNumber );
	changeOrderIcon( 1, 1, columnsNumber );
	set_users_browtab_sort_buttons_listeners();
}
// Set listener for ordering buttons:
function set_users_browtab_sort_buttons_listeners(){
    var selector, i;
    for ( i = 1 ; i <= columnsNumber ; i++ ) {
        selector = "#button-sort-" + i;
        $( selector ).off( "click" ).on( "click", function() {
			var s = 'button-sort-';
			var len = s.length;
			var col = this.id.slice( len );
			col = parseInt( col, 10 );
			ordering( col ); 
		});
    }
}
function ordering( col ){
    changeOrderIcon( col, 1, columnsNumber );
    qs_TR_arr = sort_table( qs_TR_arr, col, orderAsc[col] );
    display_qs_TR_arr();
}
// convert flan No string to number (e.g. "1" to 1 but "1a" to 1.097)
function parseFlatNo( s ){   
	var i, first, c, d;
    var z = parseFloat( s );
	if ( isNaN( z ) ){
		z = 0;
	}
	for ( i=0; i<s.length; i++ ){
		if ( !$.isNumeric( s[i] ) ){
			first=i;	// position of the first not numerical char in string s
			break;
		}
	}
	var divider = 1000;
	if ( first != undefined ){
		s = s.toLowerCase();
		for ( i=first; i<s.length; i++ ){
			c = s.charCodeAt( i );
			d = c / divider;
			z = z + d;
			divider = divider * 1000;
		}
	}
    return z;
}
// convert flan No string to number (e.g. "1" to 1 but "1a" to 1.097)
function parseBoolNull( b ){   
	var z;
	if ( b === true ){ z = 1; }
	else if ( b === null ) { z = 0; }
	else { z = -1; }
    return z;
}
// Sort 2D-array: queryset data + <TR> object:
function sort_table( arr, col, asc ){
    // sort the array by the specified column number (col) and order (asc)
    var x, y, dif;
    arr.sort( function( a, b ){
            x = a[col];     // rename comparison fields for simplisity
            y = b[col];
            switch ( col ) {
                case 1:
                case 2:
                case 4:
                    // string -> lower case for comparison
                    x = x.toLowerCase();
                    y = y.toLowerCase();
                    break;
                case 3:         // "78" --> 78 , "78a" --> 78.097
                    x = parseFlatNo( x );
                    y = parseFlatNo( y );
                    break;
                case 6:         // true --> 1 , false --> -1 , null --> 0
                    x = parseBoolNull( x );
                    y = parseBoolNull( y );
                    break;
                default:        // other fields
                    break;
            }
			dif = ( x == y ) ? 0 : (( x > y ) ? asc : -1*asc );
        return dif;
    });
    return arr;
}

/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/
 
