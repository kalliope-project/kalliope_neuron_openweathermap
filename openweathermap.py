import pyowm
from datetime import datetime, timedelta

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException
from pyowm.exceptions.api_response_error import UnauthorizedError, NotFoundError


class Openweathermap(NeuronModule):
    def __init__(self, **kwargs):
        # get message to spell out loud
        super(Openweathermap, self).__init__(**kwargs)

        self.api_key = kwargs.get('api_key', None)
        self.location = kwargs.get('location', None)
        self.lang = kwargs.get('lang', 'en')
        self.temp_unit = kwargs.get('temp_unit', 'celsius').lower()
        self.country = kwargs.get('country', None)
        self.day = kwargs.get('day', None)
        self.am_pm_time = kwargs.get('12h_format', False)

        # check if parameters have been provided
        if not self._is_parameters_ok():
            raise InvalidParameterException

        extended_location = self.location

        if self.country is not None:
            extended_location = self.location + "," + self.country

        # connect with the api. this will work every time
        owm = pyowm.OWM(API_key=self.api_key, language=self.lang)

        # search for current weather the provided place
        try:
            observation = owm.weather_at_place(extended_location)
        except UnauthorizedError as e:
            raise MissingParameterException("OpenWeatherMap crashed and reported %s" % e)
        except NotFoundError:
            raise MissingParameterException("OpenWeatherMap did not find the location %s" % self.location)

        returned_message = dict()

        # load location, longitude and latitude
        returned_message["location"] = observation.get_location().get_name()
        returned_message["latitude"] = observation.get_location().get_lat()
        returned_message["longitude"] = observation.get_location().get_lon()

        # get dict with current weather info
        current_weather = observation.get_weather()
        returned_message["current"] = self._get_dict_weather_data(current_weather)

        # forecast
        self.forecast = owm.three_hours_forecast(extended_location)
        # get all available forecast. This return a list of Weather object
        daily_forecasts = dict()
        forecasts = self.forecast.get_forecast()
        for weather in forecasts.get_weathers():
            day_weather_object = datetime.fromtimestamp(weather.get_reference_time())
            day_weather = day_weather_object.strftime('%A').lower()
            hour_weather = day_weather_object.strftime('%H:%M').lower()
            if day_weather not in daily_forecasts:
                daily_forecasts[day_weather] = dict()
            daily_forecasts[day_weather][hour_weather] = self._get_dict_weather_data(weather)
        returned_message.update(daily_forecasts)

        # we have a missing day in the week, set it to None
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for day in weekdays:
            if day not in returned_message:
                returned_message[day] = None

        # just to make the neuron simpler to use from the end user template, add a key for today and tomorrow
        # that contains already reached data
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow = tomorrow.strftime('%A').lower()
        today = datetime.now().strftime('%A').lower()
        returned_message["today"] = daily_forecasts.get(today)
        returned_message["tomorrow"] = daily_forecasts.get(tomorrow)
        # import pprint
        # pprint.pprint(returned_message)
        # forward the asked day to the template
        if self.day:
            returned_message.update({"day": self.day.lower()})
        self.say(returned_message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: NotImplementedError
        """
        if self.api_key is None:
            raise MissingParameterException("OpenWeatherMap neuron needs an api_key")
        if self.location is None:
            raise MissingParameterException("OpenWeatherMap neuron needs a location")

        return True

    def _get_dict_weather_data(self, weather_current):
        """
        return a dict of current weather data from the observation object
        :return:
        """

        returned_dict = dict()
        returned_dict["weather_status"] = weather_current.get_detailed_status()

        time_format = '%H:%M'
        if self.am_pm_time:
            time_format = '%I:%M %p'

        returned_dict["sunset"] = datetime.fromtimestamp(weather_current.get_sunset_time()).strftime(time_format)
        returned_dict["sunrise"] = datetime.fromtimestamp(weather_current.get_sunrise_time()).strftime(time_format)

        returned_dict["temperature"] = int(round(weather_current.get_temperature(unit=self.temp_unit)["temp"]))
        returned_dict["temperature_min"] = int(round(weather_current.get_temperature(unit=self.temp_unit)["temp_min"]))
        returned_dict["temperature_max"] = int(round(weather_current.get_temperature(unit=self.temp_unit)["temp_max"]))

        returned_dict["pressure"] = weather_current.get_pressure()["press"]
        returned_dict["sea_level_pressure"] = weather_current.get_pressure()["sea_level"]

        returned_dict["humidity"] = weather_current.get_humidity()

        wind = weather_current.get_wind()
        wind_deg = wind.get("deg", None)
        wind_speed = wind.get("speed", None)
        returned_dict["wind_deg"] = wind_deg
        returned_dict["wind_speed"] = wind_speed

        snow_current = weather_current.get_snow()
        snow_current = snow_current.get('all', None)
        rain_current = weather_current.get_rain()
        rain_current = rain_current.get('all', None)
        returned_dict["rainfall"] = rain_current
        returned_dict["snow"] = snow_current

        returned_dict["clouds_coverage"] = weather_current.get_clouds()

        return returned_dict
