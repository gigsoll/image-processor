[![Static Badge](https://img.shields.io/badge/pip-gistqd-blue)](https://pypi.org/project/gistqd/)

`gistqd` is a simple python CLI tool created to apply retro color effects on images with custom palettes or without them. Currently the following transformations are possible:

- ordered dithering – styles image with grid to reduce number of colors to 8
- quantization – reduces number of colors

# Example results

![quatize](https://raw.githubusercontent.com/gigsoll/image-processor/refs/heads/main/images/kyiv_poster.jpg)
![dithering](https://raw.githubusercontent.com/gigsoll/image-processor/refs/heads/main/images/dragon_poster.jpg)

# Usage

## General use of the program

```sh
Usage: python -m cli [OPTIONS] IMAGEPATH COMMAND [ARGS]...

Options:
  -c, --config PATH  path to the config in the file system
  --help             Show this message and exit.

Commands:
  dither    dither image, reducing number of colors to 8 with pattern
  quantize  basically reduce number of colors according to a pallete or...
```

## Dithering options

```sh
Usage: python -m cli IMAGEPATH dither [OPTIONS]

  dither image, reducing number of colors to 8 with pattern

Options:
  -b, --basic              use dithering without color palette
  -p, --palette TEXT       name of the palette from palette folder
  -g, --grid-size INTEGER  size of the grid for dithering, avalible sizes are:
                           2, 4, 8
  --help                   Show this message and exit.
```

## Quantization options

```sh
Usage: python -m cli IMAGEPATH quantize [OPTIONS]

  basically reduce number of colors according to a pallete or number of colors

Options:
  -b, --basic             use automatic colors without color palette
  -p, --palette TEXT      name of the palette from palette folder
  -n, --n-colors INTEGER  number of colors in resulting image
  --help                  Show this message and exit.
```
