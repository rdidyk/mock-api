// get JSON
function getJson() {
    try {
        return JSON.parse($('#json-editor').val());
    } catch (ex) {
        alert('Wrong JSON Format: ' + ex);
    }
}

function prettifyEditorJson() {
    var ugly = document.querySelector('#json-editor').value;
    var obj = JSON.parse(ugly);
    var pretty = JSON.stringify(obj, undefined, 4);
    document.querySelector('#json-editor').value = pretty;
}

// initialize
if ( document.querySelector('#json-editor') !== null ) {
    prettifyEditorJson();
    var display = document.createElement('pre');
    display.id = 'json-display';
    var el = document.querySelector('#json-editor');
    el.parentNode.appendChild(display);
    var editor = new JsonEditor('#json-display', getJson());
}

// enable translate button
// $('#translate').on('click', function () {
//     editor.load(getJson());
// });

