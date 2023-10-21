# Developing Bedrock Schema Docs

This page explains how to edit this git repository. For instructions on using the website, refer to the readme.

## Code Structure

This website is essentially a custom SSG.Not the easiest to work with, but I felt I needed the flexibility to 

## Sourcing Schemas

Currently the schema located in `schemas/schema.json` is sourced manually from Blockception. I don't know why I don't use a submodule and make this automatic, but I don't. If you 
want to update the schema, you should grab the file from [here](https://raw.githubusercontent.com/Blockception/Minecraft-bedrock-json-schemas/main/behavior/entities/entities.json).

## Building and Testing
 - Update 'Last updated' manually in `base.html`
 - Run `python generate.py` to create the website.
 - Open `index.html`

