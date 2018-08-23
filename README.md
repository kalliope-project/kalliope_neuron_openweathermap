# OpenWeatherMap API

## Synopsis 

Give the today, tomorrow weather or a forecast for 5 days at a specific day of the week with the related data (humidity, temperature, etc ...) for a given location. 

## Installation
```
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_openweathermap.git
```

## Options

| parameter  | required | default | choices                     | comment                                                                                                  |
| ---------- | -------- | ------- | --------------------------- | -------------------------------------------------------------------------------------------------------- |
| api_key    | YES      | None    |                             | User API key of the OWM API get one [here](https://home.openweathermap.org/users/sign_up)                |
| location   | YES      | None    |                             | The location                                                                                             |
| lang       | No       | en      |                             | Look for the supported languages [here](https://openweathermap.org/current#multi)                        |
| temp_unit  | No       | celsius | celsius, kelvin, fahrenheit |                                                                                                          |
| country    | No       | None    |                             | [ISO-3166 Country Code](https://en.wikipedia.org)                                                        |
| 12h_format | no       | False   | True/False                  | To get 12 hour format for sunrise and sunset return value                                                |
| day        | No       | None    | today or a weekday          | Only needed if you want a single synapse to catch the day and translate it in a file_template (required) |


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

**Dict of time_value**

| Time values |
|-------------|                                                 
|'02:00'      |
|'05:00'      |
|'08:00'      |
|'11:00'      |
|'14:00'      |
|'17:00'      |
|'20:00'      |
|'23:00'      |


**Dict of weather data**

| Name            | Description                               | Type   | Sample               |
| --------------- | ----------------------------------------- | ------ | -------------------- |
| weather_status  | The weather conditions for the given day  | String | heavy intensity rain |
| temperature     | The expected temperature (only current)   | Int    | 17                   |
| temperature_max | The expected max. temperature for 3 hours | Int    | 20                   |
| temperature_min | The expected min. temperature for 3 hours | Int    | 11                   |
| humidity        | The expected humidity in percent          | Float  | 63                   |
| wind_speed      | The expected wind speed in meter/seconds  | Float  | 0.87                 |
| wind_deg        | The expected wind directions in degree    | Float  | 163                  |
| pressure        | The expected pressure in hectopascals     | Float  | 857.32               |
| sea_level       | The expected sea level pressure in hpa    | Float  | 627.25               |
| rainfall        | The expected rainfall volume              | Float  | 13.76                |
| snowfall        | The expected snowfall volume              | Float  | None                 |
| clouds_coverage | The expected cloud coverage in percent    | Float  | 65                   |


## Note:
It is possible that some data are not available. The value for a key will be None in this case.


## Synapses example

Get the current weather
```yaml
  - name: "get-the-weather"
    signals:
      - order: "what weather is it"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          temp_unit: "celsius"
          location : "grenoble"
          country: "FR"
          say_template:
          - "Today at {{ location }}, the weather is {{ current['weather_status'] }} with a temperature of{{ current['temperature'] }} degrees and tomorrow the weather will be {{ tomorrow['11:00']['weather_status'] }} with temperatures in the morning from {{ tomorrow['08:00']['temperature'] }}  to  {{ tomorrow['20:00']['temperature'] }} degree in the evening"
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
      - order: "How is the weather on Monday morning"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          location: "grenoble"
          say_template: "The weather on Monday morning will be {{ monday['08:00']['weather_status'] }} with temperatures from  {{ monday['08:00']['temperature'] }}  to  {{ monday['14:00']['temperature'] }} degree at afternoon"
```

Forecast example for today at a given location
```yaml
  - name: "weather-forecast-daily"
    signals:
      - order: "How will be the weather today"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          temp_unit: "celsius"
          location : "grenoble"
          country: "FR"
          say_template: "The weather today starts today with {{ today['08:00']['weather_status'] }} and {{ today['11:00']['weather_status'] }} at noon for the evening you can expect {{ today['20:00']['weather_status'] }}"
```

## Templates example 

```
The current weather in {{ location }} is {{ current['weather_status'] }} with a temperature of {{ current['temperature'] }} degrees
```

## Template and synapse example to get the forecast of a specific day with a single synapse

We only get a forecast for 5 days, so if you ask for a day which is not in range it returns None data, for this case you can use a file template. 
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
    The weather today in the morning will be {{ today['08:00']['weather_status'] }} with temperatures from about {{ today['08:00']['temp'] }} to {{ today['14:00']['temp'] }} degree at afternoon

{% elif "tomorrow" == day_of_week  %} 
    The weather tomorrow will be {{ tomorrow['08:00']['weather_status'] }} with temperatures from about {{ tomorrow['08:00']['temp'] }} to {{ tomorrow['14:00']['temp'] }} degree at afternoon

    
{% elif "monday" == day_of_week  %}
    {% if monday['weather_status'] %}
        The weather on Monday will be {{ monday['08:00']['weather_status'] }} with temperatures from about {{ monday['08:00']['temp'] }} to {{ monday['14:00']['temp'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for monday
    {% endif %}
    
{% elif "tuesday" == day_of_week  %}
    {% if tuesday['weather_status'] %} 
        The weather on Tuesday will be {{ tuesday['08:00']['weather_status'] }} with temperatures from about {{ tuesday['08:00']['temp'] }} to {{ tuesday['14:00']['temp'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for tuesday
    {% endif %}
    
{% elif "wednesday" == day_of_week  %}
    {% if wednesday['weather_status'] %}
        The weather on Wednesday will be {{ wednesday['08:00']['weather_status'] }} with temperatures from about {{ wednesday['08:00']['temp'] }} to {{ wednesday['14:00']['temp'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for wednesday
    {% endif %}
    
{% elif "thursday" == day_of_week %}
    {% if thursday['weather_status'] %}
        The weather on Thursday will be {{ thursday['08:00']['weather_status'] }} with temperatures from about {{ thursday['08:00']['temp'] }} to {{ thursday['14:00']['temp'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for thursday
    {% endif %}
    
{% elif "friday" == day_of_week  %}
    {% if friday['weather_status'] %}
        The weather on Friday will be {{ friday['08:00']['weather_status'] }} with temperatures from about {{ friday['08:00']['temp'] }} to {{ friday['14:00']['temp'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for friday
    {% endif %}
    
{% elif "saturday" == day_of_week  %}
    {% if saturday['weather_status'] %}
        The weather on Saturday will be {{ saturday['08:00']['weather_status'] }} with temperatures from about {{ saturday['08:00']['temp'] }} to {{ saturday['14:00']['temp'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for saturday
    {% endif %}
    
{% elif "sunday" == day_of_week  %}
    {% if sunday['weather_status'] %} 
        The weather on Sunday will be {{ sunday['weather_status'] }} with temperatures from {{ sunday['min_temp'] }} to {{ sunday['max_temp'] }} degree
    {% else %} 
        I'm sorry, there is no forecast for sunday
    {% endif %}

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

Example template to get the wind speed and the direction, default the wind speed is in meters per second we convert it to kilometre per hour by multiply it by 3.6. 
For miles per hour, multiply it by 2.2369.
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
    {% set converted_windspeed = current['wind_speed'] * 3.6 %}
        The current wind speed is about {{ converted_windspeed|round|int }} kilometre per hour and comes from direction {{ direction }}

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
          file_template: "templates/weather_wind.j2"
```

## Example of returned dict with all data that can be then used in the template

```
{'current': {'clouds_coverage': 0,
             'humidity': 33,
             'pressure': 1014,
             'rainfall': None,
             'sea_level_pressure': None,
             'snow': None,
             'sunrise': '06:48',
             'sunset': '20:29',
             'temperature ': 31,
             'temperature_max ': 31,
             'temperature_min ': 31,
             'weather_status': u'ciel d\xe9gag\xe9',
             'wind_deg': 230,
             'wind_speed': 2.6},
 'friday': {'02:00': {'clouds_coverage': 24,
                      'humidity': 68,
                      'pressure': 855.16,
                      'rainfall': None,
                      'sea_level_pressure': 1029.39,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 16,
                      'temperature_max ': 16,
                      'temperature_min ': 14,
                      'weather_status': u'peu nuageux',
                      'wind_deg': 16.5021,
                      'wind_speed': 0.6},
            '05:00': {'clouds_coverage': 12,
                      'humidity': 81,
                      'pressure': 854.45,
                      'rainfall': None,
                      'sea_level_pressure': 1029.04,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 12,
                      'temperature_max ': 12,
                      'temperature_min ': 12,
                      'weather_status': u'peu nuageux',
                      'wind_deg': 25.0013,
                      'wind_speed': 0.56},
            '08:00': {'clouds_coverage': 20,
                      'humidity': 84,
                      'pressure': 854.27,
                      'rainfall': None,
                      'sea_level_pressure': 1029.14,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 12,
                      'temperature_max ': 12,
                      'temperature_min ': 12,
                      'weather_status': u'peu nuageux',
                      'wind_deg': 33.0019,
                      'wind_speed': 0.56},
            '11:00': {'clouds_coverage': 12,
                      'humidity': 64,
                      'pressure': 854.14,
                      'rainfall': None,
                      'sea_level_pressure': 1028.59,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 17,
                      'temperature_max ': 17,
                      'temperature_min ': 17,
                      'weather_status': u'peu nuageux',
                      'wind_deg': 336.502,
                      'wind_speed': 0.77},
            '14:00': {'clouds_coverage': 20,
                      'humidity': 52,
                      'pressure': 853.24,
                      'rainfall': None,
                      'sea_level_pressure': 1027.17,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 19,
                      'temperature_max ': 19,
                      'temperature_min ': 19,
                      'weather_status': u'peu nuageux',
                      'wind_deg': 325.001,
                      'wind_speed': 0.78},
            '17:00': {'clouds_coverage': 24,
                      'humidity': 49,
                      'pressure': 852.46,
                      'rainfall': None,
                      'sea_level_pressure': 1026.26,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 19,
                      'temperature_max ': 19,
                      'temperature_min ': 19,
                      'weather_status': u'peu nuageux',
                      'wind_deg': 319.501,
                      'wind_speed': 0.78},
            '20:00': {'clouds_coverage': 24,
                      'humidity': 58,
                      'pressure': 852.74,
                      'rainfall': None,
                      'sea_level_pressure': 1026.89,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 15,
                      'temperature_max ': 15,
                      'temperature_min ': 15,
                      'weather_status': u'l\xe9g\xe8re pluie',
                      'wind_deg': 323.501,
                      'wind_speed': 0.76},
            '23:00': {'clouds_coverage': 8,
                      'humidity': 74,
                      'pressure': 853.34,
                      'rainfall': None,
                      'sea_level_pressure': 1028.21,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 12,
                      'temperature_max ': 12,
                      'temperature_min ': 12,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 340.501,
                      'wind_speed': 0.71}},
 'latitude': 45.18,
 'location': u'Grenoble',
 'longitude': 5.73,
 'monday': {'02:00': {'clouds_coverage': 0,
                      'humidity': 69,
                      'pressure': 852.75,
                      'rainfall': None,
                      'sea_level_pressure': 1030.13,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 6,
                      'temperature_max ': 6,
                      'temperature_min ': 6,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 50.0001,
                      'wind_speed': 0.71},
            '05:00': {'clouds_coverage': 0,
                      'humidity': 68,
                      'pressure': 853.11,
                      'rainfall': None,
                      'sea_level_pressure': 1030.76,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 5,
                      'temperature_max ': 5,
                      'temperature_min ': 5,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 68.0047,
                      'wind_speed': 0.65},
            '08:00': {'clouds_coverage': 0,
                      'humidity': 59,
                      'pressure': 853.57,
                      'rainfall': None,
                      'sea_level_pressure': 1031.46,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 6,
                      'temperature_max ': 6,
                      'temperature_min ': 6,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 60.5016,
                      'wind_speed': 0.67},
            '11:00': {'clouds_coverage': 0,
                      'humidity': 33,
                      'pressure': 854.54,
                      'rainfall': None,
                      'sea_level_pressure': 1030.52,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 16,
                      'temperature_max ': 16,
                      'temperature_min ': 16,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 341.5,
                      'wind_speed': 0.76},
            '14:00': {'clouds_coverage': 0,
                      'humidity': 27,
                      'pressure': 854.94,
                      'rainfall': None,
                      'sea_level_pressure': 1029.53,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 20,
                      'temperature_max ': 20,
                      'temperature_min ': 20,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 312.503,
                      'wind_speed': 0.71},
            '17:00': {'clouds_coverage': 0,
                      'humidity': 30,
                      'pressure': 855.13,
                      'rainfall': None,
                      'sea_level_pressure': 1028.99,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 21,
                      'temperature_max ': 21,
                      'temperature_min ': 21,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 311.502,
                      'wind_speed': 0.71},
            '20:00': {'clouds_coverage': 0,
                      'humidity': 37,
                      'pressure': 855.66,
                      'rainfall': None,
                      'sea_level_pressure': 1029.87,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 18,
                      'temperature_max ': 18,
                      'temperature_min ': 18,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 320.002,
                      'wind_speed': 0.65},
            '23:00': {'clouds_coverage': 0,
                      'humidity': 60,
                      'pressure': 856.69,
                      'rainfall': None,
                      'sea_level_pressure': 1031.88,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 12,
                      'temperature_max ': 12,
                      'temperature_min ': 12,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 13.5007,
                      'wind_speed': 0.71}},
 'saturday': {'02:00': {'clouds_coverage': 44,
                        'humidity': 92,
                        'pressure': 852.96,
                        'rainfall': None,
                        'sea_level_pressure': 1028.41,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 9,
                        'temperature_max ': 9,
                        'temperature_min ': 9,
                        'weather_status': u'partiellement nuageux',
                        'wind_deg': 4.50247,
                        'wind_speed': 0.66},
              '05:00': {'clouds_coverage': 32,
                        'humidity': 98,
                        'pressure': 852.02,
                        'rainfall': None,
                        'sea_level_pressure': 1027.9,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 8,
                        'temperature_max ': 8,
                        'temperature_min ': 8,
                        'weather_status': u'partiellement nuageux',
                        'wind_deg': 19.5016,
                        'wind_speed': 0.67},
              '08:00': {'clouds_coverage': 36,
                        'humidity': 97,
                        'pressure': 851.28,
                        'rainfall': None,
                        'sea_level_pressure': 1027.37,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 8,
                        'temperature_max ': 8,
                        'temperature_min ': 8,
                        'weather_status': u'partiellement nuageux',
                        'wind_deg': 45.5101,
                        'wind_speed': 0.76},
              '11:00': {'clouds_coverage': 44,
                        'humidity': 58,
                        'pressure': 850.62,
                        'rainfall': None,
                        'sea_level_pressure': 1025.74,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 14,
                        'temperature_max ': 14,
                        'temperature_min ': 14,
                        'weather_status': u'partiellement nuageux',
                        'wind_deg': 347.004,
                        'wind_speed': 0.77},
              '14:00': {'clouds_coverage': 92,
                        'humidity': 46,
                        'pressure': 849.68,
                        'rainfall': None,
                        'sea_level_pressure': 1024.13,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 16,
                        'temperature_max ': 16,
                        'temperature_min ': 16,
                        'weather_status': u'couvert',
                        'wind_deg': 312.503,
                        'wind_speed': 0.77},
              '17:00': {'clouds_coverage': 92,
                        'humidity': 65,
                        'pressure': 849.36,
                        'rainfall': None,
                        'sea_level_pressure': 1024.38,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 12,
                        'temperature_max ': 12,
                        'temperature_min ': 12,
                        'weather_status': u'l\xe9g\xe8re pluie',
                        'wind_deg': 284.502,
                        'wind_speed': 0.72},
              '20:00': {'clouds_coverage': 80,
                        'humidity': 84,
                        'pressure': 848.98,
                        'rainfall': None,
                        'sea_level_pressure': 1025.04,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 9,
                        'temperature_max ': 9,
                        'temperature_min ': 9,
                        'weather_status': u'l\xe9g\xe8re pluie',
                        'wind_deg': 322.001,
                        'wind_speed': 0.71},
              '23:00': {'clouds_coverage': 68,
                        'humidity': 93,
                        'pressure': 849.09,
                        'rainfall': None,
                        'sea_level_pressure': 1026.19,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 7,
                        'temperature_max ': 7,
                        'temperature_min ': 7,
                        'weather_status': u'l\xe9g\xe8re pluie',
                        'wind_deg': 315.005,
                        'wind_speed': 0.66}},
 'sunday': {'02:00': {'clouds_coverage': 92,
                      'humidity': 98,
                      'pressure': 848.9,
                      'rainfall': None,
                      'sea_level_pressure': 1026.45,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 6,
                      'temperature_max ': 6,
                      'temperature_min ': 6,
                      'weather_status': u'l\xe9g\xe8re pluie',
                      'wind_deg': 314.002,
                      'wind_speed': 0.73},
            '05:00': {'clouds_coverage': 44,
                      'humidity': 96,
                      'pressure': 848.47,
                      'rainfall': None,
                      'sea_level_pressure': 1026.36,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 5,
                      'temperature_max ': 5,
                      'temperature_min ': 5,
                      'weather_status': u'l\xe9g\xe8re pluie',
                      'wind_deg': 327.003,
                      'wind_speed': 0.7},
            '08:00': {'clouds_coverage': 20,
                      'humidity': 97,
                      'pressure': 848.98,
                      'rainfall': None,
                      'sea_level_pressure': 1027.24,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 5,
                      'temperature_max ': 5,
                      'temperature_min ': 5,
                      'weather_status': u'l\xe9g\xe8re pluie',
                      'wind_deg': 13.5015,
                      'wind_speed': 0.66},
            '11:00': {'clouds_coverage': 0,
                      'humidity': 61,
                      'pressure': 849.52,
                      'rainfall': None,
                      'sea_level_pressure': 1026.64,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 10,
                      'temperature_max ': 10,
                      'temperature_min ': 10,
                      'weather_status': u'l\xe9g\xe8re pluie',
                      'wind_deg': 346.507,
                      'wind_speed': 0.71},
            '14:00': {'clouds_coverage': 8,
                      'humidity': 38,
                      'pressure': 849.76,
                      'rainfall': None,
                      'sea_level_pressure': 1025.35,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 14,
                      'temperature_max ': 14,
                      'temperature_min ': 14,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 336.002,
                      'wind_speed': 0.76},
            '17:00': {'clouds_coverage': 12,
                      'humidity': 33,
                      'pressure': 849.96,
                      'rainfall': None,
                      'sea_level_pressure': 1024.71,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 15,
                      'temperature_max ': 15,
                      'temperature_min ': 15,
                      'weather_status': u'peu nuageux',
                      'wind_deg': 336.003,
                      'wind_speed': 0.76},
            '20:00': {'clouds_coverage': 48,
                      'humidity': 39,
                      'pressure': 850.72,
                      'rainfall': None,
                      'sea_level_pressure': 1026.03,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 13,
                      'temperature_max ': 13,
                      'temperature_min ': 13,
                      'weather_status': u'partiellement nuageux',
                      'wind_deg': 339.004,
                      'wind_speed': 0.71},
            '23:00': {'clouds_coverage': 0,
                      'humidity': 62,
                      'pressure': 852,
                      'rainfall': None,
                      'sea_level_pressure': 1028.68,
                      'snow': None,
                      'sunrise': '01:00',
                      'sunset': '01:00',
                      'temperature ': 8,
                      'temperature_max ': 8,
                      'temperature_min ': 8,
                      'weather_status': u'ciel d\xe9gag\xe9',
                      'wind_deg': 9.00336,
                      'wind_speed': 0.67}},
 'thursday': {'20:00': {'clouds_coverage': 76,
                        'humidity': 50,
                        'pressure': 854.81,
                        'rainfall': None,
                        'sea_level_pressure': 1027.89,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 25,
                        'temperature_max ': 25,
                        'temperature_min ': 19,
                        'weather_status': u'l\xe9g\xe8re pluie',
                        'wind_deg': 346.502,
                        'wind_speed': 0.61},
              '23:00': {'clouds_coverage': 24,
                        'humidity': 56,
                        'pressure': 855.32,
                        'rainfall': None,
                        'sea_level_pressure': 1029.07,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 21,
                        'temperature_max ': 21,
                        'temperature_min ': 16,
                        'weather_status': u'peu nuageux',
                        'wind_deg': 356.504,
                        'wind_speed': 0.5}},
 'today': {'20:00': {'clouds_coverage': 76,
                     'humidity': 50,
                     'pressure': 854.81,
                     'rainfall': None,
                     'sea_level_pressure': 1027.89,
                     'snow': None,
                     'sunrise': '01:00',
                     'sunset': '01:00',
                     'temperature ': 25,
                     'temperature_max ': 25,
                     'temperature_min ': 19,
                     'weather_status': u'l\xe9g\xe8re pluie',
                     'wind_deg': 346.502,
                     'wind_speed': 0.61},
           '23:00': {'clouds_coverage': 24,
                     'humidity': 56,
                     'pressure': 855.32,
                     'rainfall': None,
                     'sea_level_pressure': 1029.07,
                     'snow': None,
                     'sunrise': '01:00',
                     'sunset': '01:00',
                     'temperature ': 21,
                     'temperature_max ': 21,
                     'temperature_min ': 16,
                     'weather_status': u'peu nuageux',
                     'wind_deg': 356.504,
                     'wind_speed': 0.5}},
 'tomorrow': {'02:00': {'clouds_coverage': 24,
                        'humidity': 68,
                        'pressure': 855.16,
                        'rainfall': None,
                        'sea_level_pressure': 1029.39,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 16,
                        'temperature_max ': 16,
                        'temperature_min ': 14,
                        'weather_status': u'peu nuageux',
                        'wind_deg': 16.5021,
                        'wind_speed': 0.6},
              '05:00': {'clouds_coverage': 12,
                        'humidity': 81,
                        'pressure': 854.45,
                        'rainfall': None,
                        'sea_level_pressure': 1029.04,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 12,
                        'temperature_max ': 12,
                        'temperature_min ': 12,
                        'weather_status': u'peu nuageux',
                        'wind_deg': 25.0013,
                        'wind_speed': 0.56},
              '08:00': {'clouds_coverage': 20,
                        'humidity': 84,
                        'pressure': 854.27,
                        'rainfall': None,
                        'sea_level_pressure': 1029.14,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 12,
                        'temperature_max ': 12,
                        'temperature_min ': 12,
                        'weather_status': u'peu nuageux',
                        'wind_deg': 33.0019,
                        'wind_speed': 0.56},
              '11:00': {'clouds_coverage': 12,
                        'humidity': 64,
                        'pressure': 854.14,
                        'rainfall': None,
                        'sea_level_pressure': 1028.59,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 17,
                        'temperature_max ': 17,
                        'temperature_min ': 17,
                        'weather_status': u'peu nuageux',
                        'wind_deg': 336.502,
                        'wind_speed': 0.77},
              '14:00': {'clouds_coverage': 20,
                        'humidity': 52,
                        'pressure': 853.24,
                        'rainfall': None,
                        'sea_level_pressure': 1027.17,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 19,
                        'temperature_max ': 19,
                        'temperature_min ': 19,
                        'weather_status': u'peu nuageux',
                        'wind_deg': 325.001,
                        'wind_speed': 0.78},
              '17:00': {'clouds_coverage': 24,
                        'humidity': 49,
                        'pressure': 852.46,
                        'rainfall': None,
                        'sea_level_pressure': 1026.26,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 19,
                        'temperature_max ': 19,
                        'temperature_min ': 19,
                        'weather_status': u'peu nuageux',
                        'wind_deg': 319.501,
                        'wind_speed': 0.78},
              '20:00': {'clouds_coverage': 24,
                        'humidity': 58,
                        'pressure': 852.74,
                        'rainfall': None,
                        'sea_level_pressure': 1026.89,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 15,
                        'temperature_max ': 15,
                        'temperature_min ': 15,
                        'weather_status': u'l\xe9g\xe8re pluie',
                        'wind_deg': 323.501,
                        'wind_speed': 0.76},
              '23:00': {'clouds_coverage': 8,
                        'humidity': 74,
                        'pressure': 853.34,
                        'rainfall': None,
                        'sea_level_pressure': 1028.21,
                        'snow': None,
                        'sunrise': '01:00',
                        'sunset': '01:00',
                        'temperature ': 12,
                        'temperature_max ': 12,
                        'temperature_min ': 12,
                        'weather_status': u'ciel d\xe9gag\xe9',
                        'wind_deg': 340.501,
                        'wind_speed': 0.71}},
 'tuesday': {'02:00': {'clouds_coverage': 0,
                       'humidity': 67,
                       'pressure': 856.81,
                       'rainfall': None,
                       'sea_level_pressure': 1032.42,
                       'snow': None,
                       'sunrise': '01:00',
                       'sunset': '01:00',
                       'temperature ': 10,
                       'temperature_max ': 10,
                       'temperature_min ': 10,
                       'weather_status': u'ciel d\xe9gag\xe9',
                       'wind_deg': 82.0025,
                       'wind_speed': 0.76},
             '05:00': {'clouds_coverage': 0,
                       'humidity': 70,
                       'pressure': 856.55,
                       'rainfall': None,
                       'sea_level_pressure': 1032.38,
                       'snow': None,
                       'sunrise': '01:00',
                       'sunset': '01:00',
                       'temperature ': 9,
                       'temperature_max ': 9,
                       'temperature_min ': 9,
                       'weather_status': u'ciel d\xe9gag\xe9',
                       'wind_deg': 106.502,
                       'wind_speed': 0.72},
             '08:00': {'clouds_coverage': 0,
                       'humidity': 65,
                       'pressure': 856.81,
                       'rainfall': None,
                       'sea_level_pressure': 1032.74,
                       'snow': None,
                       'sunrise': '01:00',
                       'sunset': '01:00',
                       'temperature ': 10,
                       'temperature_max ': 10,
                       'temperature_min ': 10,
                       'weather_status': u'ciel d\xe9gag\xe9',
                       'wind_deg': 137.013,
                       'wind_speed': 0.68},
             '11:00': {'clouds_coverage': 0,
                       'humidity': 38,
                       'pressure': 857.42,
                       'rainfall': None,
                       'sea_level_pressure': 1032.36,
                       'snow': None,
                       'sunrise': '01:00',
                       'sunset': '01:00',
                       'temperature ': 20,
                       'temperature_max ': 20,
                       'temperature_min ': 20,
                       'weather_status': u'ciel d\xe9gag\xe9',
                       'wind_deg': 246.504,
                       'wind_speed': 0.78},
             '14:00': {'clouds_coverage': 0,
                       'humidity': 33,
                       'pressure': 857.36,
                       'rainfall': None,
                       'sea_level_pressure': 1031.03,
                       'snow': None,
                       'sunrise': '01:00',
                       'sunset': '01:00',
                       'temperature ': 23,
                       'temperature_max ': 23,
                       'temperature_min ': 23,
                       'weather_status': u'ciel d\xe9gag\xe9',
                       'wind_deg': 273.001,
                       'wind_speed': 0.8},
             '17:00': {'clouds_coverage': 0,
                       'humidity': 31,
                       'pressure': 856.63,
                       'rainfall': None,
                       'sea_level_pressure': 1029.62,
                       'snow': None,
                       'sunrise': '01:00',
                       'sunset': '01:00',
                       'temperature ': 24,
                       'temperature_max ': 24,
                       'temperature_min ': 24,
                       'weather_status': u'ciel d\xe9gag\xe9',
                       'wind_deg': 284.5,
                       'wind_speed': 0.76}}}

```

## License

Copyright (c) 2016. All rights reserved.

Kalliope is covered by the MIT license, a permissive free software license that lets you do anything you want with the source code, 
as long as you provide back attribution and ["don't hold you liable"](http://choosealicense.com/). For the full license text see the [LICENSE.md](LICENSE.md) file.
