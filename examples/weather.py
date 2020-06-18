"""An example CLI for requesting weather information from the OpenWeather API.

The example demonstrates the usage of arguments, options and flags,
as well as descriptions and default values of arguments and options.

Usage:
    $ python weather.py Kharkiv Ukraine
    As of 2020-05-22 08:42:58:
        11.5°C (feels like 8.2°C)
        scattered clouds

    $ python weather.py Kharkiv Ukraine --forecast --lines 2
    As of 2020-05-22 09:00:00:
        9.5°C (feels like 6.3°C)
        scattered clouds

    As of 2020-05-22 12:00:00:
        12.2°C (feels like 7.7°C)
        light rain
"""

from datetime import datetime
from os import environ
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from mints import cli, Arg, Opt, Flag


class API:
    """A client for the OpenWeather API."""

    url = 'https://api.openweathermap.org/data/2.5/'

    def __init__(self, key: str):
        self.key = key

    def weather(self, city: str, country: str) -> Any:
        """Requests the current weather for the specified city."""
        return self.request('weather', q=f'{city},{country}')

    def forecast(self, city: str, country: str, lines: Optional[str]) -> Any:
        """Requests a forecast for the specified city."""
        return self.request('forecast', q=f'{city},{country}', cnt=lines)

    def request(self, endpoint: str, **params: Any) -> Any:
        """Performs a request to the OpenWeather API."""

        url = urljoin(self.url, endpoint)

        try:
            response = requests.get(url, params={'appid': self.key, **params})
            response.raise_for_status()
        except requests.HTTPError as error:
            exit(f'{error.response.status_code} HTTP error '
                 f'occurred during a request to "{endpoint}": \n'
                 f'> {error.response.json()["message"]}')
        else:
            return response.json()


@cli
def weather(city:     Arg('A city to request weather or a forecast for.'),
            country:  Arg('A country where the city is located.'),
            forecast: Flag('Whether to provide a forecast.'),
            lines:    Opt('The amount of lines to be included in a forecast.') = None,
            key:      Opt('The OpenWeather API key.') = None):
    """Find out the current weather or a forecast in any city.

    The CLI allows you to retrieve weather or a forecast for
    a specified city using the OpenWeather API. It requires an
    API key to work (the key can be specified either directly via
    the `--key` option or in an environment variable "WEATHER_KEY").

    If the `--forecast` flag is provided, the CLI will request a
    forecast for 5 days with 3-hour period. By default, 40 lines
    of data are returned. This can be controlled with the `--lines`
    option.
    """

    def celsius(kelvin: float) -> float:
        return round(kelvin - 273.15, 1)

    def rendered(entry: Dict[str, Any]) -> str:
        time = datetime.fromtimestamp(entry['dt'])
        temp = celsius(entry['main']['temp'])
        feel = celsius(entry['main']['feels_like'])
        desc = ', '.join(x['description'] for x in entry['weather'])

        return f'As of {time}: \n' \
               f'    {temp}°C (feels like {feel}°C) \n' \
               f'    {desc}'

    key = key or environ.get('WEATHER_KEY')
    api = API(key)

    if forecast:
        result = api.forecast(city, country, lines)
        result = (rendered(x) for x in result['list'])

        print('\n\n'.join(result))
    else:
        if lines is not None:
            exit('The `--lines` option was specified, '
                 'but `--forecast` was not.')

        result = api.weather(city, country)

        print(rendered(result))


if __name__ == '__main__':
    cli()
