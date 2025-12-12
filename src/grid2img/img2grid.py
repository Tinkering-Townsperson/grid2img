from grid2img import __version__, Grid
import argparse
from pathlib import Path


def img2grid():
	print(f"grid2img v{__version__}")
	parser = argparse.ArgumentParser(description="Convert an image file into a grid text file.")
	parser.add_argument("input", type=str, help="Path to the input image file.")
	parser.add_argument("output", type=str, help="Path to save the output grid text file.", nargs="?", default=None)
	parser.add_argument("--max_size", type=int, nargs="?", default=128, help="Maximum width/height of the image when converting to grid. Default is 128.")  # noqa

	args = parser.parse_args()

	if not args.output:
		args.output = Path(args.input).with_suffix(".grid")

	try:
		Grid.from_img(args.input, grid_path=args.output, max_size=(args.max_size, args.max_size))
	except Exception as e:
		print(f"An error occurred: {e}")
	else:
		print(f"Image successfully saved to {args.output}")
	finally:
		input("Press Enter to exit...")


if __name__ == "__main__":
	img2grid()
