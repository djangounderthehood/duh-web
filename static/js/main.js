function easter() {
    var speakers = document.getElementsByClassName('speaker');
    var borg = speakers[1];
    for (var i=0; i<speakers.length; i++) {
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
    var stroopwafelMode = false;
    function makeItRain() {
        stroopwafelMode = true;
        var img = (Math.random()>0.95)?window.glutenfree:window.stroopwafel;
        $(document).snowfall({
            flakeCount : 100,
            maxSpeed : 10,
            maxSize: 50,
            minSize: 10,
            image: img
        });
    }
    function makeItStop() {
        stroopwafelMode = false;
        $(document).snowfall('clear');
    }
    $('.stroopwafelify').click(
        function() {
            if(stroopwafelMode){
                makeItStop();
                $(this).attr('title', 'Turn on stroopwafel mode').text('🍯🍪🌧');
            }
            else {
                makeItRain();
                $(this).attr('title', 'Turn off stroopwafel mode').text('🍯🍪☂');
            }
        }
    );
});

$(function() {
    var currentDate = new Date();
    if((currentDate.getMinutes() == 42) && (currentDate.getSeconds() % 10 == 0)) {
        $('.emojimode-toggler').click();
    }
});

$(function() {
    var sparkles = [
        // Don't ask me how I got these numbers...
        {color: 'blue', x: 28, y: 248, size: 62},
        {color: 'green', x: 187, y: 210, size: 80},
        {color: 'yellow', x: 268, y: 300, size: 70},
        {color: 'blue', x: 410, y: 275, size: 80},
        {color: 'yellow', x: 575, y: 208, size: 45},
        {color: 'yellow', x: 636, y: 290, size: 60},
        {color: 'green', x: 761, y: 228, size: 34},
        {color: 'blue', x: 789, y: 124, size: 40},
    ]
    var header = $('header:visible');
    var images = {
        'blue': header.data('sparkle-blue'),
        'yellow': header.data('sparkle-yellow'),
        'green': header.data('sparkle-green')
    }
    for(var i=0; i<sparkles.length; i++) {
        var sparkle = sparkles[i];

        if (sparkle.x < header.width()) {
            var img = $('<div>').addClass('sparkle').addClass(sparkle.color);
            img.css('left', sparkle.x + 'px');
            img.height(sparkle.y)
            img.width(sparkle.size + 'px');
            img.appendTo(header);
            img.click(function(){$(this).remove(); checkSparkles();});
        }
    }
    header.addClass('jsified');
});

function checkSparkles() {
    if ($('header .sparkle').length == 0) {
        $('header').animate({height: 0}, {complete: function(){$('.stroopwafelify').click();}});
    }
}
