import pyowm
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
            if self.am_pm_time:
                sunset_time_today = datetime.fromtimestamp(sunset_time_today).strftime('%I:%M %p')
                sunrise_time_today = datetime.fromtimestamp(sunrise_time_today).strftime('%I:%M %p')
            else:
                sunset_time_today = datetime.fromtimestamp(sunset_time_today).strftime('%H:%M')
                sunrise_time_today = datetime.fromtimestamp(sunrise_time_today).strftime('%H:%M')
            
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

            Today = datetime.now().strftime('%A')
            
            # Daily forecast
            daily_forecasts = {}
            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', Today]
            forecasts = forecast.get_forecast()
            for weather in forecasts.get_weathers():
                for day in weekdays:
                    if day == datetime.fromtimestamp(weather.get_reference_time()).strftime('%A'):
                        data_for_day = {'forecast_temperatures' : weather.get_temperature(self.temp_unit),
                                        'forecast_weather_status' : weather.get_detailed_status(),
                                        'forecast_humidity' : weather.get_humidity(),
                                        'forecast_wind' : weather.get_wind(),
                                        'forecast_pressure' : weather.get_pressure(),
                                        'forecast_rain' : weather.get_rain(),
                                        'forecast_snow' : weather.get_snow()
                                        }
                        if Today == day:
                            daily_forecasts.update({'Today' : data_for_day})
                        daily_forecasts.update({day : data_for_day})
        


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
                    "pressure": pressure_tomorrow_press,
                    "sea_level": pressure_tomorrow_sea_level,
                    "humidity": humidity_tomorrow,
                    "wind_deg": wind_tomorrow_deg,
                    "wind_speed": wind_tomorrow_speed,
                    "snowfall": snow_tomorrow,
                    "rainfall": rain_tomorrow,
                    "clouds_coverage": clouds_coverage_tomorrow,
                    },
                
                "today": {
                    "max_temp": int(round(daily_forecasts['Today']['forecast_temperatures']['max'])),
                    "min_temp": int(round(daily_forecasts['Today']['forecast_temperatures']['min'])),
                    "temp": int(round(daily_forecasts['Today']['forecast_temperatures']['day'])),
                    "evening_temp": int(round(daily_forecasts['Today']['forecast_temperatures']['eve'])),
                    "morning_temp": int(round(daily_forecasts['Today']['forecast_temperatures']['morn'])),
                    "night_temp": int(round(daily_forecasts['Today']['forecast_temperatures']['night'])),
                    "weather_status": daily_forecasts['Today']['forecast_weather_status'],
                    "humidity": daily_forecasts['Today']['forecast_humidity'],
                    "wind_speed" : daily_forecasts['Today']['forecast_wind'].get('speed', None),
                    "wind_deg": daily_forecasts['Today']['forecast_wind'].get('deg', None),
                    "pressure": daily_forecasts['Today']['forecast_pressure'].get('press', None),
                    "sea_level": daily_forecasts['Today']['forecast_pressure'].get('sea_level', None),
                    "rainfall": daily_forecasts['Today']['forecast_rain'].get('all', None),
                    "snowfall": daily_forecasts['Today']['forecast_snow'].get('all', None)
                    },
                
                "monday": {
                    "max_temp": int(round(daily_forecasts['Monday']['forecast_temperatures']['max'])),
                    "min_temp": int(round(daily_forecasts['Monday']['forecast_temperatures']['min'])),
                    "temp": int(round(daily_forecasts['Monday']['forecast_temperatures']['day'])),
                    "evening_temp": int(round(daily_forecasts['Monday']['forecast_temperatures']['eve'])),
                    "morning_temp": int(round(daily_forecasts['Monday']['forecast_temperatures']['morn'])),
                    "night_temp": int(round(daily_forecasts['Monday']['forecast_temperatures']['night'])),
                    "weather_status": daily_forecasts['Monday']['forecast_weather_status'],
                    "humidity": daily_forecasts['Monday']['forecast_humidity'],
                    "wind_speed" : daily_forecasts['Monday']['forecast_wind'].get('speed', None),
                    "wind_deg": daily_forecasts['Monday']['forecast_wind'].get('deg', None),
                    "pressure": daily_forecasts['Monday']['forecast_pressure'].get('press', None),
                    "sea_level": daily_forecasts['Monday']['forecast_pressure'].get('sea_level', None),
                    "rainfall": daily_forecasts['Monday']['forecast_rain'].get('all', None),
                    "snowfall": daily_forecasts['Monday']['forecast_snow'].get('all', None)
                    },
                
                "tuesday": {
                    "max_temp": int(round(daily_forecasts['Tuesday']['forecast_temperatures']['max'])),
                    "min_temp": int(round(daily_forecasts['Tuesday']['forecast_temperatures']['min'])),
                    "temp": int(round(daily_forecasts['Tuesday']['forecast_temperatures']['day'])),
                    "evening_temp": int(round(daily_forecasts['Tuesday']['forecast_temperatures']['eve'])),
                    "morning_temp": int(round(daily_forecasts['Tuesday']['forecast_temperatures']['morn'])),
                    "night_temp": int(round(daily_forecasts['Tuesday']['forecast_temperatures']['night'])),
                    "weather_status": daily_forecasts['Tuesday']['forecast_weather_status'],
                    "humidity": daily_forecasts['Tuesday']['forecast_humidity'],
                    "wind_speed" : daily_forecasts['Tuesday']['forecast_wind'].get('speed', None),
                    "wind_deg": daily_forecasts['Tuesday']['forecast_wind'].get('deg', None),
                    "pressure": daily_forecasts['Tuesday']['forecast_pressure'].get('press', None),
                    "sea_level": daily_forecasts['Tuesday']['forecast_pressure'].get('sea_level', None),
                    "rainfall": daily_forecasts['Tuesday']['forecast_rain'].get('all', None),
                    "snowfall": daily_forecasts['Tuesday']['forecast_snow'].get('all', None)
                    },
                
                "wednesday": {
                    "max_temp": int(round(daily_forecasts['Wednesday']['forecast_temperatures']['max'])),
                    "min_temp": int(round(daily_forecasts['Wednesday']['forecast_temperatures']['min'])),
                    "temp": int(round(daily_forecasts['Wednesday']['forecast_temperatures']['day'])),
                    "evening_temp": int(round(daily_forecasts['Wednesday']['forecast_temperatures']['eve'])),
                    "morning_temp": int(round(daily_forecasts['Wednesday']['forecast_temperatures']['morn'])),
                    "night_temp": int(round(daily_forecasts['Wednesday']['forecast_temperatures']['night'])),
                    "weather_status": daily_forecasts['Wednesday']['forecast_weather_status'],
                    "humidity": daily_forecasts['Wednesday']['forecast_humidity'],
                    "wind_speed" : daily_forecasts['Wednesday']['forecast_wind'].get('speed', None),
                    "wind_deg": daily_forecasts['Wednesday']['forecast_wind'].get('deg', None),
                    "pressure": daily_forecasts['Wednesday']['forecast_pressure'].get('press', None),
                    "sea_level": daily_forecasts['Wednesday']['forecast_pressure'].get('sea_level', None),
                    "rainfall": daily_forecasts['Wednesday']['forecast_rain'].get('all', None),
                    "snowfall": daily_forecasts['Wednesday']['forecast_snow'].get('all', None)
                    },
            
                "thursday": {
                    "max_temp": int(round(daily_forecasts['Thursday']['forecast_temperatures']['max'])),
                    "min_temp": int(round(daily_forecasts['Thursday']['forecast_temperatures']['min'])),
                    "temp": int(round(daily_forecasts['Thursday']['forecast_temperatures']['day'])),
                    "evening_temp": int(round(daily_forecasts['Thursday']['forecast_temperatures']['eve'])),
                    "morning_temp": int(round(daily_forecasts['Thursday']['forecast_temperatures']['morn'])),
                    "night_temp": int(round(daily_forecasts['Thursday']['forecast_temperatures']['night'])),
                    "weather_status": daily_forecasts['Thursday']['forecast_weather_status'],
                    "humidity": daily_forecasts['Thursday']['forecast_humidity'],
                    "wind_speed" : daily_forecasts['Thursday']['forecast_wind'].get('speed', None),
                    "wind_deg": daily_forecasts['Thursday']['forecast_wind'].get('deg', None),
                    "pressure": daily_forecasts['Thursday']['forecast_pressure'].get('press', None),
                    "sea_level": daily_forecasts['Thursday']['forecast_pressure'].get('sea_level', None),
                    "rainfall": daily_forecasts['Thursday']['forecast_rain'].get('all', None),
                    "snowfall": daily_forecasts['Thursday']['forecast_snow'].get('all', None)
                    },

                "friday": {
                    "max_temp": int(round(daily_forecasts['Friday']['forecast_temperatures']['max'])),
                    "min_temp": int(round(daily_forecasts['Friday']['forecast_temperatures']['min'])),
                    "temp": int(round(daily_forecasts['Friday']['forecast_temperatures']['day'])),
                    "evening_temp": int(round(daily_forecasts['Friday']['forecast_temperatures']['eve'])),
                    "morning_temp": int(round(daily_forecasts['Friday']['forecast_temperatures']['morn'])),
                    "night_temp": int(round(daily_forecasts['Friday']['forecast_temperatures']['night'])),
                    "weather_status": daily_forecasts['Friday']['forecast_weather_status'],
                    "humidity": daily_forecasts['Friday']['forecast_humidity'],
                    "wind_speed" : daily_forecasts['Friday']['forecast_wind'].get('speed', None),
                    "wind_deg": daily_forecasts['Friday']['forecast_wind'].get('deg', None),
                    "pressure": daily_forecasts['Friday']['forecast_pressure'].get('press', None),
                    "sea_level": daily_forecasts['Friday']['forecast_pressure'].get('sea_level', None),
                    "rainfall": daily_forecasts['Friday']['forecast_rain'].get('all', None),
                    "snowfall": daily_forecasts['Friday']['forecast_snow'].get('all', None)
                    },
                
                "saturday": {
                    "max_temp": int(round(daily_forecasts['Saturday']['forecast_temperatures']['max'])),
                    "min_temp": int(round(daily_forecasts['Saturday']['forecast_temperatures']['min'])),
                    "temp": int(round(daily_forecasts['Saturday']['forecast_temperatures']['day'])),
                    "evening_temp": int(round(daily_forecasts['Saturday']['forecast_temperatures']['eve'])),
                    "morning_temp": int(round(daily_forecasts['Saturday']['forecast_temperatures']['morn'])),
                    "night_temp": int(round(daily_forecasts['Saturday']['forecast_temperatures']['night'])),
                    "weather_status": daily_forecasts['Saturday']['forecast_weather_status'],
                    "humidity": daily_forecasts['Saturday']['forecast_humidity'],
                    "wind_speed" : daily_forecasts['Saturday']['forecast_wind'].get('speed', None),
                    "wind_deg": daily_forecasts['Saturday']['forecast_wind'].get('deg', None),
                    "pressure": daily_forecasts['Saturday']['forecast_pressure'].get('press', None),
                    "sea_level": daily_forecasts['Saturday']['forecast_pressure'].get('sea_level', None),
                    "rainfall": daily_forecasts['Saturday']['forecast_rain'].get('all', None),
                    "snowfall": daily_forecasts['Saturday']['forecast_snow'].get('all', None)
                    },
                
                "sunday": {
                    "max_temp": int(round(daily_forecasts['Sunday']['forecast_temperatures']['max'])),
                    "min_temp": int(round(daily_forecasts['Sunday']['forecast_temperatures']['min'])),
                    "temp": int(round(daily_forecasts['Sunday']['forecast_temperatures']['day'])),
                    "evening_temp": int(round(daily_forecasts['Sunday']['forecast_temperatures']['eve'])),
                    "morning_temp": int(round(daily_forecasts['Sunday']['forecast_temperatures']['morn'])),
                    "night_temp": int(round(daily_forecasts['Sunday']['forecast_temperatures']['night'])),
                    "weather_status": daily_forecasts['Sunday']['forecast_weather_status'],
                    "humidity": daily_forecasts['Sunday']['forecast_humidity'],
                    "wind_speed" : daily_forecasts['Sunday']['forecast_wind'].get('speed', None),
                    "wind_deg": daily_forecasts['Sunday']['forecast_wind'].get('deg', None),
                    "pressure": daily_forecasts['Sunday']['forecast_pressure'].get('press', None),
                    "sea_level": daily_forecasts['Sunday']['forecast_pressure'].get('sea_level', None),
                    "rainfall": daily_forecasts['Sunday']['forecast_rain'].get('all', None),
                    "snowfall": daily_forecasts['Sunday']['forecast_snow'].get('all', None)
                    }

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
