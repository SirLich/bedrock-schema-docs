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

    // Ripple effect
    const circle = document.createElement("span");
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    console.log();
    console.log(event.clientX)
    circle.style.left = `${event.clientX - (button.getBoundingClientRect().x + radius)}px`;
    circle.style.top = `${event.clientY - (button.getBoundingClientRect().y + radius)}px`;
    circle.classList.add("ripple"); 

    const ripple = button.getElementsByClassName("ripple")[0];

    if (ripple) {
      ripple.remove();
    }

    button.appendChild(circle);
  });
});

