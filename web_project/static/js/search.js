function search() {
    var input = document.getElementById("search1");
    var text = input.value.trim();

    if (text == "") {
        document.location.href = "/articles";
    } else {
        document.location.href = '/articles/find/' + encodeURIComponent(text);
    }
}
