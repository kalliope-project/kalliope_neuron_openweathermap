# OpenWeatherMap API

## Synopsis 

Retrieve the weather for today, tomorrow or a forecast for 7 days for a specific day of the week with the related data (humidity, temperature, etc ...) for a given location. 

## Installation
```
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_openweathermap.git
```

## Options

| parameter       | required | default    | choices                     | comment                                                                                                    |
| --------------- | -------- | ---------- | --------------------------- | ---------------------------------------------------------------------------------------------------------- |
| api_key         | YES      | None       |                             | User API key of the OWM API get one [here](https://home.openweathermap.org/users/sign_up)                  |
| location        | YES      | None       |                             | The location                                                                                               |
| lang            | No       | en         |                             | Look for the supported languages [here](https://openweathermap.org/current#multi)                          |
| temp_unit       | No       | celsius    | celsius, kelvin, fahrenheit |                                                                                                            |
| wind_speed_unit | No       | meters_sec | meters_sec, miles_hour, km_hour, knots, beaufort |                                                                                       |
| country         | No       | None       |                             | [ISO-3166 Country Code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements)|
| 12h_format      | no       | False      | True/False                  | To get 12 hour format for sunrise and sunset return value                                                  |
| day             | No       | None       | today, tomorrow or weekday  | Only needed if you want a single synapse to catch the day and translate it in a file_template (required)   |


## Return Values

| Name      | Description                               | Type   | Sample                                                                    |
| --------- | ----------------------------------------- | ------ | ------------------------------------------------------------------------- |
| location  | The current location                      | String | Grenoble                                                                  |
| longitude | The current longitude                     | Float  | 5.73                                                                      |
| latitude  | The current latitude                      | Float  | 45.18                                                                     |
| current   | Dict of weather data for the current time | Dict   | {'clouds_coverage': 24, 'humidity': 68, 'pressure': 855.16 ... }          |
| tomorrow  | Dict of weather data for tomorrow         | Dict   | {'<time_value>': { <weatherdata> }, {'<time_value>': { <weather_data> }}  |
| today     | Dict of weather data for today            | Dict   | {'<time_value>': { <weather_data> }, {'<time_value>': { <weather_data> }} |
| monday    | Dict of weather data for monday           | Dict   | {'<time_value>': { <weather_data> }, {'<time_value>': { <weather_data> }} |
| tuesday   | Dict of weather data for tuesday          | Dict   | {'<time_value>': { <weather_data> }, {'<time_value>': { <weather_data> }} |
| wednesday | Dict of weather data for wednesday        | Dict   | {'<time_value>': { <weather_data> }, {'<time_value>': { <weather_data> }} |
| thursday  | Dict of weather data for thursday         | Dict   | {'<time_value>': { <weather_data> }, {'<time_value>': { <weather_data> }} |
| friday    | Dict of weather data for friday           | Dict   | {'<time_value>': { <weather_data> }, {'<time_value>': { <weather_data> }} |
| saturday  | Dict of weather data for saturday         | Dict   | {'<time_value>': { <weather_data> }, {'<time_value>': { <weather_data> }} |
| sunday    | Dict of weather data for sunday           | Dict   | {'<time_value>': { <weather_data> }, {'<time_value>': { <weather_data> }} |

## Note:
If today is Friday the 13th, the returned key `friday` is the key for the next week Friday the 20th.  

**Dict of time_value**

You can retrieve a hourly forecast for the next 48 hours, example:

```yaml
{{ tomorrow['08:00']['temperature'] }}
{{ monday['22:00']['weather_status'] }}

```
Or for the next 7 days a daily forecast.

```yaml
{{ today['daily_forecast']['weather_status'] }}
{{ monday['daily_forecast']['weather_status'] }}

```

| Time values     |
|-----------------|                                                 
|'00:00'          |
|'01:00'          |
|  .              | 
|  .              |
|  .              |
|'22:00'          |
|'23:00'          |
|'daily_forecast' |


**Dict of weather data**

| Name               | Description                                                                              | Type   | Sample               |
|:-------------------|:-----------------------------------------------------------------------------------------|:-------|:---------------------|
| weather_status     | The weather conditions for the given day                                                 | String | heavy intensity rain |
| sunset             | Sunset time (only for daily_forecast and current weather)                                | String | 01:00                |
| sunrise            | Sunrise time (only for daily_forecast and current weather)                               | String | sunrise              |
| temperature        | The expected temperature                                                                 | Int    | 17                   |
| temperature_max    | The expected max. temperature. Only for daily_forecast                                   | Int    | 20                   |
| temperature_min    | The expected min. temperature. Only for daily_forecast                                   | Int    | 11                   |
| pressure           | The expected pressure in hectopascals                                                    | Float  | 857.32               |
| sea_level_pressure | The expected sea level pressure in hpa                                                   | Float  | 627.25               |
| humidity           | The expected humidity in percent                                                         | Float  | 63                   |
| wind_speed         | The expected wind speed in meter/seconds                                                 | Float  | 0.87                 |
| wind_deg           | The expected wind directions in degree                                                   | Float  | 163                  |
| rainfall           | The expected rainfall volume                                                             | Float  | 13.76                |
| snow               | The expected snowfall volume                                                             | Float  | None                 |
| clouds_coverage    | The expected cloud coverage in percent                                                   | Float  | 65                   |


## Note:
It is possible that some data are not available. The value for a key will be None in this case.

## Synapses example

Get the current weather
```yaml
  - name: "get-the-weather"
    signals:
      - order: "what is the weather like"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          temp_unit: "celsius"
          location : "grenoble"
          country: "FR"
          say_template:
          - "Today at {{ location }}, the weather is {{ current['weather_status'] }} with a temperature of {{ current['temperature'] }} degrees and tomorrow the weather will be {{ tomorrow['daily_forecast']['weather_status'] }} with temperatures in the morning from {{ tomorrow['08:00']['temperature'] }}  to  {{ tomorrow['20:00']['temperature'] }} degree in the evening"
```

Load the location from your order
```yaml
  - name: "get-the-weather"
    signals:
      - order: "what is the weather in {{ location }}"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          temp_unit: "celsius"
          location: "{{ location }}"
          say_template:
          - "Today at {{ location }}, the weather is {{ current['weather_status'] }} with a temperature of{{ current['temperature'] }} degrees"
          
```

Forecast example for monday
```yaml
  - name: "weather-forecast-daily"
    signals:
      - order: "How is the weather on Monday"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          location: "grenoble"
          say_template: "The weather on Monday morning will be {{ monday['daily_forecast']['weather_status'] }} with temperatures from  {{ monday['daily_forecast']['temperature_min'] }}  to  {{ monday['daily_forecast']['temperature_max'] }} degree"
```

Forecast example for tomorrow at for specific times
```yaml
  - name: "weather-forecast-daily"
    signals:
      - order: "How will be the weather tomorrow"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          temp_unit: "celsius"
          location : "grenoble"
          country: "FR"
          say_template: "The weather tomorrow starts with {{ tomorrow['08:00']['weather_status'] }} in the morning, you can expect {{ tomorrow['14:00']['weather_status'] }} at the early afternoon and for the evening {{ tomorrow['20:00']['weather_status'] }}"
```

## Templates example 

```
The current weather in {{ location }} is {{ current['weather_status'] }} with a temperature of {{ current['temperature'] }} degrees
```

## Template and synapse example to get the forecast of a specific day with a single synapse

You need to set the day parameter to parse your day to the template. 

```
{% set day_of_week = {
    "your_day_translation": "today",
    "your_day_translation": "tomorrow",
    "your_day_translation": "monday",
    "your_day_translation": "tuesday",
    "your_day_translation": "wednesday", 
    "your_day_translation": "thursday",
    "your_day_translation": "friday",
    "your_day_translation": "saturday", 
    "your_day_translation": "sunday"
    }[day] | default("")
-%}

{% if "today" == day_of_week  %} 
    The weather today will be {{ today['daily_forecast']['weather_status'] }} with temperatures from about {{ today['daily_forecast']['temperature_min'] }} to {{ today['daily_forecast']['temperature_max'] }} degree.

{% elif "tomorrow" == day_of_week  %} 
    The weather tomorrow will be {{ tomorrow['daily_forecast']['weather_status'] }} with temperatures from about {{ tomorrow['daily_forecast']['temperature_min'] }} to {{ tomorrow['daily_forecast']['temperature_max'] }} degree at afternoon
    
{% elif "monday" == day_of_week  %}
    The weather on Monday will be {{ monday['daily_forecast']['weather_status'] }} with temperatures from about {{ monday['daily_forecast']['temperature_min'] }} to {{ monday['daily_forecast']['temperature_max'] }} degree at afternoon
    
{% elif "tuesday" == day_of_week  %}
      The weather on Tuesday will be {{ tuesday['daily_forecast']['weather_status'] }} with temperatures from about {{ tuesday['daily_forecast']['temperature_min'] }} to {{ tuesday['daily_forecast']['temperature_max'] }} degree at afternoon

{% elif "wednesday" == day_of_week  %}
      The weather on Wednesday will be {{ wednesday['daily_forecast']['weather_status'] }} with temperatures from about {{ wednesday['daily_forecast']['temperature_min'] }} to {{ wednesday['daily_forecast']['temperature_max'] }} degree at afternoon
    
{% elif "thursday" == day_of_week %}
      The weather on Thursday will be {{ thursday['daily_forecast']['weather_status'] }} with temperatures from about {{ thursday['daily_forecast']['temperature_min'] }} to {{ thursday['daily_forecast']['temperature_max'] }} degree at afternoon

{% elif "friday" == day_of_week  %}
      The weather on Friday will be {{ friday['daily_forecast']['weather_status'] }} with temperatures from about {{ friday['daily_forecast']['temperature_min'] }} to {{ friday['daily_forecast']['temperature_max'] }} degree at afternoon

{% elif "saturday" == day_of_week  %}
      The weather on Saturday will be {{ saturday['daily_forecast']['weather_status'] }} with temperatures from about {{ saturday['daily_forecast']['temperature_min'] }} to {{ saturday['daily_forecast']['temperature_max'] }} degree at afternoon
    
{% elif "sunday" == day_of_week  %} 
    The weather on Sunday will be {{ sunday['daily_forecast']['weather_status'] }} with temperatures from about {{ sunday['daily_forecast']['temperature_min'] }} to {{ sunday['daily_forecast']['temperature_max'] }} degree at afternoon.

{% endif %}
```

Example of translation for french
```
{% set day_of_week = {
    "aujourd'hui": "today",
    "lundi": "monday",
    "mardi": "tuesday",
    "mercredi": "wednesday", 
    "jeudi": "thursday",
    "vendredi": "friday",
    "samedi": "saturday", 
    "dimanche": "sunday"
    }[day] | default("")
-%}
```

Example for a single synapse
```yaml
  - name: "wetter-forecast-daily"
    signals:
      - order: "what is the weather on {{ day }}"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          country: "FR"
          location: "Grenoble"
          day: "{{ day }}"
          file_template: "templates/daily_weather.j2" 
          
```
or for each day
```yaml
  - name: "wetter-forecast-daily"
    signals:
      - order: "what is the weather on Monday"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          country: "FR"
          location: "Grenoble"
          day: "monday"
          file_template: "templates/daily_weather.j2" 
          
```

Example template to get the wind speed and the direction.
Change the wind directions into your desire language.

```
{% if current['wind_deg'] <= 348 or current['wind_deg'] > 348 %}
    {% if current['wind_deg'] >= 348 %}
        {% set direction = "North" %}  
    {% elif current['wind_deg'] < 11 %}
        {% set direction = "North" %} 
    {% endif %}
{% endif %} 
 
{% if current['wind_deg'] >= 11 and current['wind_deg'] < 33 %}
    {% set direction = "North northeast" %}
{% elif current['wind_deg'] >= 33 and current['wind_deg'] < 56 %}
    {% set direction = "Northeast" %}    
{% elif current['wind_deg'] >= 56 and current['wind_deg'] < 78 %}
    {% set direction = "East northeast" %}  
{% elif current['wind_deg'] >= 78 and current['wind_deg'] < 101 %}
    {% set direction = "East" %}    
{% elif current['wind_deg'] >= 101 and current['wind_deg'] < 123 %}
    {% set direction = "East southeast" %} 
{% elif current['wind_deg'] >= 123 and current['wind_deg'] < 146 %}
    {% set direction = "Southeast" %}
{% elif current['wind_deg'] >= 146 and current['wind_deg'] < 168 %}
    {% set direction = "South southeast" %}
{% elif current['wind_deg'] >= 168 and current['wind_deg'] < 191 %}
    {% set direction = "South" %} 
{% elif current['wind_deg'] >= 191 and current['wind_deg'] < 213 %}
    {% set direction = "South southwest" %}
{% elif current['wind_deg'] >= 213 and current['wind_deg'] < 236 %}
    {% set direction = "Southwest" %}
{% elif current['wind_deg'] >= 236 and current['wind_deg'] < 258 %}
    {% set direction = "West Southwest" %}
{% elif current['wind_deg'] >= 258 and current['wind_deg'] < 281 %}
    {% set direction = "West" %}
{% elif current['wind_deg'] >= 281 and current['wind_deg'] < 303 %}
    {% set direction = "West northwest" %}
{% elif current['wind_deg'] >= 303 and current['wind_deg'] < 326 %}
    {% set direction = "Northwest" %} 
{% elif current['wind_deg'] >= 326 and current['wind_deg'] < 348 %}
    {% set direction = "North northwest" %}
{% endif %}

{% if current['wind_speed'] %}
      The current wind speed is about {{ current['wind_speed']|round|int }} kilometer per hour and comes from direction {{ direction }}

{% endif %}
```

Example synapse for wind speed
```yaml
  - name: "weather-windspeed"
    signals:
      - order: "what is the current wind speed and direction"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          country: "FR"
          location: "Grenoble"
          speed_unit: "km_hour"
          file_template: "templates/weather_wind.j2"
```

## Example of returned dict with all data that can be then used in the template

```json
{
    "location": "Paris",
    "latitude": 48.853401,
    "longitude": 2.3486,
    "current": {
        "weather_status": "broken clouds",
        "sunset": "21:31",
        "sunrise": "06:02",
        "temperature": 17,
        "temperature_min": null,
        "temperature_max": null,
        "pressure": 1017,
        "sea_level_pressure": null,
        "humidity": 58,
        "wind_deg": 98,
        "wind_speed": 4.02,
        "snow": null,
        "rainfall": null,
        "clouds_coverage": 75
    },
    "today": {
        "15:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 17,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1017,
            "sea_level_pressure": null,
            "humidity": 56,
            "wind_deg": 206,
            "wind_speed": 5.77,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 80
        },
        "16:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 17,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1017,
            "sea_level_pressure": null,
            "humidity": 58,
            "wind_deg": 207,
            "wind_speed": 5.19,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 75
        },
        "17:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 17,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1017,
            "sea_level_pressure": null,
            "humidity": 57,
            "wind_deg": 205,
            "wind_speed": 5.3,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 80
        },
        "18:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 17,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1017,
            "sea_level_pressure": null,
            "humidity": 56,
            "wind_deg": 208,
            "wind_speed": 5.82,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 85
        },
        "19:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 17,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1016,
            "sea_level_pressure": null,
            "humidity": 58,
            "wind_deg": 207,
            "wind_speed": 6.01,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 90
        },
        "20:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 16,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1015,
            "sea_level_pressure": null,
            "humidity": 60,
            "wind_deg": 209,
            "wind_speed": 5.96,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 95
        },
        "21:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 15,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1014,
            "sea_level_pressure": null,
            "humidity": 63,
            "wind_deg": 206,
            "wind_speed": 5.8,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "22:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 14,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1014,
            "sea_level_pressure": null,
            "humidity": 63,
            "wind_deg": 210,
            "wind_speed": 5.66,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "23:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 14,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1014,
            "sea_level_pressure": null,
            "humidity": 60,
            "wind_deg": 213,
            "wind_speed": 5.86,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "daily_forecast": {
            "weather_status": "overcast clouds",
            "sunset": "21:31",
            "sunrise": "06:02",
            "temperature": 16,
            "temperature_min": 6,
            "temperature_max": 17,
            "pressure": 1019,
            "sea_level_pressure": null,
            "humidity": 53,
            "wind_deg": 207,
            "wind_speed": 6.01,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 90
        }
    },
    "friday": {
        "00:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 13,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1013,
            "sea_level_pressure": null,
            "humidity": 58,
            "wind_deg": 216,
            "wind_speed": 5.86,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "01:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 13,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1013,
            "sea_level_pressure": null,
            "humidity": 60,
            "wind_deg": 216,
            "wind_speed": 5.76,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "02:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1012,
            "sea_level_pressure": null,
            "humidity": 67,
            "wind_deg": 223,
            "wind_speed": 5.83,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "03:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1011,
            "sea_level_pressure": null,
            "humidity": 72,
            "wind_deg": 226,
            "wind_speed": 5.82,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "04:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1011,
            "sea_level_pressure": null,
            "humidity": 71,
            "wind_deg": 228,
            "wind_speed": 5.54,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "05:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 11,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 75,
            "wind_deg": 232,
            "wind_speed": 5.7,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "06:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 10,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 81,
            "wind_deg": 232,
            "wind_speed": 5.66,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "07:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 10,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 79,
            "wind_deg": 232,
            "wind_speed": 5.97,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "08:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 11,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 69,
            "wind_deg": 233,
            "wind_speed": 6.61,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "09:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 65,
            "wind_deg": 232,
            "wind_speed": 6.69,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 96
        },
        "10:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 13,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 61,
            "wind_deg": 231,
            "wind_speed": 7.07,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 82
        },
        "11:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 14,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 55,
            "wind_deg": 231,
            "wind_speed": 7.32,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 78
        },
        "12:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 15,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 49,
            "wind_deg": 234,
            "wind_speed": 7.67,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 83
        },
        "13:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 16,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 45,
            "wind_deg": 232,
            "wind_speed": 7.98,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 80
        },
        "14:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 17,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1008,
            "sea_level_pressure": null,
            "humidity": 42,
            "wind_deg": 233,
            "wind_speed": 8.14,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 76
        },
        "15:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 15,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1008,
            "sea_level_pressure": null,
            "humidity": 55,
            "wind_deg": 228,
            "wind_speed": 7.31,
            "snow": null,
            "rainfall": 0.15,
            "clouds_coverage": 98
        },
        "16:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 16,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 50,
            "wind_deg": 235,
            "wind_speed": 8.09,
            "snow": null,
            "rainfall": 0.22,
            "clouds_coverage": 85
        },
        "17:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 16,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 54,
            "wind_deg": 236,
            "wind_speed": 7.87,
            "snow": null,
            "rainfall": 0.25,
            "clouds_coverage": 66
        },
        "18:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 16,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1006,
            "sea_level_pressure": null,
            "humidity": 57,
            "wind_deg": 238,
            "wind_speed": 7.48,
            "snow": null,
            "rainfall": 0.23,
            "clouds_coverage": 54
        },
        "19:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 15,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1006,
            "sea_level_pressure": null,
            "humidity": 57,
            "wind_deg": 236,
            "wind_speed": 7.46,
            "snow": null,
            "rainfall": 0.12,
            "clouds_coverage": 45
        },
        "20:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 14,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1006,
            "sea_level_pressure": null,
            "humidity": 59,
            "wind_deg": 236,
            "wind_speed": 7.23,
            "snow": null,
            "rainfall": 0.1,
            "clouds_coverage": 38
        },
        "21:00": {
            "weather_status": "clear sky",
            "sunset": null,
            "sunrise": null,
            "temperature": 13,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1006,
            "sea_level_pressure": null,
            "humidity": 59,
            "wind_deg": 237,
            "wind_speed": 6.87,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 1
        },
        "22:00": {
            "weather_status": "clear sky",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 59,
            "wind_deg": 236,
            "wind_speed": 6.75,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 1
        },
        "23:00": {
            "weather_status": "clear sky",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 61,
            "wind_deg": 232,
            "wind_speed": 6.93,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 2
        },
        "daily_forecast": {
            "weather_status": "light rain",
            "sunset": "21:33",
            "sunrise": "06:01",
            "temperature": 16,
            "temperature_min": 10,
            "temperature_max": 17,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 45,
            "wind_deg": 233,
            "wind_speed": 8.14,
            "snow": null,
            "rainfall": 1.07,
            "clouds_coverage": 80
        }
    },
    "saturday": {
        "00:00": {
            "weather_status": "clear sky",
            "sunset": null,
            "sunrise": null,
            "temperature": 11,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 64,
            "wind_deg": 229,
            "wind_speed": 7.02,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 1
        },
        "01:00": {
            "weather_status": "clear sky",
            "sunset": null,
            "sunrise": null,
            "temperature": 10,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 69,
            "wind_deg": 228,
            "wind_speed": 7.12,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 1
        },
        "02:00": {
            "weather_status": "clear sky",
            "sunset": null,
            "sunrise": null,
            "temperature": 10,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 75,
            "wind_deg": 228,
            "wind_speed": 7.04,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 1
        },
        "03:00": {
            "weather_status": "clear sky",
            "sunset": null,
            "sunrise": null,
            "temperature": 9,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 77,
            "wind_deg": 226,
            "wind_speed": 6.96,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 9
        },
        "04:00": {
            "weather_status": "few clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 9,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 78,
            "wind_deg": 227,
            "wind_speed": 6.74,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 14
        },
        "05:00": {
            "weather_status": "few clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 9,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 80,
            "wind_deg": 226,
            "wind_speed": 6.68,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 24
        },
        "06:00": {
            "weather_status": "scattered clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 9,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 79,
            "wind_deg": 226,
            "wind_speed": 6.64,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 38
        },
        "07:00": {
            "weather_status": "scattered clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 9,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1008,
            "sea_level_pressure": null,
            "humidity": 78,
            "wind_deg": 224,
            "wind_speed": 6.37,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 49
        },
        "08:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 9,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 76,
            "wind_deg": 224,
            "wind_speed": 6.29,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 57
        },
        "09:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 11,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 71,
            "wind_deg": 222,
            "wind_speed": 6.58,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 69
        },
        "10:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 60,
            "wind_deg": 229,
            "wind_speed": 7.39,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 53
        },
        "11:00": {
            "weather_status": "scattered clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 14,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 50,
            "wind_deg": 234,
            "wind_speed": 7.59,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 38
        },
        "12:00": {
            "weather_status": "scattered clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 15,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 44,
            "wind_deg": 235,
            "wind_speed": 7.76,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 32
        },
        "13:00": {
            "weather_status": "scattered clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 15,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 47,
            "wind_deg": 242,
            "wind_speed": 7.3,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 34
        },
        "14:00": {
            "weather_status": "scattered clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 15,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 47,
            "wind_deg": 245,
            "wind_speed": 6.78,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 39
        },
        "daily_forecast": {
            "weather_status": "light rain",
            "sunset": "21:34",
            "sunrise": "06:00",
            "temperature": 15,
            "temperature_min": 9,
            "temperature_max": 18,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 47,
            "wind_deg": 235,
            "wind_speed": 7.76,
            "snow": null,
            "rainfall": 2.53,
            "clouds_coverage": 34
        }
    },
    "sunday": {
        "daily_forecast": {
            "weather_status": "scattered clouds",
            "sunset": "21:35",
            "sunrise": "05:59",
            "temperature": 16,
            "temperature_min": 7,
            "temperature_max": 16,
            "pressure": 1016,
            "sea_level_pressure": null,
            "humidity": 43,
            "wind_deg": 217,
            "wind_speed": 6.46,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 48
        }
    },
    "monday": {
        "daily_forecast": {
            "weather_status": "light rain",
            "sunset": "21:36",
            "sunrise": "05:58",
            "temperature": 16,
            "temperature_min": 10,
            "temperature_max": 16,
            "pressure": 1013,
            "sea_level_pressure": null,
            "humidity": 63,
            "wind_deg": 209,
            "wind_speed": 6.28,
            "snow": null,
            "rainfall": 6.04,
            "clouds_coverage": 99
        }
    },
    "tuesday": {
        "daily_forecast": {
            "weather_status": "light rain",
            "sunset": "21:37",
            "sunrise": "05:57",
            "temperature": 14,
            "temperature_min": 7,
            "temperature_max": 16,
            "pressure": 1020,
            "sea_level_pressure": null,
            "humidity": 72,
            "wind_deg": 297,
            "wind_speed": 5.24,
            "snow": null,
            "rainfall": 2.94,
            "clouds_coverage": 80
        }
    },
    "wednesday": {
        "daily_forecast": {
            "weather_status": "light rain",
            "sunset": "21:39",
            "sunrise": "05:56",
            "temperature": 16,
            "temperature_min": 7,
            "temperature_max": 17,
            "pressure": 1025,
            "sea_level_pressure": null,
            "humidity": 45,
            "wind_deg": 324,
            "wind_speed": 5.09,
            "snow": null,
            "rainfall": 0.26,
            "clouds_coverage": 27
        }
    },
    "thursday": {
        "daily_forecast": {
            "weather_status": "scattered clouds",
            "sunset": "21:40",
            "sunrise": "05:55",
            "temperature": 18,
            "temperature_min": 10,
            "temperature_max": 18,
            "pressure": 1024,
            "sea_level_pressure": null,
            "humidity": 43,
            "wind_deg": 6,
            "wind_speed": 3.29,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 48
        }
    },
    "tomorrow": {
        "00:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 13,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1013,
            "sea_level_pressure": null,
            "humidity": 58,
            "wind_deg": 216,
            "wind_speed": 5.86,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "01:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 13,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1013,
            "sea_level_pressure": null,
            "humidity": 60,
            "wind_deg": 216,
            "wind_speed": 5.76,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "02:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1012,
            "sea_level_pressure": null,
            "humidity": 67,
            "wind_deg": 223,
            "wind_speed": 5.83,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "03:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1011,
            "sea_level_pressure": null,
            "humidity": 72,
            "wind_deg": 226,
            "wind_speed": 5.82,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "04:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1011,
            "sea_level_pressure": null,
            "humidity": 71,
            "wind_deg": 228,
            "wind_speed": 5.54,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "05:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 11,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 75,
            "wind_deg": 232,
            "wind_speed": 5.7,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "06:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 10,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 81,
            "wind_deg": 232,
            "wind_speed": 5.66,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "07:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 10,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 79,
            "wind_deg": 232,
            "wind_speed": 5.97,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "08:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 11,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 69,
            "wind_deg": 233,
            "wind_speed": 6.61,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 100
        },
        "09:00": {
            "weather_status": "overcast clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 65,
            "wind_deg": 232,
            "wind_speed": 6.69,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 96
        },
        "10:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 13,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1010,
            "sea_level_pressure": null,
            "humidity": 61,
            "wind_deg": 231,
            "wind_speed": 7.07,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 82
        },
        "11:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 14,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 55,
            "wind_deg": 231,
            "wind_speed": 7.32,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 78
        },
        "12:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 15,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 49,
            "wind_deg": 234,
            "wind_speed": 7.67,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 83
        },
        "13:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 16,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 45,
            "wind_deg": 232,
            "wind_speed": 7.98,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 80
        },
        "14:00": {
            "weather_status": "broken clouds",
            "sunset": null,
            "sunrise": null,
            "temperature": 17,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1008,
            "sea_level_pressure": null,
            "humidity": 42,
            "wind_deg": 233,
            "wind_speed": 8.14,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 76
        },
        "15:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 15,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1008,
            "sea_level_pressure": null,
            "humidity": 55,
            "wind_deg": 228,
            "wind_speed": 7.31,
            "snow": null,
            "rainfall": 0.15,
            "clouds_coverage": 98
        },
        "16:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 16,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 50,
            "wind_deg": 235,
            "wind_speed": 8.09,
            "snow": null,
            "rainfall": 0.22,
            "clouds_coverage": 85
        },
        "17:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 16,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 54,
            "wind_deg": 236,
            "wind_speed": 7.87,
            "snow": null,
            "rainfall": 0.25,
            "clouds_coverage": 66
        },
        "18:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 16,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1006,
            "sea_level_pressure": null,
            "humidity": 57,
            "wind_deg": 238,
            "wind_speed": 7.48,
            "snow": null,
            "rainfall": 0.23,
            "clouds_coverage": 54
        },
        "19:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 15,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1006,
            "sea_level_pressure": null,
            "humidity": 57,
            "wind_deg": 236,
            "wind_speed": 7.46,
            "snow": null,
            "rainfall": 0.12,
            "clouds_coverage": 45
        },
        "20:00": {
            "weather_status": "light rain",
            "sunset": null,
            "sunrise": null,
            "temperature": 14,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1006,
            "sea_level_pressure": null,
            "humidity": 59,
            "wind_deg": 236,
            "wind_speed": 7.23,
            "snow": null,
            "rainfall": 0.1,
            "clouds_coverage": 38
        },
        "21:00": {
            "weather_status": "clear sky",
            "sunset": null,
            "sunrise": null,
            "temperature": 13,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1006,
            "sea_level_pressure": null,
            "humidity": 59,
            "wind_deg": 237,
            "wind_speed": 6.87,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 1
        },
        "22:00": {
            "weather_status": "clear sky",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 59,
            "wind_deg": 236,
            "wind_speed": 6.75,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 1
        },
        "23:00": {
            "weather_status": "clear sky",
            "sunset": null,
            "sunrise": null,
            "temperature": 12,
            "temperature_min": null,
            "temperature_max": null,
            "pressure": 1007,
            "sea_level_pressure": null,
            "humidity": 61,
            "wind_deg": 232,
            "wind_speed": 6.93,
            "snow": null,
            "rainfall": null,
            "clouds_coverage": 2
        },
        "daily_forecast": {
            "weather_status": "light rain",
            "sunset": "21:33",
            "sunrise": "06:01",
            "temperature": 16,
            "temperature_min": 10,
            "temperature_max": 17,
            "pressure": 1009,
            "sea_level_pressure": null,
            "humidity": 45,
            "wind_deg": 233,
            "wind_speed": 8.14,
            "snow": null,
            "rainfall": 1.07,
            "clouds_coverage": 80
        }
    }
}
```

## License

Copyright (c) 2016. All rights reserved.

Kalliope is covered by the MIT license, a permissive free software license that lets you do anything you want with the source code, 
as long as you provide back attribution and ["don't hold you liable"](http://choosealicense.com/). For the full license text see the [LICENSE.md](LICENSE.md) file.
