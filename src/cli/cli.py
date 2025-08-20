import click
from os import getcwd, path, listdir
from pathlib import Path
from platformdirs import user_config_dir
from backend.models.image_pipeline import ImagePipeline
from cli.config import Config


@click.group()
@click.argument("imagepath", type=click.Path())
@click.option(
    "--config", "-c", type=click.Path(), help="path to the config in the file system"
)
@click.pass_context
def cli(ctx, imagepath: str, config: str):
    ctx.ensure_object(dict)
    ctx.obj["PIPELINE"] = ImagePipeline(imagepath)
    ctx.obj["CONFIG"] = Config(config)


@cli.command()
@click.pass_context
@click.option("--basic", "-b", is_flag=True, help="use dithering without color palette")
@click.option(
    "--palette", "-p", type=str, help="name of the palette from palette folder"
)
@click.option(
    "--grid-size",
    "-g",
    type=int,
    help="size of the grid for dithering, avalible sizes are: 2, 4, 8",
)
def dither(ctx, basic: bool, palette: str, grid_size: int):
    """
    dither image, reducing number of colors to 8 with pattern
    """
    pipeline: ImagePipeline = ctx.obj["PIPELINE"]
    config: Config = ctx.obj["CONFIG"]

    _, pal_dir = handle_palette_list(config.palette_dir)

    try:
        validate(
            config=config,
            palette=palette,
            number=grid_size,
            number_bounds=[2, 4, 8],
            basic=basic,
        )
    except ValueError as e:
        click.echo(f"ERROR: {e}")
        return

    if basic:
        pipeline = pipeline.dither_basic(grid_size)
    else:
        palette = path.join(pal_dir, f"{palette}.json")
        pipeline = pipeline.dither_palette(grid_size, palette)

    write_image(pipeline, config)


@cli.command()
@click.pass_context
@click.option(
    "--basic", "-b", is_flag=True, help="use automatic colors without color palette"
)
@click.option(
    "--palette", "-p", type=str, help="name of the palette from palette folder"
)
@click.option("--n-colors", "-n", type=int, help="number of colors in resulting image")
def quantize(ctx, basic: bool, palette: str, n_colors: int):
    """
    basically reduce number of colors according to a pallete or number of colors
    """
    pipeline: ImagePipeline = ctx.obj["PIPELINE"]
    config: Config = ctx.obj["CONFIG"]

    _, pal_dir = handle_palette_list(config.palette_dir)

    try:
        validate(
            config=config,
            palette=palette,
            number=n_colors,
            number_bounds=[8, 27, 64],
            basic=basic,
        )
    except ValueError as e:
        click.echo(f"ERROR: {e}")
        return

    if basic:
        pipeline = pipeline.quantize(n_colors)
    else:
        palette = path.join(pal_dir, f"{palette}.json")
        pipeline = pipeline.remap_to_existing_palette(palette)

    write_image(pipeline, config)


def handle_output_location(input: str, save_dir: str) -> str:
    file_name = str(path.basename(input)).split(".")
    if save_dir == "current":
        save_dir = getcwd()
        save_name = "".join(file_name[:-1]) + "_modified" + ".png"
    else:
        save_name = str(path.basename(input))
    if not path.exists(save_dir):
        raise ValueError("Wrong save dir")
    return path.join(save_dir, save_name)


def handle_palette_list(palette_path) -> tuple[list[str], str]:
    if palette_path == "default":
        palette_path = path.join(user_config_dir("gistqd"), "palettes")
    files: list[str] = listdir(palette_path)
    names: list[str] = [
        Path(file).stem for file in files if path.splitext(file)[-1] == ".json"
    ]
    return names, palette_path


def validate(config, palette, number, number_bounds, basic) -> None:
    availible_palette, _ = handle_palette_list(config.palette_dir)
    if (palette and palette not in availible_palette) or (not basic and not palette):
        raise ValueError(
            f"Wrong palette, avalible palettes: {', '.join(availible_palette)}"
        )
    if number and number not in number_bounds:
        raise ValueError(f"Value is out of bounds, avalible bounds {number_bounds}")


def write_image(pipeline: ImagePipeline, config: Config) -> None:
    try:
        pipeline.write(
            handle_output_location(pipeline.in_path, config.default_output_dir)
        )
    except ValueError:
        to_cwd = click.prompt(
            "Youc config path seems to be corrupted, would you like to save image in the current directory (y/n): ",
            type=bool,
        )
        if to_cwd:
            pipeline.write(handle_output_location(pipeline.in_path, "current"))


if __name__ == "__main__":
    cli()
