"""Command-line interface."""
import click

from i_need_a_res.lib import return_prettified_valid_cities
from i_need_a_res.resy_util.lib import ResyCities


@click.command()
@click.option("--city", type=click.Choice(return_prettified_valid_cities(ResyCities), case_sensitive=False))  # type: ignore[arg-type]
@click.option("--party-members", type=int)
@click.option("--book-date", default="today")
@click.version_option()
def main() -> None:
    """I Need A Res."""


if __name__ == "__main__":
    main(prog_name="i-need-a-res")  # pragma: no cover
