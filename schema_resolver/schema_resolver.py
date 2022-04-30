from pprint import PrettyPrinter
import jsonref

def main():
	with open('schemas/schema.json', 'r') as f:
		data = jsonref.loads(f.read())

	with open('../schema.json', 'w+') as f:
		pp = PrettyPrinter(indent=4, stream=f)
		pp.pprint(data)
		

if __name__ == "__main__":
	main()