from __future__ import annotations
from typing import List
import json
import os

class TagBuilder():
	"""
	HTML Builder Class for generating HTML.
	"""
	def __init__(self, tag_name : str, data : str = "", *, parent : TagBuilder = None) -> None:
		self.parent = parent
		self.data = data
		self.tag_name = tag_name
		self.children : List[TagBuilder] = []

	def insert_tag(self, tag_name: str, data : str = "") -> TagBuilder:
		"""
		Inserts a new tag into this structure, returning the child tag.
		"""
		child = TagBuilder(tag_name, data, parent=self)
		self.children.append(child)
		return child

	def append_tag(self, tag_name: str, data : str = "") -> None:
		"""
		Appends a new tag to this structure, returning the parent tag.
		"""
		child = TagBuilder(tag_name, data, parent=self)
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

	def __str__(self) -> str:
		"""
		Returns the HTML string for this tag, and all child tags recursively.
		"""
		html = "<{}>\n\t".format(self.tag_name)
		html += self.data
		for child in self.children:
			html += str(child)

		html += "</{}>".format(self.tag_name)
		return html

	def __repr__(self) -> str:
		return str(self)

