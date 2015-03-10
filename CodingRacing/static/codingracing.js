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
        editor.setOption('readOnly', true);
        $('.finish-button-container').hide();
        $('.game-results #distance').html(data.distance);
        $('.game-results').show();
    }, 'json');
}

var game_diff_position = {row: 0, column: 0};
var game_language = '';
function send_editor_content_timer(game_id, editor)
{
    return setInterval(function(){
        var full_text = editor.getSession().doc.$lines.join('\n');
        $.post('/training/' + game_id + '/update', {'text' : full_text}, function(data){
            game_diff_position = data.diff_position;
        }, 'json')
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

    $.getJSON('/training/start?lang=' + game_language + '&timestamp=' + timestamp(), function(game){
        var $countdown = $('#countdown');
        var $code_image = $('.code-image');
        $code_image.find('> img').hide();
        $('.finish-button-container a').attr('disabled', true);
        $countdown.countdown(GAME_DELAY, function(){
            $code_image.find('> img').attr('src', game.image);
            $code_image.find('> img').show();
            editor.setOptions({readOnly: false});
            editor.selectAll();
            editor.remove();
            game_diff_position = 0;
            editor.focus();

            var timer = send_editor_content_timer(game.id, editor)
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

function set_cursor_to_diff_position(editor)
{
    editor.moveCursorToPosition(game_diff_position);

    editor.clearSelection();
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
    ace_editor.commands.addCommand({
        name: 'findDiffPosition',
        bindKey: {win: 'Ctrl-Q', mac: 'Command-Q'},
        exec: function(){
            set_cursor_to_diff_position(ace_editor)
        }
    });

    $('.start-game-container a.btn').click(function(){
        game_language = $('select[name=language]').val();
        if (game_language == 'none')
            return false;

        $('.select-language').hide();
        $('.game').show();
        start_game(ace_editor);
    });

    $('.game-results a.btn').click(function(){
        $('.finish-button-container').show();
        $('.game-results').hide();
        start_game(ace_editor);
    });
});
