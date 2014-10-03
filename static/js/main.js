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
