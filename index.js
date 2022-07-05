const blocks = document.querySelectorAll('.open-block');
blocks.forEach(block => {
	block.addEventListener('click', function handleClick(event) {
		block.nextSibling.classList.toggle('invisible');
		block.nextSibling.nextSibling.classList.toggle('hidden');
	});
});

const extenders = document.querySelectorAll('.extender');
extenders.forEach(block => {
	block.addEventListener('click', function handleClick(event) {
		block.classList.toggle('invisible');
		block.nextSibling.classList.toggle('hidden');
	});
});


function filter() {

	var searchbar = document.getElementById('searchbar');

	var filter = searchbar.value.toUpperCase();
	
	var elements = document.querySelectorAll('.component');
	
	elements.forEach(element => {
		let searchTerm = element.className.toUpperCase();
		console.log(searchTerm)
		if (searchTerm.includes(filter)) {
			element.style.display = 'block';
		}
		else 
		{
			element.style.display = 'none';
		}
	});

	for (i = 0; i < li.length; i++) {
	  a = li[i].getElementsByTagName("a")[0];
	  txtValue = a.textContent || a.innerText;
	  if (txtValue.toUpperCase().indexOf(filter) > -1) {
		li[i].style.display = "";
	  } else {
		li[i].style.display = "none";
	  }
	}
  }