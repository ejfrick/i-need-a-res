"""I Need A Res."""
from datetime import datetime as dt
from datetime import timedelta as td


class LocationError(ValueError):
    """A custom exception for invalid locations."""

    pass


def convert_book_date_to_datetime(book_date: str) -> dt:
    """Converts human-friendly date options into a datetime object.

    Args:
        book_date: date to book reservation

    Returns:
        A datetime object representation of the book date.

    """
    if book_date.lower() == "today":
        book_datetime = dt.now()
    elif book_date.lower() == "tomorrow":
        book_datetime = dt.now() + td(days=1)
    else:
        book_datetime = dt.strptime(book_date, "%m/%d/%Y")

    return book_datetime
