"""Command-line interface."""
from random import choice
from typing import Optional
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
@click.option("--party-members", type=click.INT, help="Party size. Must be a number.")
@click.option(
    "--book-date",
    default="today",
    type=click.STRING,
    help="Date for the reservation. Must be either today, tomorrow, or in MM/DD/YYYY format.",
)
@click.option(
    "--resy-auth",
    nargs=2,
    type=click.STRING,
    help="Resy authorization. Must be in the format API_KEY,USER_TOKEN",
    default=None,
)
@click.option(
    "--opentable-auth",
    nargs=2,
    type=click.STRING,
    help="OpenTable authorization. Must be in the format API_KEY,USER_TOKEN",
    default=None,
)
@click.version_option()
def cli(
    city: str,
    party_members: int,
    book_date: str,
    resy_auth: Optional[Tuple[str, str]],
    opentable_auth: Optional[Tuple[str, str]],
) -> None:
    """I Need A Res. For when you just need somewhere to sit and eat."""
    resy_api_key, resy_user_token = resy_auth if resy_auth is not None else None, None
    opentable_api_key, opentable_user_token = (
        opentable_auth if opentable_auth is not None else None,
        None,
    )
    book_datetime = convert_book_date_to_datetime(book_date)

    if resy_api_key is not None:
        try:
            resy_pick = get_resy_reservation(
                api_key=resy_api_key,  # type: ignore[arg-type]
                auth_token=resy_user_token,  # type: ignore[arg-type]
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
    else:
        resy_pick = None

    if opentable_api_key is not None:
        try:
            opentable_pick = get_opentable_reservation(
                api_key=opentable_api_key,  # type: ignore[arg-type]
                auth_token=opentable_user_token,  # type: ignore[arg-type]
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
    else:
        opentable_pick = None

    picks = [pick for pick in [resy_pick, opentable_pick] if pick is not None]
    rand_pick = choice(picks)

    click.echo(f"There is {rand_pick}")


if __name__ == "__main__":
    cli(prog_name="i-need-a-res")  # pragma: no cover
