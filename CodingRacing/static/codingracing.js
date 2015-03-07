function timestamp()
{
    if (!Date.now)
        Date.now = function() { return new Date().getTime(); }
    return Math.floor(Date.now() / 1000);
}

(function( $ ) {
    $.fn.countdown = function (seconds, callback) {
        var self = this;
        self.show();
        self.html('<img src="/static/countdown.gif"><div class="seconds"></div>');
        var $seconds_div = self.find('div');
        $seconds_div.html(seconds);
        var start_time = timestamp();
        var timer = setInterval(function () {
            var diff = timestamp() - start_time;
            $seconds_div.html(seconds - diff);
            if (seconds - diff == 0) {
                clearTimeout(timer);
                self.hide();
                callback(self);
            }
        }, 100);
        // for debug purpose
        //clearTimeout(timer)

        return self;
    }
})( jQuery );

var GAME_DELAY = 3; // seconds
var LOAD_IMG_AFTER = 1; // seconds
var UPDATE_LAST_TEXT_INTERVAL = 1; // seconds

function send_finish_command(game_id, editor)
{
    var full_text = editor.getSession().doc.$lines.join('\n');
    $.post('/training/' + game_id + '/finish', {'text' : full_text, 'timestamp' : timestamp()}, function(data) {
        console.log(data);
    }, 'json');
}

function send_editor_content_timer(game_id, editor)
{
    return setInterval(function(){
        var full_text = editor.getSession().doc.$lines.join('\n');
        $.post('/training/' + game_id + '/update', {'text' : full_text})
    }, UPDATE_LAST_TEXT_INTERVAL * 1000)
}

function activate_finish_game_button(game_id, editor, callback)
{
    $('.finish-button-container a').attr('disabled', false);
    var finish_game = function(){
        $('.finish-button-container a').attr('disabled', true);
        editor.commands.removeCommand('sendFinishCommand')
        send_finish_command(game_id, editor);
        callback();
    }
    $('.finish-button-container a').click(finish_game);
    editor.commands.addCommand({
        name: 'sendFinishCommand',
        bindKey: {win: 'Ctrl-Enter', mac: 'Command-Enter'},
        exec: finish_game
    });
}

function start_game(editor)
{
    editor.setOptions({readOnly: true});

    $.getJSON('/training/start?lang=csharp&timestamp=' + timestamp(), function(game){
        var $countdown = $('#countdown');
        $('.finish-button-container a').attr('disabled', true);
        $countdown.countdown(GAME_DELAY, function(){
            var $code_image = $('.code-image');
            $code_image.find('> img').attr('src', game.image);
            editor.setOptions({readOnly: false});
            editor.selectAll();
            editor.remove();
            editor.focus();

            timer = send_editor_content_timer(game.id, editor)
            activate_finish_game_button(game.id, editor, function(){
                clearInterval(timer);
            });
        });
        setTimeout(function(){
            var img = new Image();
            img.src = game.image;
        }, LOAD_IMG_AFTER * 1000);
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

    start_game(ace_editor);
});
