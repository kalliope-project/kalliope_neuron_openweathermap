from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from datetime import datetime, timedelta
from kalliope.core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException
from time import sleep

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
        self.wind_speed_unit = kwargs.get('wind_speed_unit', 'meters_sec')
        
        self.time_format = '%H:%M'         
        if self.am_pm_time:
            self.time_format = '%I:%M %p'

        # check if parameters have been provided
        if not self._is_parameters_ok():
            raise InvalidParameterException

        config_dict = get_default_config()
        config_dict['language'] = self.lang

        # connect with the api. this will work every time
        owm = OWM(self.api_key, config_dict)

        loc = owm.city_id_registry()
        location_list = loc.locations_for(self.location, country=self.country.upper() if self.country else None)
        if not location_list:
            raise MissingParameterException("OpenWeatherMap did not find the location %s" % self.location)
        
        # we only care about the first location in the list
        location = location_list[0]

        returned_message = dict()
        # load location, longitude and latitude
        returned_message["location"] = location.name
        returned_message["latitude"] = location.lat
        returned_message["longitude"] = location.lon

        mgr = owm.weather_manager()

        # in rare cases the neuron will failed to retrieve the data, we will retry 3 times, otherwise raise an exception
        for a in range(3):
            try:
                # we make a one_call to retrieve the weather data for current weather, hourly for the next 48 hours and a daily forecast for the next 7 days
                # see https://openweathermap.org/api/one-call-api
                weather_data = mgr.one_call(location.lat, location.lon)
            except Exception as e:
                if a == 2:
                    raise MissingParameterException("Openweathermap crashed and reported %s" % e)
                sleep(1)
                pass

        # get dict with current weather info
        returned_message["current"] = self._get_dict_weather_data(weather_data.current)

        # get all available forecast. This return a list of Weather object
        daily_forecast = dict()

        # get a forecast for the next 48 hours
        for hour in weather_data.forecast_hourly:
            time_object = datetime.fromtimestamp(hour.reference_time())
            day_weather = time_object.strftime('%A').lower()
            hour_weather = time_object.strftime('%H:%M').lower()
            if datetime.now().strftime("%Y-%m-%d") == time_object.strftime("%Y-%m-%d"):
                day_weather = "today"
            if day_weather not in daily_forecast:
                daily_forecast[day_weather] = dict()

            daily_forecast[day_weather][hour_weather] = self._get_dict_weather_data(hour)
        
        # get a daily forecast for the next 7 days
        for day in weather_data.forecast_daily:
            time_object = datetime.fromtimestamp(day.reference_time())
            day_weather = time_object.strftime('%A').lower()
            if datetime.now().strftime("%Y-%m-%d") == time_object.strftime("%Y-%m-%d"):
                day_weather = "today"
            if day_weather not in daily_forecast:
                daily_forecast[day_weather] = dict()

            daily_forecast[day_weather]["daily_forecast"] = self._get_dict_weather_data(day)

        returned_message.update(daily_forecast)

        # we have a missing day in the week, set it to None
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for day in weekdays:
            if day not in returned_message:
                returned_message[day] = None

        # just to make the neuron simpler to use from the end user template, add a key for tomorrow
        # that contains already reached data
        tomorrow = datetime.now() + timedelta(days=1)
        returned_message["tomorrow"] = daily_forecast.get(tomorrow.strftime('%A').lower())

        # forward the asked day to the template
        if self.day:
            returned_message.update({"day": self.day.lower()})
        self.say(returned_message)
    
    def _get_dict_weather_data(self, weather_data):
        """
        return a dict of current weather data from the observation object
        :return:
        """
        returned_dict = dict()
        returned_dict["weather_status"] = weather_data.detailed_status
        
        returned_dict["sunset"] = self._get_sun_rise_set_time(weather_data.sunset_time())
        returned_dict["sunrise"] = self._get_sun_rise_set_time(weather_data.sunrise_time())
        
        temp, temp_max, temp_min = self._get_temperatures_vaĺues(weather_data.temperature(unit=self.temp_unit))
        returned_dict["temperature"] = temp
        returned_dict["temperature_min"] = temp_min
        returned_dict["temperature_max"] = temp_max
        
        returned_dict["pressure"] = weather_data.pressure["press"]
        returned_dict["sea_level_pressure"] = weather_data.pressure["sea_level"]
        returned_dict["humidity"] = weather_data.humidity
        
        current_wind = weather_data.wind(self.wind_speed_unit)
        returned_dict["wind_deg"] = current_wind.get("deg", None)
        returned_dict["wind_speed"] = current_wind.get("speed", None)
        
        returned_dict["snow"] = self._get_snow_rain_value(weather_data.snow)
        returned_dict["rainfall"] = self._get_snow_rain_value(weather_data.rain)
        returned_dict["clouds_coverage"] = weather_data.clouds

        return returned_dict

    def _get_sun_rise_set_time(self, sun_time):
        """
        Three hours forecast returns none for sunrise and sunset,
        only current weather and daily forecast returns times.
        :return: formated sunrise / sunset time or none
        """
        if sun_time:
            return datetime.fromtimestamp(sun_time).strftime(self.time_format)
        return sun_time

    def _get_snow_rain_value(self, _dict):
        """
        Current weather key is "1h".
        Three hours forecast key is "3h".
        Daily forecast key is "all".
        :return: matching value, or None
        """
        if _dict.get("1h"):
            return _dict.get("1h")
        if _dict.get("3h"):
            return _dict.get("3h")
        if _dict.get("all"):
            return _dict.get("all")
        return None

    def _get_temperatures_vaĺues(self, _dict):
        """
        Current weather and three hour forecast returns a "temp, temp_max, temp_min" key.
        Daily forecast returns "day, min, max" key.
        :return: matching rounded int value, or None
        """
        temp = None
        temp_max = None
        temp_min = None

        if _dict.get("temp"):
            temp = int(round(_dict.get("temp")))
        if _dict.get("day"):
            temp = int(round(_dict.get("day")))
        if _dict.get("min"):
            temp_min = int(round(_dict.get("min")))
        if _dict.get("temp_min"):
            temp_min = int(round(_dict.get("temp_min")))
        if _dict.get("max"):
            temp_max = int(round(_dict.get("max")))
        if _dict.get("temp_max"):
            temp_max = int(round(_dict.get("temp_max")))

        return temp, temp_max, temp_min

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

