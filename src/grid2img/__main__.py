from grid2img import __version__, Grid, ColourMap
from json import load
import argparse
from pathlib import Path


def main():
	print(f"grid2img v{__version__}")
	parser = argparse.ArgumentParser(description="Convert a grid text file into an image.")
	parser.add_argument("input", type=str, help="Path to the input grid text file.")
	parser.add_argument("output", type=str, help="Path to save the output image file.", nargs="?", default=None)
	parser.add_argument("colourmap", type=str, nargs="?", default=None, help="Optional path to a JSON file defining the colour map.")  # noqa

	args = parser.parse_args()

	if args.colourmap:
		with open(args.colourmap, "r") as cm_file:
			colour_dict = load(cm_file)
		colourmap = ColourMap().populate({k: tuple(v) for k, v in colour_dict.items()})
		grid = Grid(args.input, colourmap)
	else:
		grid = Grid(args.input)

	if not args.output:
		args.output = Path(args.input).with_suffix(".png")

	try:
		grid.parse().render().export(args.output)
	except Exception as e:
		print(f"An error occurred: {e}")
	else:
		print(f"Image successfully saved to {args.output}")
	finally:
		input("Press Enter to exit...")


if __name__ == "__main__":
	main()
