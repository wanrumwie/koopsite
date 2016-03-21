/*
Global:  QUnit (?), expect (?), qs_TR_arr, selElement, selRowIndex, set0_qs_TR_arr, set_name_to_selElement (?)
*/

/********************************************************************/

function set0_qs_TR_arr() {
    // helper function to fill qs_TR_arr by sample values:
    var i, j, ob, TR;
    var arr = [];   // 2D array - table
    for ( i = 0 ; i < 10 ; i++ ) {
        arr[i] = [];
        TR = "TR";
        ob = {};
        ob.TR     = TR;  // add DOM TR object to array as 0th column 
        ob.model  = "model";  
        ob.id     = "id";
        ob.name   = "name";
        arr[i][0] = ob;
        for ( j = 1 ; j <= 4; j++ ) {
            arr[i][j] = i * j;
        }
    }
    return arr;
}

/********************************************************************/

QUnit.test('self test: set sample values to qs_TR_arr', function ( assert ) {
    expect( 4 * 10 );
    var qs_TR_arr = set0_qs_TR_arr();
    var i, j;
    for ( i = 0 ; i < 10 ; i++ ) {
        for ( j = 1 ; j <= 4; j++ ) {
            assert.strictEqual( qs_TR_arr[i][j], i * j, 'row value');
        }
    }
});
QUnit.test('self test: set sample values to qs_TR_arr[i][0] objects', function ( assert ) {
    expect( 4 * 10 );
    var qs_TR_arr = set0_qs_TR_arr();
    var i;
    for ( i = 0 ; i < 10 ; i++ ) {
        assert.strictEqual( qs_TR_arr[i][0].TR,     "TR",    'object element');
        assert.strictEqual( qs_TR_arr[i][0].model,  "model", 'object element');
        assert.strictEqual( qs_TR_arr[i][0].id,     "id",    'object element');
        assert.strictEqual( qs_TR_arr[i][0].name,   "name",  'object element');
    }
});

var qs_TR_arr = set0_qs_TR_arr();
var selElement = {};
var selRowIndex;

QUnit.test('set_name_to_selElement', function ( assert ) {
    expect( 2 );
    selElement.name = "name";
    var newName = "newName";
    selRowIndex = 0;
    set_name_to_selElement( newName );
    assert.strictEqual( qs_TR_arr[selRowIndex][0].name, newName, 'qs_TR_arr[i][0].name');
    assert.strictEqual( selElement.name,  newName, 'selElement.name');
});


