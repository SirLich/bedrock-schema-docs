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
