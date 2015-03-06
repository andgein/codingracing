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

function start_game(editor)
{
    editor.setOptions({readOnly: true});
    $.getJSON('/training/start?lang=csharp&timestamp=' + timestamp(), function(game){
        var $countdown = $('#countdown');
        $countdown.countdown(GAME_DELAY, function(){
            var $code_image = $('.code-image');
            $code_image.find('> img').attr('src', game.image);
            editor.setOptions({readOnly: false});
            editor.selectAll();
            editor.remove();
            editor.focus();
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
