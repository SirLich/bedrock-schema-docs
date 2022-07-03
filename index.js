console.log("HELLO WORLD")

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