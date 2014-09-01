function easter() {
    var speakers = document.getElementsByClassName('speaker');
    var borg = speakers[1];
    for (i=0; i<speakers.length; i++) {
        speakers[i].src = borg.src;
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