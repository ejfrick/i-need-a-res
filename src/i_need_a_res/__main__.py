"""Command-line interface."""
import click

from i_need_a_res.lib import return_prettified_valid_cities
from i_need_a_res.opentable_util.lib import OpenTableCities
from i_need_a_res.opentable_util.opentable import (
    get_reservation as get_opentable_reservation,
)
from i_need_a_res.resy_util.lib import ResyCities
from i_need_a_res.resy_util.resy import get_reservation as get_resy_reservation


@click.command()
@click.option("--city", type=click.Choice(return_prettified_valid_cities(ResyCities), case_sensitive=False))  # type: ignore[arg-type]
@click.option("--party-members", type=int)
@click.option("--book-date", default="today")
@click.version_option()
def main() -> None:
    """I Need A Res."""


if __name__ == "__main__":
    main(prog_name="i-need-a-res")  # pragma: no cover
