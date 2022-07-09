from textwrap import indent
import tag_builder as tb
import json
import traceback

def smart_get(data, key, definitions, default=None):
	"""
	Returns the value of a key in a dictionary, or a default value if the key does not exist.
	"""

	result = data.get('properties', {}).get(key, {})

	if "$ref" in result.keys():
		result = definitions.get(result.get('$ref').split('/')[-1], {})

	return result

def force_array(data):
	"""
	Returns a list of data, even if it is a single item.
	"""
	if isinstance(data, list):
		return data
	else:
		return [data]
		
def resolve_schema_references(schema, definitions):
	"""
	Resolves the references of a schema, at a single 'level'.
	"""
	if isinstance(schema, dict) and "$ref" in schema.keys():
		schema = definitions.get(schema.get("$ref").split("/")[-1], {})
	return schema

def type_convert(type):
	"""
	Converts a type to a more readable format.
	"""

	type_map = {
		"number": "float",
		None: "filter",
	}
	
	return type_map.get(type, type)

def fetch_compound_types(schema):
	"""
	Returns a list of compound types in a schema.
	This is a form of "look ahead", where we look at the next schema 
	to see what types we are dealing with.
	"""

	compound_types = []

	for option in schema.get("oneOf"):
		compound_types.append(type_convert(option.get("type")))

	return compound_types


def gen_recursive(parent: tb.TagBuilder, property_name: str, schema: dict, indent: int, inside_array, definitions : dict, classes, full_path) -> tb.TagBuilder:
	"""
	Recursive method to generate html based on a json schema.
	"""
	try:
		schema = resolve_schema_references(schema, definitions)

		# TODO: Handle this being an array
		data_type = type_convert(schema.get('type'))
		description = schema.get('description', 'Unknown Description')

		# The 'tag' is the head of the HTML object that we will fill.
		tag = parent.insert_tag('div', style=f"indent indent-{indent} {' '.join(classes)} {full_path}")

		# Comment
		tag.append_tag("div", f"# {description}", style="token comment")

		# Property 
		if not inside_array:
			tag.append_tag("span", f'"{property_name}"', style='token property')
			tag.append_tag("span", ":", style="token operator")
		else:
			tag.append_tag("span", f'{data_type}', style=f"token {data_type}")

		# Compound types
		if schema.get("oneOf"):
			# A preview of the compound types
			compound_types = fetch_compound_types(schema)

			first = True
			for compound_type in compound_types:
				if not first:
					tag.append_tag("span", "or", style="token comment")
				first = False
				tag.append_tag("span", f"{compound_type}", style=f"token {compound_type}")


			# Recurse into each compound type
			inner_tag = tb.TagBuilder("div", style="compound-block")
			for option in schema.get("oneOf"):
				gen_recursive(inner_tag, property_name, option, indent + 1, True, definitions, ["compound"], full_path)
			tag.insert(inner_tag)
			return tag

		# Simple Types, which are not compound
		if data_type != 'object' and data_type != 'array':
			if not inside_array:
				tag.append_tag("span", f'{data_type}', style=f"token {data_type}")
		
		# Object Types
		if data_type == 'object':

			tag.append_tag("span", '{', style='token punctuation open-block')
			tag.append_tag("span", '...', style='token comment invisible extender')

			# The generated child properties
			inner_tag =tb.TagBuilder("div", style="block")
			for property_name, value in schema.get('properties', {}).items():
				gen_recursive(inner_tag, property_name, value, indent + 1, False, definitions, ["object"], f"{full_path}.{property_name}")
			tag.insert(inner_tag)

			# The final part
			tag.append_tag("span", '}', style='token punctuation close-block')

		# Array Types
		if data_type == 'array':

			items = schema.get('items', [])

			tag.append_tag("span", '[', style='token punctuation open-block')
			tag.append_tag("span", '...', style='token comment invisible extender')
			
			# The generated child properties
			inner_tag =tb.TagBuilder("div", style="block")
			for item in force_array(items):
				gen_recursive(inner_tag, property_name, item, indent + 1, True, definitions, ["array"], full_path)
			tag.insert(inner_tag)

			# The final part
			tag.append_tag("span", ']', style='token punctuation close-block')

		return tag
	except Exception as e:
		print("Failed  on: ", property_name)
		print(e)
		print(traceback.format_exc())
		return parent.insert_tag("div", f"unknown: {e}", style="token unknown indent")

def generate_html(data, definitions):
	"""
	Expects a dictionary containing component names and schema data
	"""

	components = tb.TagBuilder("div").decorate("class", "site-content")

	for component_name, schema in data.get('properties').items():
		component = components.insert_tag("div", style=f"component {component_name}")
		code = component.insert_tag("code", style="code")
		gen_recursive(code, component_name, schema, 0, False, definitions, [], component_name)

	with open('base.html', 'r') as f:
		html = f.read()

	html = html.replace('<gen/>', components.generate())

	return html

def main():
	with open('schema.json') as f:
		schema = json.load(f)

	# TODO make this smart-get smarter.
	definitions = schema.get('definitions')
	data = smart_get(schema, 'minecraft:entity', definitions)
	data = smart_get(data, 'components', definitions)
	html = generate_html(data, definitions)

	with open('index.html', 'w') as f:
		f.write(html)


if __name__ == "__main__":
	main()