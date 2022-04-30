import tag_builder as tb
import json

def gen_recursive(parent : tb.TagBuilder, key : str, schema : dict) -> tb.TagBuilder:
	"""
	Recursive method to generate html based on a json schema.
	"""

	type = schema.get('type', None)

	print(f"Handling: {key} - {type}")

	if type == 'boolean':
		return (
			parent.insert_tag("p", schema.get('description', 'Unknown Description'))
			.decorate("class", "property_description string_description")
			.image('icons/seeding.svg')
		)

	elif type == 'string':
		return (
			parent.insert_tag("p", schema.get('description', 'Unknown Description'))
			.decorate("class", "property_description string_description")
			.image('icons/book-2.svg')
		)

	elif type == 'object':
		tag = parent.insert_tag("details").decorate('class', 'property_container')
		tag.insert_tag("summary", key).decorate("class", "property_name")

		tag.insert_tag("p", schema.get('description', 'Unknown Description')).decorate("class", "property_description object_description")
		
		table = (
			tb.TagBuilder("table")
			.insert_tag("tr")
				.append_tag("th", "Name")
				.append_tag("th", "Type")
				.append_tag("th", "Description")
			.parent
		)

		for key, value in schema.get('properties', {}).items():
			description = tb.TagBuilder("td", value.get('description', 'Unknown Description'))

			gen_recursive(description, key, value)

			(table.insert_tag("tr")
				.append_tag("td", key)
				.append_tag("td", value.get('type', 'Unknown Type'))
				.append(description)
			)

			

		tag.append(table)

		return tag

def generate_html(data):
	"""
	Expects a dictionary containing component names and schema data
	"""

	components = tb.TagBuilder("div").decorate("class", "components")

	for component_name, schema in data.items():
		gen_recursive(components, component_name, schema)

	tag = (
		tb.TagBuilder("html")
			.insert_tag("head")
				.append_tag("title", "Component Test")
				.insert_tag("link", collapse=True)
					.decorate("rel", "stylesheet")
					.decorate("href", "index.css")
				.parent
				.insert_tag("link", collapse=True)
					.decorate("rel", "stylesheet")
					.decorate("href", "https://unpkg.com/@tabler/icons@latest/iconfont/tabler-icons.min.css")
				.parent
			.parent
			.insert_tag("body")
				.insert(components)
		.generate()
	)

	return tag

def main():
	with open('addrider.json') as f:
		data = json.load(f)
		
	html = generate_html(data)

	with open('index.html', 'w') as f:
		f.write('<!DOCTYPE html>')
		f.write(html)


if __name__ == "__main__":
	main()