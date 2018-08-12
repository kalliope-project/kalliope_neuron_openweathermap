import sys
import pyowm
from datetime import datetime

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')


def get_weather_forecast(daily_forecasts, day):
    """
    return a dict of weather data following the provided "day" string in the daily_forecasts object
    """
    return {
        "max_temp": int(round(daily_forecasts[day]['forecast_temperatures']['max'])),
        "min_temp": int(round(daily_forecasts[day]['forecast_temperatures']['min'])),
        "temp": int(round(daily_forecasts[day]['forecast_temperatures']['day'])),
        "evening_temp": int(round(daily_forecasts[day]['forecast_temperatures']['eve'])),
        "morning_temp": int(round(daily_forecasts[day]['forecast_temperatures']['morn'])),
        "night_temp": int(round(daily_forecasts[day]['forecast_temperatures']['night'])),
        "weather_status": daily_forecasts[day]['forecast_weather_status'],
        "humidity": daily_forecasts[day]['forecast_humidity'],
        "wind_speed": daily_forecasts[day]['forecast_wind'].get('speed', None),
        "wind_deg": daily_forecasts[day]['forecast_wind'].get('deg', None),
        "pressure": daily_forecasts[day]['forecast_pressure'].get('press', None),
        "sea_level": daily_forecasts[day]['forecast_pressure'].get('sea_level', None),
        "rainfall": daily_forecasts[day]['forecast_rain'].get('all', None),
        "snowfall": daily_forecasts[day]['forecast_snow'].get('all', None)
    }


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
        self.am_pm_time = kwargs.get('12h_format', False)

        # check if parameters have been provided
        if self._is_parameters_ok():
            # Units in pyown need to be in lowercase
            self.temp_unit = self.temp_unit.lower()
            
            extended_location = self.location
            if self.country is not None:
                self.extended_location = self.location + "," + self.country

            owm = pyowm.OWM(API_key=self.api_key, language=self.lang)
            
            # Current 
            observation = owm.weather_at_place(extended_location)
            weather_current = observation.get_weather()
            
            found_location = observation.get_location()
            location = found_location.get_name()
            latitude = found_location.get_lat()
            longitude = found_location.get_lon()
            
            weather_current_status = weather_current.get_detailed_status()
            sunset_time_today = weather_current.get_sunset_time()
            sunrise_time_today = weather_current.get_sunrise_time()

            time_format = '%H:%M'
            if self.am_pm_time:
                time_format = '%I:%M %p'

            sunset_time_today = datetime.fromtimestamp(sunset_time_today).strftime(time_format)
            sunrise_time_today = datetime.fromtimestamp(sunrise_time_today).strftime(time_format)
            
            temp_current = weather_current.get_temperature(unit=self.temp_unit)
            temp_current_temp = temp_current['temp']
            temp_current_temp_max = temp_current['temp_max']
            temp_current_temp_min = temp_current['temp_min']

            pressure_current = weather_current.get_pressure()
            pressure_current_press = pressure_current.get('press', None)
            pressure_current_sea_level = pressure_current.get('sea_level', None)

            humidity_current = weather_current.get_humidity()
            
            wind_current = weather_current.get_wind()
            wind_current_deg = wind_current.get('deg', None)
            wind_current_speed = wind_current.get('speed', None)

            snow_current = weather_current.get_snow()
            snow_current = snow_current.get('all', None)
            
            rain_current = weather_current.get_rain()
            rain_current = rain_current.get('all', None)
            
            clouds_coverage_current = weather_current.get_clouds()
            
            # Tomorrow
            forecast = owm.daily_forecast(extended_location)
            tomorrow = pyowm.timeutils.tomorrow()
            weather_tomorrow = forecast.get_weather_at(tomorrow)
            weather_tomorrow_status = weather_tomorrow.get_detailed_status()

            temp_tomorrow = weather_tomorrow.get_temperature(unit=self.temp_unit)
            temp_tomorrow_temp = temp_tomorrow['day']
            temp_tomorrow_temp_max = temp_tomorrow['max']
            temp_tomorrow_temp_min = temp_tomorrow['min']
            temp_tomorrow_eve = temp_tomorrow['eve']
            temp_tomorrow_morning = temp_tomorrow['morn']
            temp_tomorrow_night = temp_tomorrow['night']
            
            pressure_tomorrow = weather_tomorrow.get_pressure()
            pressure_tomorrow_press = pressure_tomorrow.get('press', None)
            pressure_tomorrow_sea_level = pressure_tomorrow.get('sea_level', None)
            
            humidity_tomorrow = weather_tomorrow.get_humidity()

            wind_tomorrow = weather_tomorrow.get_wind()
            wind_tomorrow_deg = wind_tomorrow.get('all', None)
            wind_tomorrow_speed = wind_tomorrow.get('speed', None)

            snow_tomorrow = weather_tomorrow.get_snow()
            snow_tomorrow = snow_tomorrow.get('all', None)
            
            rain_tomorrow = weather_tomorrow.get_rain()
            rain_tomorrow = rain_tomorrow.get('all', None)

            clouds_coverage_tomorrow = weather_tomorrow.get_clouds()

            today = datetime.now().strftime('%A').lower()
            
            # Daily forecast
            daily_forecasts = dict()
            weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', today]
            forecasts = forecast.get_forecast()
            for weather in forecasts.get_weathers():
                for day in weekdays:
                    if day == datetime.fromtimestamp(weather.get_reference_time()).strftime('%A').lower():
                        data_for_day = {'forecast_temperatures': weather.get_temperature(self.temp_unit),
                                        'forecast_weather_status': weather.get_detailed_status(),
                                        'forecast_humidity': weather.get_humidity(),
                                        'forecast_wind': weather.get_wind(),
                                        'forecast_pressure': weather.get_pressure(),
                                        'forecast_rain': weather.get_rain(),
                                        'forecast_snow': weather.get_snow()
                                        }
                        if today == day:
                            daily_forecasts.update({'today': data_for_day})
                        daily_forecasts.update({day: data_for_day})

            message = {
                "location": location,
                "longitude": longitude,
                "latitude": latitude,
                "sunset_today": sunset_time_today,
                "sunrise_today": sunrise_time_today,

                "current": {
                    "weather_status": weather_current_status,
                    "temp": int(round(temp_current_temp)),
                    "max_temp": int(round(temp_current_temp_max)),
                    "min_temp": int(round(temp_current_temp_min)),
                    "pressure": pressure_current_press,
                    "sea_level": pressure_current_sea_level,
                    "humidity": humidity_current,
                    "wind_deg": wind_current_deg,
                    "wind_speed": wind_current_speed,
                    "snowfall": snow_current,
                    "rainfall": rain_current,
                    "clouds_coverage": clouds_coverage_current,
                },

                "tomorrow": {
                    "weather_status": weather_tomorrow_status,
                    "temp": int(round(temp_tomorrow_temp)),
                    "max_temp": int(round(temp_tomorrow_temp_max)),
                    "min_temp": int(round(temp_tomorrow_temp_min)),
                    "evening_temp": int(round(temp_tomorrow_eve)),
                    "morning_temp": int(round(temp_tomorrow_night)),
                    "night_temp": int(round(temp_tomorrow_morning)),
                    "pressure": pressure_tomorrow_press,
                    "sea_level": pressure_tomorrow_sea_level,
                    "humidity": humidity_tomorrow,
                    "wind_deg": wind_tomorrow_deg,
                    "wind_speed": wind_tomorrow_speed,
                    "snowfall": snow_tomorrow,
                    "rainfall": rain_tomorrow,
                    "clouds_coverage": clouds_coverage_tomorrow,
                },

                "today": get_weather_forecast(daily_forecasts, "today"),
                "monday": get_weather_forecast(daily_forecasts, "monday"),
                "tuesday": get_weather_forecast(daily_forecasts, "tuesday"),
                "wednesday": get_weather_forecast(daily_forecasts, "wednesday"),
                "thursday": get_weather_forecast(daily_forecasts, "thursday"),
                "friday": get_weather_forecast(daily_forecasts, "friday"),
                "saturday": get_weather_forecast(daily_forecasts, "saturday"),
                "sunday": get_weather_forecast(daily_forecasts, "sunday"),

            }

            if self.day:
                message.update({"day": self.day.lower()})
            self.say(message)

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
