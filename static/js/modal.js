// Get the modal
const modal = document.getElementById("modal");

// Get the button that opens the modal
const signInBtn = document.getElementById("signInBtn");
const registerBtn = document.getElementById("registerBtn");

// Get the <span> element that closes the modal
const closeBtn = document.getElementsByClassName("close")[0];

// When the user clicks the button, open the modal
signInBtn.onclick = function() {
  modal.style.display = "block";
}

registerBtn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
closeBtn.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
