function checkAndRedirect() {
    var inputName = document.getElementById("nameInput").value;
    var selectLang = document.getElementById("dropdown").value;

    var message = "Name : " + inputName + "\n Language : " + selectLang;

    if (inputName.trim() === "" && selectLang.trim() === "") {
        alert("\"Language\" and \"Name\" are empty.");
    } else if (inputName.trim() === "") {
        alert("\"Name\" is empty.");
    } else if (selectLang.trim() === "") {
        alert("\"Language\" is empty.");
    } else {
        // alert(message);
        window.location.href = "another_page.html?selectedOption=" + encodeURIComponent(selectLang) + "&textInputValue=" + encodeURIComponent(inputName);
    }
}