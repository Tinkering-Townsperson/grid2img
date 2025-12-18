# grid2img

Revival and refactorization of my 2021 project "[Grid](https://github.com/Tinkering-Townsperson/Grid)". Converts a text file to a bitmap pixel art image.

<div align="center">
  <a href="https://moonshot.hackclub.com" target="_blank">
    <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/35ad2be8c916670f3e1ac63c1df04d76a4b337d1_moonshot.png"
         alt="This project is part of Moonshot, a 4-day hackathon in Florida visiting Kennedy Space Center and Universal Studios!"
         style="width: 100%;">
  </a>
</div>

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
