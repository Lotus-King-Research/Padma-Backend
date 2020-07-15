function getSelectionText() {
    var text = "";
    if (window.getSelection) {
        text = window.getSelection().toString();
    } else if (document.selection && document.selection.type != "Control") {
        text = document.selection.createRange().text;
    }
    return text;
};

(function() {

document.addEventListener( "click", function(e) {
  var menu = document.getElementById("dropdown-menu");
  menu.style.display = "none";
});

"use strict";

document.addEventListener( "contextmenu", function(e) {
  var text = getSelectionText();

  if (text !== '') {

    var menu = document.getElementById("dropdown-menu");

    menu.addEventListener("click", function(e) {

    e.stopPropagation();
    });

    menu.style.display = "block";
    menu.style.top = e.pageY + 'px';
    menu.style.left = e.pageX + 35 + 'px';
    e.preventDefault();

    document.getElementById("dictionary_lookup").href="/dictionary_lookup?query=" + text;
    document.getElementById("search_texts").href="/search_texts?query=" + text;
    document.getElementById("similar_words").href="/similar_words?query=" + text;
    document.getElementById("word_statistics").href="/word_statistics?query=" + text;
    document.getElementById("tokenize").href="/tokenize?query=" + text;

  }
});

})();