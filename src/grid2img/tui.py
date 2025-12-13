from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Button, DirectoryTree, Footer, Header, Label, TabbedContent, TabPane

from grid2img import __version__, Grid  # noqa
from enum import Enum


class Modes(Enum):
	GRID2IMG = 1
	IMG2GRID = 2


class FilePickerScreen(ModalScreen[Path | None]):
	"""Simple modal for picking a file from the filesystem."""

	def __init__(self, title: str, start_dir: Path | str | None = None) -> None:
		super().__init__()
		self._title = title
		self._start_dir = Path(start_dir or Path.cwd())

	def compose(self) -> ComposeResult:
		yield Vertical(
			Label(self._title, id="dialog-title"),
			DirectoryTree(str(self._start_dir), id="file-tree"),
			Button("Cancel", id="cancel", variant="error"),
		)

	def on_directory_tree_file_selected(
		self, event: DirectoryTree.FileSelected
	) -> None:
		event.stop()
		self.dismiss(Path(event.path))

	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "cancel":
			event.stop()
			self.dismiss(None)


class Grid2ImgApp(App):
	CSS_PATH = "grid2img.tcss"
	TITLE = "Grid2Img TUI"

	def __init__(self):
		super().__init__()
		self.selected_path: Optional[Path] = None
		self.mode = Modes.GRID2IMG

	def compose(self) -> ComposeResult:
		yield Header()
		yield Label("Grid2Img TUI Application", id="title")
		with TabbedContent("Grid2Img", "Img2Grid"):
			with TabPane("Grid2Img"):
				yield Horizontal(
					Button("Load Grid", id="load-grid", variant="primary"),
					Button("Render Image", id="render-image", variant="success"),
				)
				yield Label("", id="status-bar")

			with TabPane("Img2Grid"):
				yield Horizontal(
					Button("Load Image", id="load-image", variant="primary"),
					Button("Convert to Grid", id="convert-grid", variant="success"),
				)
				yield Label("", id="status-bar")

		yield Footer()

	def on_button_pressed(self, event: Button.Pressed) -> None:
		# self.notify(f"Button pressed: {event.button.id}", severity="information")
		if event.button.id == "load-grid":
			self._open_file_picker("grid")
			self.mode = Modes.GRID2IMG
		elif event.button.id == "render-image":
			grid = Grid(self.selected_path) if self.selected_path and self.mode == Modes.GRID2IMG else None
			if grid:
				output_path = self.selected_path.with_suffix(".png")
				grid.parse().render().export(output_path)
				self.notify(f"Image rendered to: {output_path}", severity="success")
				return
			else:
				self.notify("No grid file selected", severity="warning")
		elif event.button.id == "load-image":
			self._open_file_picker("image")
			self.mode = Modes.IMG2GRID
		elif event.button.id == "convert-grid":
			output_path = self.selected_path.with_suffix(".grid") if self.selected_path and self.mode == Modes.IMG2GRID else None
			if output_path:
				grid = Grid.from_img(self.selected_path, output_path)
				self.notify(f"Grid created at: {output_path}", severity="success")
			else:
				self.notify("No image file selected", severity="warning")

	def _open_file_picker(self, picker_type: str) -> None:
		"""Open a modal file picker for grids or images."""
		title = "Select Grid File" if picker_type == "grid" else "Select Image File"
		screen = FilePickerScreen(title, start_dir=Path("/").resolve())
		if picker_type == "grid":
			self.push_screen(screen, self._handle_grid_file)
		else:
			self.push_screen(screen, self._handle_image_file)

	def _handle_grid_file(self, path: Path | None) -> None:
		path = Path(path).resolve()
		if path is None or not path.exists():
			self.notify("Grid selection cancelled", severity="warning")
			return
		if path.suffix.lower() != ".grid":
			self.notify("Please select a .grid file", severity="warning")
			return
		self.notify(f"Selected grid: {path}", severity="information")
		self.selected_path = path

	def _handle_image_file(self, path: Path | None) -> None:
		if path is None:
			self.notify("Image selection cancelled", severity="warning")
			return
		allowed = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
		if path.suffix.lower() not in allowed:
			self.notify("Please select an image file (png/jpg/jpeg/bmp/gif)", severity="warning")
			return
		self.notify(f"Selected image: {path}", severity="information")


if __name__ == "__main__":
	app = Grid2ImgApp()
	app.run()
