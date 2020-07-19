class PadmaDropdownMenu {
  constructor() {
    window.addEventListener("load", this.init.bind(this));
  }
  init() {
    this.element = document.getElementById("dropdown-menu");
    this.element.addEventListener("click",   (event) => { event.stopPropagation(); });
    document.addEventListener("click",       this.close.bind(this));
    document.addEventListener("contextmenu", this.open.bind(this));

    window.requestAnimationFrame(() => {
      this.element.classList.add("initialized");
    });
  }
  open(event) {
    if( !this.getSelectionText().length ){
      return;
    }
    event.preventDefault();
    this.setLinks();
    this.element.classList.add("visible");
    this.element.style.top = this.getVerticalOffset(event.pageY) + "px";
    this.element.style.left = event.pageX + 35 + "px";
  }
  close() {
    this.element.classList.remove("visible");
  }
  setLinks() {
    let text = this.getSelectionText();
    document.getElementById("dictionary_lookup").href = "/dictionary_lookup?query=" + text;
    document.getElementById("search_texts"     ).href = "/search_texts?query="      + text;
    document.getElementById("find_similar"     ).href = "/find_similar?query="      + text;
    document.getElementById("word_statistics"  ).href = "/word_statistics?query="   + text;
    document.getElementById("tokenize"         ).href = "/tokenize?query="          + text;
  }
  getSelectionText() {
    var text = "";
    if (window.getSelection) {
      text = window.getSelection().toString();
    } else if (document.selection && document.selection.type != "Control") {
      text = document.selection.createRange().text;
    }
    return text;
  }
  getVerticalOffset(offset) {
    let elementHeight = this.element.offsetHeight,
    viewPortHeight    = window.innerHeight,
    scrollTop         = window.scrollY,
    margin            = 5;

    offset = Math.min( offset, scrollTop + viewPortHeight - elementHeight - margin );
    offset = Math.max( offset, scrollTop + margin );

    return offset;
  }
}

new PadmaDropdownMenu();