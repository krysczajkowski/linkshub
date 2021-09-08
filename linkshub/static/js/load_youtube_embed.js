function load_youtube_embed(url, div_id) {
    var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    var match = url.match(regExp);

    var id

    if (match && match[2].length == 11) {
        id = match[2];
    } else {
        id = 'error';
    }

    document.getElementById(div_id).innerHTML = '<iframe src="//www.youtube.com/embed/' + id + '" frameborder="0" allowfullscreen></iframe>'
}