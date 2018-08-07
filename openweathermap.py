import pyowm
import requests
import json
from datetime import datetime

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException


class Openweathermap(NeuronModule):
    def __init__(self, **kwargs):
        # get message to spell out loud
        super(Openweathermap, self).__init__(**kwargs)

        self.api_key = kwargs.get('api_key', None)
        self.location = kwargs.get('location', None)
        self.lang = kwargs.get('lang', 'en')
        self.temp_unit = kwargs.get('temp_unit', 'celsius')
        self.country = kwargs.get('country', None)
        self.day = kwargs.get('day', None)
        self.days = kwargs.get('days_translation', {'Monday': 'monday',
                                        'Tuesday': 'tuesday',
                                        'Wednesday': 'wednesday',
                                        'Thursday': 'thursday',
                                        'Friday': 'friday',
                                        'Saturday': 'saturday',
                                        'Sunday': 'sunday'})
        
        # check if parameters have been provided
        if self._is_parameters_ok():
            # Units in pyown need to be in lowercase
            self.temp_unit = self.temp_unit.lower()
            
            extended_location = self.location
            if self.country is not None:
                self.extended_location = self.location + "," + self.country
            if not self.day:
                owm = pyowm.OWM(API_key=self.api_key, language=self.lang)

                # Tomorrow
                forecast = owm.daily_forecast(extended_location)
                tomorrow = pyowm.timeutils.tomorrow()
                weather_tomorrow = forecast.get_weather_at(tomorrow)
                weather_tomorrow_status = weather_tomorrow.get_detailed_status()
                sunset_time_tomorrow = weather_tomorrow.get_sunset_time('iso')
                sunrise_time_tomorrow = weather_tomorrow.get_sunrise_time('iso')

                temp_tomorrow = weather_tomorrow.get_temperature(unit=self.temp_unit)
                temp_tomorrow_temp = temp_tomorrow['day']
                temp_tomorrow_temp_max = temp_tomorrow['max']
                temp_tomorrow_temp_min = temp_tomorrow['min']

                pressure_tomorrow = weather_tomorrow.get_pressure()
                pressure_tomorrow_press = pressure_tomorrow['press']
                pressure_tomorrow_sea_level = pressure_tomorrow['sea_level']

                humidity_tomorrow = weather_tomorrow.get_humidity()

                wind_tomorrow = weather_tomorrow.get_wind()
                # wind_tomorrow_deg = wind_tomorrow['deg']
                wind_tomorrow_speed = wind_tomorrow['speed']

                snow_tomorrow = weather_tomorrow.get_snow()
                rain_tomorrow = weather_tomorrow.get_rain()
                clouds_coverage_tomorrow = weather_tomorrow.get_clouds()

                # Today
                observation = owm.weather_at_place(extended_location)
                weather_today = observation.get_weather()
                weather_today_status = weather_today.get_detailed_status()
                sunset_time_today = weather_today.get_sunset_time('iso')
                sunrise_time_today = weather_today.get_sunrise_time('iso')

                temp_today = weather_today.get_temperature(unit=self.temp_unit)
                temp_today_temp = temp_today['temp']
                temp_today_temp_max = temp_today['temp_max']
                temp_today_temp_min = temp_today['temp_min']

                pressure_today = weather_today.get_pressure()
                pressure_today_press = pressure_today['press']
                pressure_today_sea_level = pressure_today['sea_level']

                humidity_today = weather_today.get_humidity()

                wind_today = weather_today.get_wind()
                # disable temporarily this data. Will be fixed in the next release of pyown
                # see: https://github.com/csparpa/pyowm/issues/177
                try:
                    wind_today_deg = wind_today['deg']
                except KeyError:
                    wind_today_deg = None
                wind_today_speed = wind_today['speed']

                snow_today = weather_today.get_snow()
                rain_today = weather_today.get_rain()
                clouds_coverage_today = weather_today.get_clouds()

                message = {
                    "location": self.location,

                    "weather_today": weather_today_status,
                    "sunset_today_time": sunset_time_today,
                    "sunrise_today_time": sunrise_time_today,
                    "temp_today_temp": temp_today_temp,
                    "temp_today_temp_max": temp_today_temp_max,
                    "temp_today_temp_min": temp_today_temp_min,
                    "pressure_today_press": pressure_today_press,
                    "pressure_today_sea_level": pressure_today_sea_level,
                    "humidity_today": humidity_today,
                    "wind_today_deg": wind_today_deg,
                    "wind_today_speed": wind_today_speed,
                    "snow_today": snow_today,
                    "rain_today": rain_today,
                    "clouds_coverage_today": clouds_coverage_today,

                    "weather_tomorrow": weather_tomorrow_status,
                    "sunset_time_tomorrow": sunset_time_tomorrow,
                    "sunrise_time_tomorrow": sunrise_time_tomorrow,
                    "temp_tomorrow_temp": temp_tomorrow_temp,
                    "temp_tomorrow_temp_max": temp_tomorrow_temp_max,
                    "temp_tomorrow_temp_min": temp_tomorrow_temp_min,
                    "pressure_tomorrow_press": pressure_tomorrow_press,
                    "pressure_tomorrow_sea_level": pressure_tomorrow_sea_level,
                    "humidity_tomorrow": humidity_tomorrow,
                    # "wind_tomorrow_deg": wind_tomorrow_deg,
                    "wind_tomorrow_speed": wind_tomorrow_speed,
                    "snow_tomorrow": snow_tomorrow,
                    "rain_tomorrow": rain_tomorrow,
                    "clouds_coverage_tomorrow": clouds_coverage_tomorrow
                }

                self.say(message)
            # Daily forecast
            if self.day:
                forecast = self.GetForecast(extended_location)
                self.say(forecast)
                    
    def GetForecast(self, location):
        # We dont use pyown for the daily forecast, and we don't won't to break the current config so we convert the units to the required parameter for the API call
        if self.temp_unit == 'celsius':
            self.temp_unit = 'metric'
        if self.temp_unit == 'fahrenheit':
            self.temp_unit = 'imperial'
        if self.temp_unit == 'kelvin':
            self.temp_unit = 'kelvin'
 
        # We use the API for the 5 day / 3 hours --> https://openweathermap.org/forecast5
        # Don't know why but we get a return of 7 days, so we can ask the weather for the next 7 days.
        url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=" + location + "&lang=" + self.lang + "&APPID=" + self.api_key + "&units=" + self.temp_unit
        response = requests.get(url)
        data = response.json()
        
        # To get the forecast for today we dont need self.days, so we update the dictionary with the current day
        if self.day == 'today':
            self.days.update({datetime.now().strftime('%A') : 'today'})

        forecasts = {}
        forecasts.update({'forecast_city' : data['city']['name']})
        for forecast in data['list']:   
            for en_day, user_day_in_dict in self.days.iteritems():
                if user_day_in_dict.lower() == self.day.lower():
                    if en_day == datetime.fromtimestamp(forecast['dt']).strftime('%A'):
                        forecasts.update({'forecast_temp' : int(round(forecast['temp']['day']))})
                        forecasts.update({'forecast_min_temp' : int(round(forecast['temp']['min']))})
                        forecasts.update({'forecast_max_temp' : int(round(forecast['temp']['max']))})
                        forecasts.update({'forecast_evening_temp' : int(round(forecast['temp']['eve']))})
                        forecasts.update({'forecast_morning_temp' : int(round(forecast['temp']['morn']))})
                        forecasts.update({'forecast_night_temp' : int(round(forecast['temp']['night']))})
                        for weather_description in forecast['weather']:
                            forecasts.update({'forecast_weather_descripton' : weather_description['description']})
                        forecasts.update({'forecast_day' : self.day})
        return forecasts
    
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
