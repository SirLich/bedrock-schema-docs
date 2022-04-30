from textwrap import indent
import tag_builder as tb
import json
import pprint

DEFINITIONS = {}

def smart_get(data, key, definitions, default=None):
	"""
	Returns the value of a key in a dictionary, or a default value if the key does not exist.
	"""

	result = data.get('properties', {}).get(key, {})

	if "$ref" in result.keys():
		result = definitions.get(result.get('$ref').split('/')[-1], {})

	return result

def resolve_ref(schema, definitions):
	if isinstance(schema, dict) and "$ref" in schema.keys():
		schema = definitions.get(schema.get("$ref").split("/")[-1], {})
	return schema

def type_convert(type):
	type_map = {
		"number": "float"
	}

	return type_map.get(type, type)

def fetch_compound_types(schema):
	"""
	Returns a list of compound types in a schema
	"""

	compound_types = []

	for option in schema.get("oneOf"):
		compound_types.append(option.get("type", "unknown"))

	return compound_types


def gen_recursive(parent: tb.TagBuilder, property_name: str, schema: dict, indent: int, inside_array, definitions : dict) -> tb.TagBuilder:
	"""
	Recursive method to generate html based on a json schema.
	"""
	try:
		schema = resolve_ref(schema, definitions)
		type = type_convert(schema.get('type', "unknown"))

		description = schema.get('description', 'Unknown Description')

		tag = parent.insert_tag('div', style=f"indent indent-{indent}")


		# comments
		# tag.append_tag("br", collapse=True)
		tag.append_tag("div", f"# {description}", style="token comment")

		# Compound types
		if schema.get("oneOf"):
			compound_types = fetch_compound_types(schema)
			
			tag.append_tag("span", f'"{property_name}"', style='token property')
			tag.append_tag("span", ":", style="token operator")

			button_group = tag.insert_tag("span", style="button-group")

			for i, compound_type in enumerate(compound_types):
				if i == 0:
					bonus_class = "left"
				elif i == len(compound_types) - 1:
					bonus_class = "right"

				(
					button_group.insert_tag("button", f'{compound_type}', style=f"token {compound_type} button {bonus_class}")
						.decorate("type", "button")
						.decorate("onClick", f"alert('{bonus_class}')")
				)

			for option in schema.get("oneOf"):
				gen_recursive(tag, property_name, option, indent + 1, True, definitions)
			
			return tag

		# Simple Types, which are not compound
		if type != 'object' and type != 'array':
			if not inside_array:
				tag.append_tag("span", f'"{property_name}"', style='token property')
				tag.append_tag("span", ":", style="token operator")
			tag.append_tag("span", f'{type}', style=f"token {type}")
		
		# Object Types
		if type == 'object':
			
			if not inside_array:
				tag.append_tag("span", f'"{property_name}"', style='token property')
				tag.append_tag("span", ":", style="token operator")
			
			tag.append_tag("span", f'{type}', style=f"token {type}")
			tag.insert_tag("div", '{', style='token punctuation')

			# The generated child properties
			for property_name, value in schema.get('properties', {}).items():
				gen_recursive(tag, property_name, value, indent + 1, False, definitions)

			# The final part
			tag.append_tag("span", '}', style='token punctuation')

		# Array Types
		if type == 'array':
			(
				tag.append_tag("span", f'"{property_name}"', style='token property')
				.append_tag("span", ":", style="token operator")
				.append_tag("span", f'{type}', style=f"token {type}")
				.insert_tag("div", '[', style='token punctuation')
			)
			
			# The generated child properties
			gen_recursive(tag, property_name, schema.get('items', {}), indent + 1, True, definitions)
			
			# The final part
			tag.append_tag("span", ']', style='token punctuation')

		return tag
	except Exception:
		return tag

def generate_html(data, definitions):
	"""
	Expects a dictionary containing component names and schema data
	"""

	print(json.dumps(data, indent=2))
	components = tb.TagBuilder("div").decorate("class", "components")

	for component_name, schema in data.get('properties').items():
		component = components.insert_tag("div", style="component")
		code = component.insert_tag("code", style="code")
		gen_recursive(code, component_name, schema, 0, False, definitions)

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
				.parent
			.parent
			.insert_tag("body")
				.insert(components)
		.generate()
	)

	return tag

def main():
	with open('schema.json') as f:
		schema = json.load(f)

	definitions = schema.get('definitions')

	data = smart_get(schema, 'minecraft:entity', definitions)
	data = smart_get(data, 'components', definitions)
		
	html = generate_html(data, definitions)

	with open('index.html', 'w') as f:
		f.write('<!DOCTYPE html>')
		f.write(html)


if __name__ == "__main__":
	main()