import sys
import click

from backend.models.image_pipeline import ImagePipeline


@click.command()
@click.argument("input", nargs=1, type=click.Path(file_okay=True))
@click.argument("output", nargs=1, type=click.Path(file_okay=True, dir_okay=True))
@click.option(
    "--quantize-palette",
    type=click.Path(file_okay=True),
    multiple=True,
    help="path to palette to quantize",
)
@click.option(
    "--dither-basic",
    multiple=True,
    help="dither image to use basic 8 colors with specific table size,"
    " can be 2, 4, or 8",
    type=int,
)
@click.option(
    "--denoice",
    multiple=True,
    help="remove noice from image",
    is_flag=True,
)
def cli(
    input: str,
    output: str,
    quantize_palette: tuple[str, ...],
    dither_basic: tuple[str, ...],
    denoice: tuple[bool, ...],
):
    arg_order = _parse_arvg()
    arg_used = dict.fromkeys(arg_order, 0)
    pipe = ImagePipeline(input)
    for arg in arg_order:
        arg_count = arg_used[arg]
        print(arg)
        match arg:
            case "--quantize-palette":
                print(quantize_palette)
                pipe = pipe.remap_to_existing_palette(quantize_palette[arg_count])
            case "--dither-basic":
                pipe = pipe.dither_basic(dither_basic[arg_count])
            case "--denoice":
                pipe = pipe.denoice()

        arg_used[arg] += 1
    pipe.write(output)


def _parse_arvg():
    args = [arg for arg in sys.argv[1:] if arg[:2] == "--"]
    return tuple(args)
