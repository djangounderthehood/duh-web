function easter() {
    var speakers = document.getElementsByClassName('speaker');
    var borg = speakers[1];
    for (i=0; i<speakers.length; i++) {
        speakers[i].src = borg.src;
    }

    var attendees = document.getElementsByClassName('attendee');
    borg = document.querySelector("img[alt='Jannis Leidel']");
    for (i=0; i<attendees.length; i++) {
        attendees[i].src = borg.src;
    }
}
if (window.addEventListener) {
  var state = 0, keyseq = [38,38,40,40,37,39,37,39,66,65];
  window.addEventListener("keydown", function(e) {
    if (e.keyCode == keyseq[state]){
        state++;
    }
    else {
        state = 0;
    }
    if (state == keyseq.length) {
        easter();
    }
    }, true);
}

// Smooth scrolling for anchor links:

$(document).ready(function() {
    $('a[href*=#]').each(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname && this.hash.replace(/#/,'') ) {
            var $targetId = $(this.hash), $targetAnchor = $('[name=' + this.hash.slice(1) +']');
            var $target = $targetId.length ? $targetId : $targetAnchor.length ? $targetAnchor : false;
            if ($target) {
                var targetOffset = $target.offset().top - 50;

                $(this).click(function() {
                    $('html, body').animate({scrollTop: targetOffset}, 1000);
                    return false;
                });
            }
        }
    });
});

// countdown timers
$(function() {
    $('.countdown').each(function() {
        var countdownContainer = $('.countdown-container', this);
        var countdownPast = $('.countdown-past', this);
        var countdownFuture = $('.countdown-future', this);
        // XXX the countdown lib we're using doesn't handle timezones
        var finalDate = moment($(this).data('target')).toDate();

        countdownContainer.countdown(finalDate, function(event) {
            var countDownText = event.strftime('%-D days %-H h %M min %S sec');
            countdownContainer.text(countDownText);
        }).on('finish.countdown', function() {
            countdownPast.addClass('hidden');
            countdownFuture.removeClass('hidden');
        });
    });
});

$(function() {
    var emojiMode = false;
    function emojiModeOn() {
        emojiMode = true;
        $('[data-emoji-alt]').each(function() {
            $(this).attr('title', $(this).text()).text($(this).data('emoji-alt')).addClass('emoji-alt');
        });
    }
    function emojiModeOff() {
        emojiMode = false;
        $('.emoji-alt').each(function() {
            $(this).text($(this).attr('title')).removeAttr('title').removeClass('emoji-alt');
        });
    }
    $('.emojimode-toggler').click(
        function() {
            if(emojiMode){
                emojiModeOff();
                $(this).attr('title', 'Turn on emoji mode').text('😺');
            }
            else {
                emojiModeOn();
                $(this).attr('title', 'Turn off emoji mode').text('😿');
            }
        }
    );
});

$(function() {
    var currentDate = new Date();
    if((currentDate.getMinutes() == 42) && (currentDate.getSeconds() % 10 == 0)) {
        $('.emojimode-toggler').click();
    }
})
