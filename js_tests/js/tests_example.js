
QUnit.test( "keylogger api behavior", function( assert ) {
  var doc = $( document ),
    keys = new KeyLogger( doc );
console.log('keys=', keys, '---------------');

  // Trigger the key event
  doc.trigger( $.Event( "keydown", { keyCode: 9 } ) );
console.log('keys=', keys);

  // Verify expected behavior
  assert.deepEqual( keys.log, [ 9 ], "correct key was logged" );
});


QUnit.test( "keylogger api behavior2", function( assert ) {
  var doc = $( document ),
    keys = new KeyLogger( doc );
console.log('keys=', keys, '================');

  // Trigger the key event
  doc.trigger( $.Event( "keydown", { keyCode: 9 } ) );
console.log('keys=', keys);

  // Verify expected behavior
  assert.deepEqual( keys.log, [ 9 ], "correct key was logged" );
});
