"""Command-line interface."""
from random import choice
from typing import Tuple

import click

from i_need_a_res.lib import LocationError
from i_need_a_res.lib import convert_book_date_to_datetime
from i_need_a_res.lib import return_prettified_valid_cities
from i_need_a_res.opentable_util.lib import OpenTableCities
from i_need_a_res.opentable_util.opentable import (
    get_reservation as get_opentable_reservation,
)
from i_need_a_res.resy_util.lib import ResyCities
from i_need_a_res.resy_util.resy import get_reservation as get_resy_reservation


@click.command()
@click.option("--city", type=click.Choice(return_prettified_valid_cities(ResyCities), case_sensitive=False), help="City to book the reservation in. Must be one of supported.")  # type: ignore[arg-type]
@click.option("--party-members", type=int, help="Party size. Must be a number.")
@click.option(
    "--book-date",
    default="today",
    type=str,
    help="Date for the reservation. Must be either today, tomorrow, or in MM/DD/YYYY format.",
)
@click.option(
    "--resy-auth",
    nargs=2,
    type=str,
    help="Resy authorization. Must be in the format API_KEY,USER_TOKEN",
)
@click.option(
    "--opentable-auth",
    nargs=2,
    type=str,
    help="OpenTable authorization. Must be in the format API_KEY,USER_TOKEN",
)
@click.version_option()
def main(
    city: str,
    party_members: int,
    book_date: str,
    resy_auth: Tuple[str, str],
    opentable_auth: Tuple[str, str],
) -> None:
    """I Need A Res. For when you just need somewhere to sit and eat."""
    resy_api_key, resy_user_token = resy_auth
    opentable_api_key, opentable_user_token = opentable_auth
    book_datetime = convert_book_date_to_datetime(book_date)

    try:
        resy_pick = get_resy_reservation(
            api_key=resy_api_key,
            auth_token=resy_user_token,
            city=city,
            search_day=book_datetime,
            party_size=party_members,
        )
    except LocationError:
        click.echo(
            f"Location {city} is not supported by Resy. Please pick another location.",
            err=True,
        )
    except Exception as e:
        click.echo(f"Something went wrong: {e}", err=True)

    try:
        opentable_pick = get_opentable_reservation(
            api_key=opentable_api_key,
            auth_token=opentable_user_token,
            city=city,
            search_day=book_datetime,
            party_size=party_members,
        )
    except LocationError:
        click.echo(
            f"Location {city} is not supported by OpenTable. Please pick another location",
            err=True,
        )
    except Exception as e:
        click.echo(f"Something went wrong: {e}", err=True)

    picks = [pick for pick in [resy_pick, opentable_pick] if pick is not None]
    rand_pick = choice(picks)

    click.echo(f"There is {rand_pick}")


if __name__ == "__main__":
    main(prog_name="i-need-a-res")  # pragma: no cover
