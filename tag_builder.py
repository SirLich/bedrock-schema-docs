"""
This file is a mini library for building html based on a tag-based system.
"""

from __future__ import annotations
from typing import List

class TagBuilder():
	"""
	HTML Builder Class for generating HTML.
	"""
	def __init__(self, tag_name : str, data : str = "", *, parent : TagBuilder = None, collapse = False, style = "") -> None:
		self.parent = parent
		self.collapse = collapse
		self.data = data
		self.tag_name = tag_name
		self.children : List[TagBuilder] = []
		self.properties = {
			"class": style
		}

	def decorate(self, property_name : str, property_value : str):
		"""
		Adds a property to this tag.
		"""
		base = self.properties.get(property_name, "")

		self.properties[property_name] = f"{base} {property_value}"
		return self


	def insert_table(self, data : List[List[str]]) -> None:
		"""
		Inserts a table into this structure.
		"""
		table_builder = self.insert_tag("table")

		for row in data:
			row_builder = table_builder.insert_tag("tr")
			for cell in row:
				row_builder.insert_tag("td", str(cell))

		return table_builder

	def append(self, tag: TagBuilder) -> TagBuilder:
		"""
		Appends a new tag to this structure, returning the parent tag.
		"""
		tag.parent = self
		self.children.append(tag)
		return self

	def insert(self, tag: TagBuilder) -> TagBuilder:
		"""
		Inserts a new tag into this structure, returning the child tag.
		"""
		tag.parent = self
		self.children.append(tag)
		return tag

	def insert_tag(self, tag_name: str, data : str = "", *, collapse = False,  style = "") -> TagBuilder:
		"""
		Inserts a new tag into this structure, returning the child tag.
		"""
		child = TagBuilder(tag_name, data, parent=self, collapse=collapse, style=style)
		self.children.append(child)
		return child

	def image(self, src: str, alt: str = "") -> TagBuilder:
		"""
		Inserts an image into this structure.
		"""
		return self.insert_tag("img", f"", collapse=True).decorate("src", src).decorate("alt", alt)

		
	def append_tag(self, tag_name: str, data : str = "", *, collapse = False, style = "") -> TagBuilder:
		"""
		Appends a new tag to this structure, returning the parent tag.
		"""
		child = TagBuilder(tag_name, data, parent=self, collapse=collapse, style=style)
		self.children.append(child)
		return self

	def generate(self):
		"""
		Generates the HTML for this structure by walking up to the top parent
		then rendering.
		"""
		if self.parent != None:
			return self.parent.generate()
		else:
			return str(self)

	def prettify_properties(self) -> str:
		"""
		Returns a string of all properties for this tag.
		"""
		html = ""
		for key, value in self.properties.items():
			html += f"{key}=\"{value.strip()}\" "
		return html.strip()

	def __str__(self) -> str:
		"""
		Returns the HTML string for this tag, and all child tags recursively.
		"""
		end_line = "/" if self.collapse else ""

		html = f"<{self.tag_name} {self.prettify_properties()}{end_line}>\n"
		html += self.data
		for child in self.children:
			html += str(child)

		if not self.collapse:
			html += "</{}>".format(self.tag_name)

		return html

	def __repr__(self) -> str:
		return str(self)

