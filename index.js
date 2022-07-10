const blocks = document.querySelectorAll(".open-block");
blocks.forEach((block) => {
  block.addEventListener("click", function handleClick(event) {
    block.nextSibling.classList.toggle("invisible");
    block.nextSibling.nextSibling.classList.toggle("hidden");
  });
});

const extenders = document.querySelectorAll(".extender");
extenders.forEach((block) => {
  block.addEventListener("click", function handleClick(event) {
    block.classList.toggle("invisible");
    block.nextSibling.classList.toggle("hidden");
  });
});

function collapseAll() {
  const blocks = document.querySelectorAll(".open-block");
  blocks.forEach((block) => {
	block.nextSibling.classList.toggle("invisible");
	block.nextSibling.nextSibling.classList.toggle("hidden");
  });
}

function filter() {
  var searchbar = document.getElementById("searchbar");

  var filter = searchbar.value.toUpperCase();

  var elements = document.querySelectorAll(".component");

  var filterCount = 0;

  elements.forEach((element) => {
    let searchTerm = element.className.toUpperCase();
    console.log(searchTerm);
    if (searchTerm.includes(filter)) {
      filterCount += 1;
      element.style.display = "block";
    } else {
      element.style.display = "none";
    }
  });

  var counter = document.getElementById("counter");
  counter.innerHTML = filterCount;
}

filter();


const copy_buttons = document.querySelectorAll(".copy-button");
copy_buttons.forEach((button) => {
  button.addEventListener("click", function handleClick(event) {
    navigator.clipboard.writeText(button.nextSibling.innerHTML);
  });
});

function myFunction() {
  /* Get the text field */
  var copyText = document.getElementById("myInput");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

   /* Copy the text inside the text field */
  navigator.clipboard.writeText(copyText.value);

  /* Alert the copied text */
  alert("Copied the text: " + copyText.value);
} 