__version__ = "1.1.0"

from os import PathLike
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw


class ColourMap:
	def __init__(self):
		self.map: dict[str, tuple[int]] = {"#": (255, 255, 255), ".": (0, 0, 0)}

	def populate(self, colour_dict: dict[str, tuple[int]]) -> "ColourMap":
		self.map = colour_dict
		return self

	def add_colour(self, symbol: str, colour: tuple[int]) -> "ColourMap":
		self.map[symbol] = colour
		return self

	def get_colour(self, symbol: str) -> tuple[int]:
		return self.map.get(symbol, (255, 255, 255))  # Default to white if not found

	@property
	def symbols(self) -> tuple:
		return tuple(self.map.keys())


class Grid:
	EXPECTED_FORMAT = "!GRIDFILE" + "".join(__version__.split("."))

	def __init__(self, path: PathLike, colourmap: Optional[ColourMap] = None):
		self.path = Path(path).resolve()
		self.colourmap = colourmap if isinstance(colourmap, ColourMap) else ColourMap()
		self.scale = 100

		self.img = None
		self.draw = None
		self.file = None

		self.grid_data = []
		self.width, self.height = 0, 0

	@classmethod
	def from_img(cls, img_path: PathLike, grid_path: Optional[PathLike] = None) -> "Grid":
		if not grid_path:
			grid_path = Path(img_path).with_suffix(".grid").resolve()
		# Placeholder for future implementation
		raise NotImplementedError("from_img method is not yet implemented.")

	def __repr__(self):
		if not all((self.width, self.height)):
			return f"<Unparsed Grid(path='{self.path}')>"

		return f"<Parsed Grid(path='{self.path}', dimensions={self.width}x{self.height})>"

	def parse(self):
		self.file = self.path.open("r")
		data = self.file.read()

		# Isolate metadata and grid data
		self.metadata, grid = data.split("---")

		# Process/validate metadata
		header_line = self.metadata.strip().splitlines()[0]

		if header_line == self.EXPECTED_FORMAT:
			print("Current version, proceeding with parsing...")
		elif header_line[0:-1] == self.EXPECTED_FORMAT[0:-1]:
			print("Patch version mismatch, proceeding with parsing...")
		elif header_line[0:-2] == self.EXPECTED_FORMAT[0:-2]:
			print("Minor version mismatch, proceeding with parsing...")
		elif header_line[0:-3] == self.EXPECTED_FORMAT[0:-3]:
			raise ValueError("Major version mismatch, aborting...")
		else:
			raise ValueError("Unrecognized file format, aborting...")

		# TODO: Expand metadata processing (e.g., colormap definitions)

		if "\nSCALE=" in self.metadata:
			scale_line = [line for line in self.metadata.splitlines() if line.startswith("SCALE=")][0]
			self.scale = int(scale_line.split("SCALE=")[1].strip())
			print(f"Set scale to {self.scale}")

		if "\nCM:\n" in self.metadata:
			cm_section = self.metadata.split("\nCM:\n")[1]
			for line in cm_section.strip().splitlines():
				symbol, hexcode = line.split("=")
				rgbcolour = tuple(int(hexcode[i:i+2], 16) for i in (0, 2, 4))
				self.colourmap.add_colour(symbol, rgbcolour)
				print(f"Added colour mapping: '{symbol}' -> {rgbcolour}")

		self.grid_data = [line for line in grid.strip().splitlines() if line]
		self.width = len(self.grid_data[0])
		self.height = len(self.grid_data)

		self.file.close()

		return self

	def render(self):
		if not self.grid_data:
			raise ValueError("Grid data is empty. Please parse the grid first.")

		self.img = Image.new(mode="RGB", size=(self.width * self.scale, self.height * self.scale), color=(255, 255, 255))
		self.draw = ImageDraw.Draw(self.img)

		for y in range(self.height):
			for x in range(self.width):
				self.draw.rectangle((
					x * self.scale,
					y * self.scale,
					x * self.scale + self.scale,
					y * self.scale + self.scale
					), fill=self.colourmap.get_colour(self.grid_data[y][x]))

		return self

	def export(self, output_path: PathLike, quality: int = 95):
		self.img.save(output_path, quality=quality)
