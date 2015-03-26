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
            if (seconds - diff <= 0) {
                clearTimeout(timer);
                self.hide();
                callback(self);
            }
        }, 100);
        // for debug purpose
        // clearTimeout(timer)

        return self;
    }

    $.fn.pressEnter = function(fn) {
        return this.each(function() {
            $(this).bind('enterPress', fn);
            $(this).keyup(function(e){
                if(e.keyCode == 13)
                {
                  $(this).trigger("enterPress");
                }
            })
        });
     };
})( jQuery );

$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    if (results == null)
       return null;
    else
       return results[1] || 0;
}

$.escapeHtml = function(text) {
  var map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };

  return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

var GAME_DELAY = 5; // seconds
var LOAD_IMG_AFTER = 2; // seconds
var UPDATE_LAST_TEXT_INTERVAL = 1; // seconds

function send_finish_command(game_type, game_id, editor)
{
    var full_text = editor.getSession().doc.$lines.join('\n');
    $.post('/' + game_type + '/' + game_id + '/finish', {'text' : full_text, 'timestamp' : timestamp()}, function(data) {
        editor.setOption('readOnly', true);

        $('.finish-button-container').hide();
        $('.howto').hide();
        $('.competitors').hide();

        $('.game-results #speed').html(data.speed);
        $('.game-results #seconds').html(data.seconds);
        $('.game-results #total_seconds').html(data.total_seconds);
        $('.game-results #distance').html(data.distance);
        $('.game-results').show();
        $('.return-to-main-button-container').show();
    }, 'json');
}

var game_diff_position = {row: 0, column: 0};
var game_language = '';
function send_editor_content_timer(game_type, game_id, editor)
{
    return setInterval(function(){
        var full_text = editor.getSession().doc.$lines.join('\n');
        $.post('/' + game_type + '/' + game_id + '/update', {'text' : full_text}, function(data){
            game_diff_position = data.diff_position;

            if (data.competitors)
            {
                $competitors = $('.competitors');
                if (! $competitors.is(':visible'))
                    $competitors.fadeIn();
                $competitors.html('');

                for (var c in data.competitors)
                {
                    $competitors.append('<div class="competitor"><div class="name"></div><div class="percents"><div class="bar"></div></div></div>')
                    var $competitor = $competitors.find('.competitor').last();
                    $competitor.find('.name').text(c);
                    $competitor.find('.bar').css('width', data.competitors[c] + '%', 'important');
                }
            }
        }, 'json')
    }, UPDATE_LAST_TEXT_INTERVAL * 1000)
}

function activate_finish_game_button(game_type, game_id, editor, callback)
{
    $('.finish-button-container a').attr('disabled', false);
    var finish_game = function(){
        $('.finish-button-container a').attr('disabled', true);
        editor.commands.removeCommand('sendFinishCommand')
        send_finish_command(game_type, game_id, editor);
        callback();
    }
    $('.finish-button-container a').click(finish_game);
    editor.commands.addCommand({
        name: 'sendFinishCommand',
        bindKey: {win: 'Ctrl-Enter', mac: 'Command-Enter'},
        exec: finish_game
    });
}

function start_training(editor)
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

            var timer = send_editor_content_timer('training', game.id, editor)
            activate_finish_game_button('training', game.id, editor, function(){
                clearInterval(timer);
            });
        });
        setTimeout(function(){
            var img = new Image();
            img.src = game.image;
        }, LOAD_IMG_AFTER * 1000);
    });
}

