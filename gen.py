import tag_builder as tb

def create_test_html():
	return (
		tb.TagBuilder("html")
		.insert_tag("head")
		.insert_tag("title", "WoW!")
		.generate()
	)

def main():
	test = create_test_html()
	with open('test.html', 'w') as f:
		f.write('<!DOCTYPE html>')
		f.write(test)


if __name__ == "__main__":
	main()