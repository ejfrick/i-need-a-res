"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """I Need A Res."""


if __name__ == "__main__":
    main(prog_name="i-need-a-res")  # pragma: no cover