function start_contest(game_id, editor)
{
    editor.setOptions({readOnly: true});

    $.getJSON('/contest/' + game_id + '/check', function(game){
        var $countdown = $('#countdown');
        var $code_image = $('.code-image');
        var before_start = game.before_start;
        $code_image.find('> img').hide();
        $('.finish-button-container a').attr('disabled', true);
        $countdown.countdown(before_start, function(){
            $code_image.find('> img').attr('src', game.image);
            $code_image.find('> img').show();
            editor.setOptions({readOnly: false});
            editor.selectAll();
            editor.remove();
            game_diff_position = 0;
            editor.focus();

            var timer = send_editor_content_timer('contest', game_id, editor)
            activate_finish_game_button('contest', game_id, editor, function(){
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

    if (typeof ace != 'undefined' && $('#editor').length)
    {
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
            exec: function () {
                set_cursor_to_diff_position(ace_editor)
            }
        });

        $('.hotkeys-button').click(function(){
            ace.config.loadModule("ace/ext/keybinding_menu", function(module) {
                module.init(ace_editor);
                ace_editor.showKeyboardShortcuts()
            })
        });

        var results = new RegExp('contest/(\\d+)').exec(window.location.href);
        if (results)
        {
            var game_id = results[1];
            start_contest(game_id, ace_editor);
        }
    }

    game_language = $.urlParam('lang');
    /*
    if (game_language != null)
        start_training(ace_editor)
    */

    $('.i-understood').click(function(){
       $('.faq').modal('hide');
        start_training(ace_editor);
    });
    $('.select-language a.btn').click(function(){
        game_language = $(this).data('language');
        if (game_language == 'none')
            return false;

        window.location.href = '/training?lang=' + game_language;
    });

    $('.return-to-main-button-container a.btn').click(function(){
        $('.finish-button-container').show();
        $('.howto').show();
        $('.game-results').hide();
        $('.return-to-main-button-container').hide();
        start_training(ace_editor);
    });

    $('.enjoy-contest-button').click(function(){
        var password = $('input[name=password]').val();
        $.post('/contest/enjoy', {'password': password}, function(data){
            if ('error' in data)
            {
                $('.enjoy-contest-result').text(data['error']);
                return;
            }
            $('.enjoy-contest-result').text('Ожидаем остальных...');
            var game_id = data['id'];
            var timer = setInterval(function(){
                $.getJSON('/contest/' + game_id + '/check', function(data){
                    if ('error' in data)
                        return;
                    var state = data['state'];
                    if (state == 'running')
                    {
                        window.location.href = '/contest/' + game_id;
                        clearInterval(timer);
                    }
                });
            }, 1000);
        }, 'json')
    });

    $('.enter-password input[name=password]').pressEnter(function(){
        $(this).parent().find('a.btn').click();
    });

    $('.select-language-button').click(function(){
        $('.enter-password').hide();
        $('.select-language').fadeIn();
    });

    $('.enter-password-button').click(function(){
        $('.select-language').hide();
        $('.enter-password').fadeIn();
    });

    if ($('.faq').length)
        $('.faq').modal('show');

    var results = new RegExp('/manage/contest/(\\d+)').exec(window.location.href)
    if (results)
    {
        var game_id = results[1];
        setInterval(function() {
                manage_update_stat(game_id);
            }, 2000);
        /* And call it */
        manage_update_stat(game_id);

        $('.manage-start-game').click(function(){
            $.get('/manage/contest/' + game_id + '/start');
        });
    }

    if ($('[data-toggle="tooltip"]').length)
        $('[data-toggle="tooltip"]').tooltip();
});

function manage_update_stat(game_id)
{
    $.getJSON('/manage/contest/' + game_id + '/status', function(data){
        var $participants = $('.participants');
        var users = data.users;
        $participants.html('');

        if (data.state == 'not-started')
            $('.password').text('Пароль: ' + data.password)
        else {
            $participants.parent().removeClass('inactive');
            $('.password-content').hide();
        }

        var users_count = 0;
        for (var user_id in users)
            users_count += 1;

        if (users_count > 0)
            $participants.parent().show();

        for (var user_id in users)
        {
            if ($('#participant-' + user_id).length == 0){
                $participants.append('<div class="participant col-sm-' + (12 / users_count) + '" id="participant-' + user_id + '"><div class="info"><img src="" class="photo"><div class="name"></div></div><div class="code" id="code-' + user_id + '">&nbsp;</div><div class="speed"></div></div>');
            }
            var $participant = $('#participant-' + user_id);
            //var editor = ace.edit('code-' + user_id);
            //editor.setOption('readOnly', true);

            var name = users[user_id].full_name;
            var photo = users[user_id].photo_50;
            $participant.find('.name').text($.escapeHtml(name));
            $participant.find('.photo').attr('src', photo);

            if (user_id in data.last_texts) {
                //editor.setValue(data.last_texts[user_id], 1);
                $participant.find('.code').show().html($.escapeHtml(data.last_texts[user_id].text).replace(/\n/g, '<br>').replace(/ /g, '&nbsp;'));
                $participant.find('.speed').show().text(data.last_texts[user_id].speed);
            }
            else
            {
                $participant.find('.code').hide();
                $participant.find('.speed').hide();
            }

            if (user_id in data.scores)
            {
                $participant.find('.speed').addClass('finished');
                var speed_text = '<div class="details">' + data.scores[user_id].seconds + ' сек. + 5 &times; ' + data.scores[user_id].distance + ' = ' + data.scores[user_id].total_seconds + ' сек.</div>' + data.scores[user_id].speed;
                $participant.find('.speed').show().html(speed_text);
            }
        }

    });
}