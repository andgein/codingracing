function start_game()
{
    $.getJSON('/training/start?lang=csharp', function(data){
       console.log(data)
    });
}

$(document).ready(function(){
    var countdown = $('#countdown');

    ace.require('ace/ext/language_tools');
    var ace_editor = ace.edit('editor');
    ace_editor.setTheme('ace/theme/xcode');
    ace_editor.getSession().setMode('ace/mode/csharp');
    ace_editor.setOptions({
        enableBasicAutocompletion: true,
        enableSnippets: true,
        enableLiveAutocompletion: false
    });

    start_game();
});
