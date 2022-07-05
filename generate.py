from textwrap import indent
import tag_builder as tb
import json
import hashlib, base64

def tiny_hash(value):
	return hashlib.md5(bytes(value)).digest(); d=base64.b64encode(d); 

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
		compound_types.append(type_convert(option.get("type", "unknown")))

	return compound_types


def gen_recursive(parent: tb.TagBuilder, property_name: str, schema: dict, indent: int, inside_array, definitions : dict, classes, full_path) -> tb.TagBuilder:
	"""
	Recursive method to generate html based on a json schema.
	"""
	try:
		schema = resolve_ref(schema, definitions)
		type = type_convert(schema.get('type', "unknown"))

		description = schema.get('description', 'Unknown Description')

		tag = parent.insert_tag('div', style=f"indent indent-{indent} {' '.join(classes)} {full_path}")


		# comments
		tag.append_tag("div", f"# {description}", style="token comment")

		# Compound types
		if schema.get("oneOf"):
			compound_types = fetch_compound_types(schema)
			
			tag.append_tag("span", f'"{property_name}"', style='token property')
			tag.append_tag("span", ":", style="token operator")

			button_group = tag.insert_tag("span", f"[{', '.join(compound_types)}]", style="token type italic")

			# for i, compound_type in enumerate(compound_types):
			# 	button_group.insert_tag("span", f'{compound_type}', style=f"token {compound_type} italic")
			# 	button_group.insert_tag("span", ", ", style=f"token comment italic")

			for option in schema.get("oneOf"):
				gen_recursive(tag, property_name, option, indent + 1, True, definitions, ["compound"], full_path)
			
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
			else:
				tag.append_tag("span", f'{type}', style=f"token {type}")

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
		if type == 'array':
			if not inside_array:
				tag.append_tag("span", f'"{property_name}"', style='token property')
				tag.append_tag("span", ":", style="token operator")
			else:
				tag.append_tag("span", f'{type}', style=f"token {type}")

			tag.append_tag("span", '[', style='token punctuation open-block')
			
			tag.append_tag("span", '...', style='token comment invisible extender')
			
			# The generated child properties
			inner_tag =tb.TagBuilder("div", style="block")
			gen_recursive(inner_tag, property_name, schema.get('items', {}), indent + 1, True, definitions, ["array"], full_path)
			tag.insert(inner_tag)

			# The final part
			tag.append_tag("span", ']', style='token punctuation close-block')

		return tag
	except Exception:
		return parent.insert_tag("div", f"unknown", style="token unknown indent")

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

	definitions = schema.get('definitions')
	data = smart_get(schema, 'minecraft:entity', definitions)
	data = smart_get(data, 'components', definitions)
	html = generate_html(data, definitions)

	with open('index.html', 'w') as f:
		f.write(html)


if __name__ == "__main__":
	main()