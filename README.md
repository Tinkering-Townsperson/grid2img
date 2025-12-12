# grid2img

Revival and refactorization of my 2021 project "[Grid](https://github.com/Tinkering-Townsperson/Grid)". Converts a text file to a bitmap pixel art image.

## Installation

### Windows

On windows, you don't need to build `grid2img` since there is a prebuilt exe file in `./dist`.

```powershell
git clone https://github.com/Tinkering-Townsperson/grid2img.git
cd .\grid2img\dist
```

### Mac/Linux

On Mac OS/Linux, it's easiest to use `pipx` to install `grid2img`

```bash
git clone https://github.com/Tinkering-Townsperson/grid2img.git
cd ./grid2img/
pipx install .
```

## Usage

```bash
grid2img ./example.grid
```

## Example files

### Source

```grid
!GRIDFILE110

CM:
#=00EEFF
.=556677

---
.........................
.#####.####..#####.####..
.#.....#...#...#...#...#.
.#.....#...#...#...#...#.
.#.....####....#...#...#.
.#...#.#.#.....#...#...#.
.#...#.#..#....#...#...#.
.#####.#...#.#####.####..
.........................
.#####.#####.............
...#...#.................
...#...#.................
...#...#####.............
...#.......#.............
...#.......#.............
.#####.#####.............
.........................
.#####.#####.#####.#.....
.#.....#...#.#...#.#.....
.#.....#...#.#...#.#.....
.#.....#...#.#...#.#.....
.#.....#...#.#...#.#.....
.#.....#...#.#...#.#.....
.#####.#####.#####.#####.
.........................
```

### Render

![Exported grid file](./examples/example.png)
