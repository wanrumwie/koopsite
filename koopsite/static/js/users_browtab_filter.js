// JavaScript Document
console.log('start loading user_browtab_filter.js');

/**********************************************************************
 * START of the code covered by tests
 **********************************************************************/

 //TODO-bug detected: nonfiltered data are displayed after page refresh, but filter flags remain it's valuea.

var radio_names;
var filt_val;
var date_joined_from, date_joined_to;

// document_ready_handler called from html:
function users_browtab_filter_document_ready_handler(){
	appendFilterListeners();
	appendDateFields();
	appendDateFieldsListeners();
	radio_names 		= ['is_recognized', 'is_active', 'has_members', 'date_joined_all'];
	clearFilterFields();
	clearDateFields();
console.log('users_browtab_filter_document_ready_handler');
}
// Set listener for filter buttons:
function appendFilterListeners(){
    $( "#filter_box" ).off( "change", "input" ).on( "change", "input" , filter_handler );
}
// Filtering data:
function applyFilter(){
	restore_data();
    filt_val 	= get_filters();
    qs_TR_arr 	= filter_table( qs_TR_arr );
    rowsNumber 	= qs_TR_arr.length;
    display_qs_TR_arr();
	display_records_info();
}
function cancelFilter(){
	restore_data();
    display_qs_TR_arr();
	display_records_info();
}
function restore_data(){
	var col = get_ordered_col();
	restore_qs_TR_arr();	// restore qs_TR_arr from JSON string and set rowsNumber = qs_TR_arr.length
	qs_TR_arr = sort_table( qs_TR_arr, col, orderAsc[col] );
}
function display_records_info(){
	$( "#records_info_box" ).show();
	$( "#records_info" ).text( rowsNumber + ' / ' + rowsNumber_start );
}
function clearFilterFields(){
    $( "input:radio" ).val( ['all'] );
}
function get_filters(){
    var dict = {};
    var i, n, v, selector; 
    var sel_patt = "#filter_box input:radio[name=<>]:checked";
    for ( i in radio_names ) {
        n = radio_names[i];
        selector = sel_patt.replace( '<>', n );
        v = $( selector ).val();
        dict[n] = v;
    }
    date_joined_from = get_iso_field( "iso_", "#date_joined_from" );
    date_joined_to   = get_iso_field( "iso_", "#date_joined_to" );
    return dict;
}
function get_iso_field( iso, selector ){
    var v, iso_v;
    var iso_selector = "#" + iso + selector.slice(1);
    v = $( selector ).val();
    if ( v === "" || !v ) {
        iso_v = "";
    }
    else {
        iso_v = $( iso_selector ).val();
    }
    return iso_v;
}
function filter_table( arr ){
    // filter the array by the filt_val and date_val dictionaries
    var a = [], bool, bool_all, x, n, v, col, date_from, date_to;
    var filtered_arr = jQuery.grep( arr, function( a, i ){
        bool_all = true;
        for ( n in filt_val ) {
            v = filt_val[n];
            switch ( n ) {
                case 'date_joined_all':
                    col = 5;
                    break;
                case 'is_recognized':
                    col = 6;
                    break;
                case 'is_active':
                    col = 7;
                    break;
                case 'has_members':
                    col = 8;
                    break;
                default:
                    break;
            }
            x = a[col];     // rename comparison field for simplisity
            switch ( v ) {
                case 'all':
                    bool = true;
                    break;
                case 'yes':
                    bool = ( x === true );
                    break;
                case 'no':
                    if ( col == 5 ) {
                        x = x.slice( 0, 10 );
                        if ( !date_joined_from || date_joined_from === '' ) { date_from = ""; }
						else 												{ date_from = date_joined_from; }
                        if ( !date_joined_to || date_joined_to === '' ) 	{ date_to   = "99999999"; }
						else 												{ date_to   = date_joined_to; }
                        bool = ( date_from <= x && x <= date_to );
                    }
                    else {
                        bool = ( x === false );
                    }
                    break;
                case 'none':
                    bool = ( x === null || x === undefined );
                    break;
                default:
            }
            bool_all = ( bool_all && bool );
        }
        return bool_all;
    });
    return filtered_arr;
}
function appendDateFields() {
    $.datepicker.setDefaults({
        altFormat:          "yy-mm-dd",
        buttonImageOnly:    true,
        buttonImage:        "/static/admin/img/icon_calendar.gif",
		dateFormat:			"dd.mm.yy",
		gotoCurrent: 		true,
        numberOfMonths:     1,
        regional:           "uk",
        selectOtherMonths:  true,
        showOn:             "button",
        showOtherMonths:    true
    });
    $( "#date_joined_from" ).datepicker({
        altField: 	 '#iso_date_joined_from', 
        defaultDate: "-1w"
    });
    $( "#date_joined_to" ).datepicker({
        altField: 	 '#iso_date_joined_to', 
        defaultDate: ""
    });
}
function appendDateFieldsListeners(){
    $( "#date_joined_from" ).off( "change" ).on( "change", dateFieldListener );
    $( "#date_joined_to" ).off( "change" ).on( "change", dateFieldListener );
}
function dateFieldListener( ){
	var dstr 		= $( this ).val();
	var dateFormat 	= $( this ).datepicker( "option", "dateFormat" );
	var altField 	= $( this ).datepicker( "option", "altField" );
	var parsedDate;
	try {
		parsedDate = $.datepicker.parseDate( dateFormat, dstr );
		$( this ).removeClass( "error" ); 
	}
	catch( err ){
		$( altField ).val( "" ); 
		$( this ).addClass( "error" ); 
	}
}
function clearDateFields(){
    $( ".date-input input" ).val('');
}
// TODO-bug: iso_field remains empty after entering correct date in date field => filters don`t apply 
function filter_handler(){
    var $checkbox = $( '#id_apply_filters' );	
    var bool = $checkbox.prop('checked' );
console.log('filter_handler:', 'bool=', bool);
	if ( bool ) { applyFilter(); }
	else 		{ cancelFilter(); }
}



/**********************************************************************
 * END of the code covered by tests
 **********************************************************************/

 