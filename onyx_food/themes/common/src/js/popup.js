/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function popUp() {
    document.getElementById("popup-content").classList.toggle("show");
  }
  
  // Close the dropdown menu if the user clicks outside of it
  window.onclick = function(event) {
    console.log(document.getElementById("popup-content").classList);
    if (document.getElementById("popup-content").classList.contains('show')) {
      var dropdowns = document.getElementsByClassName("popup-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  } 