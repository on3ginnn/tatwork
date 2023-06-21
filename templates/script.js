window.onload = function () {
    
    const profileDropdown = document.querySelector(".profile_dropdown");
    console.log(profileDropdown);

    profileDropdown.addEventListener('click', function (e) {
        console.log(e.target);
    });

}