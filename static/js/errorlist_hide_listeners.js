console.log('start loading errorlist_hide_listeners.js');

// document_ready_handler called from html:
// Hiding the error message in form after user press key | change select | click button 
// in field with error data.
function set_errorlist_hide_listeners(){
    $( 'input' ).off( 'keypress' ).on( 'keypress', hide_error );
    $( 'select' ).off( 'change' ).on( 'change', hide_error );
    $( 'input[type="file"]' ).off( 'click' ).on( 'click', hide_error );
}
function hide_error(){
	$( this ).siblings( '.errorlist' ).hide();
}

/*
function set_errorlist_hide_listeners(){
    $( 'input' ).off( 'keypress' ).on( 'keypress', function () {
        $( this ).siblings( '.errorlist' ).hide();
    });
    $( 'select' ).off( 'change' ).on( 'change', function () {
        $( this ).siblings( '.errorlist' ).hide();
    });
    $( 'input[type="file"]' ).off( 'click' ).on( 'click', function () {
        $( this ).siblings( '.errorlist' ).hide();
    });
}

*/
