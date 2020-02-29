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
|'01:00'      |
|'04:00'      |
|'07:00'      |
|'10:00'      |
|'13:00'      |
|'16:00'      |
|'19:00'      |
|'22:00'      |


**Dict of weather data**

| Name               | Description                               | Type   | Sample               |
|:-------------------|:------------------------------------------|:-------|:---------------------|
| weather_status     | The weather conditions for the given day  | String | heavy intensity rain |
| sunset             | Sunset time                               | String | 01:00                |
| sunrise            | Sunrise time                              | String | sunrise              |
| temperature        | The expected temperature                  | Int    | 17                   |
| temperature_max    | The expected max. temperature for 3 hours | Int    | 20                   |
| temperature_min    | The expected min. temperature for 3 hours | Int    | 11                   |
| pressure           | The expected pressure in hectopascals     | Float  | 857.32               |
| sea_level_pressure | The expected sea level pressure in hpa    | Float  | 627.25               |
| humidity           | The expected humidity in percent          | Float  | 63                   |
| wind_speed         | The expected wind speed in meter/seconds  | Float  | 0.87                 |
| wind_deg           | The expected wind directions in degree    | Float  | 163                  |
| rainfall           | The expected rainfall volume              | Float  | 13.76                |
| snow               | The expected snowfall volume              | Float  | None                 |
| clouds_coverage    | The expected cloud coverage in percent    | Float  | 65                   |


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
          - "Today at {{ location }}, the weather is {{ current['weather_status'] }} with a temperature of{{ current['temperature'] }} degrees and tomorrow the weather will be {{ tomorrow['10:00']['weather_status'] }} with temperatures in the morning from {{ tomorrow['07:00']['temperature'] }}  to  {{ tomorrow['19:00']['temperature'] }} degree in the evening"
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
          say_template: "The weather on Monday morning will be {{ monday['07:00']['weather_status'] }} with temperatures from  {{ monday['07:00']['temperature'] }}  to  {{ monday['16:00']['temperature'] }} degree at afternoon"
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
          say_template: "The weather today starts today with {{ today['07:00']['weather_status'] }} and {{ today['10:00']['weather_status'] }} at noon for the evening you can expect {{ today['19:00']['weather_status'] }}"
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
    The weather today in the morning will be {{ today['07:00']['weather_status'] }} with temperatures from about {{ today['07:00']['temperature'] }} to {{ today['16:00']['temperature'] }} degree at afternoon

{% elif "tomorrow" == day_of_week  %} 
    The weather tomorrow will be {{ tomorrow['07:00']['weather_status'] }} with temperatures from about {{ tomorrow['07:00']['temperature'] }} to {{ tomorrow['16:00']['temperature'] }} degree at afternoon

    
{% elif "monday" == day_of_week  %}
    {% if monday['weather_status'] %}
        The weather on Monday will be {{ monday['07:00']['weather_status'] }} with temperatures from about {{ monday['07:00']['temperature'] }} to {{ monday['16:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for monday
    {% endif %}
    
{% elif "tuesday" == day_of_week  %}
    {% if tuesday['weather_status'] %} 
        The weather on Tuesday will be {{ tuesday['07:00']['weather_status'] }} with temperatures from about {{ tuesday['07:00']['temperature'] }} to {{ tuesday['16:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for tuesday
    {% endif %}
    
{% elif "wednesday" == day_of_week  %}
    {% if wednesday['weather_status'] %}
        The weather on Wednesday will be {{ wednesday['07:00']['weather_status'] }} with temperatures from about {{ wednesday['07:00']['temperature'] }} to {{ wednesday['16:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for wednesday
    {% endif %}
    
{% elif "thursday" == day_of_week %}
    {% if thursday['weather_status'] %}
        The weather on Thursday will be {{ thursday['07:00']['weather_status'] }} with temperatures from about {{ thursday['07:00']['temperature'] }} to {{ thursday['16:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for thursday
    {% endif %}
    
{% elif "friday" == day_of_week  %}
    {% if friday['weather_status'] %}
        The weather on Friday will be {{ friday['07:00']['weather_status'] }} with temperatures from about {{ friday['07:00']['temperature'] }} to {{ friday['16:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for friday
    {% endif %}
    
{% elif "saturday" == day_of_week  %}
    {% if saturday['weather_status'] %}
        The weather on Saturday will be {{ saturday['07:00']['weather_status'] }} with temperatures from about {{ saturday['07:00']['temperature'] }} to {{ saturday['16:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for saturday
    {% endif %}
    
{% elif "sunday" == day_of_week  %}
    {% if sunday['weather_status'] %} 
        The weather on Sunday will be {{ sunday['07:00']['weather_status'] }} with temperatures from about {{ sunday['07:00']['temperature'] }} to {{ sunday['16:00']['temperature'] }} degree at afternoon
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

```json
{
   "location":"Grenoble",
   "latitude":45.07,
   "longitude":5.83,
   "current":{
      "weather_status":"light rain",
      "sunset":"18:22",
      "sunrise":"07:16",
      "temperature":10,
      "temperature_min":7,
      "temperature_max":13,
      "pressure":1006,
      "sea_level_pressure":"None",
      "humidity":87,
      "wind_deg":230,
      "wind_speed":4.1,
      "rainfall":"None",
      "snow":"None",
      "clouds_coverage":100
   },
   "saturday":{
      "19:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":6,
         "temperature_min":0,
         "temperature_max":6,
         "pressure":1009,
         "sea_level_pressure":1009,
         "humidity":97,
         "wind_deg":167,
         "wind_speed":2.95,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "22:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":5,
         "temperature_min":0,
         "temperature_max":5,
         "pressure":1010,
         "sea_level_pressure":1010,
         "humidity":99,
         "wind_deg":214,
         "wind_speed":2.32,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      }
   },
   "sunday":{
      "01:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":3,
         "temperature_min":0,
         "temperature_max":3,
         "pressure":1010,
         "sea_level_pressure":1010,
         "humidity":99,
         "wind_deg":251,
         "wind_speed":2.28,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "04:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":1,
         "temperature_min":-1,
         "temperature_max":1,
         "pressure":1009,
         "sea_level_pressure":1009,
         "humidity":99,
         "wind_deg":288,
         "wind_speed":1.71,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "07:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-1,
         "temperature_min":-1,
         "temperature_max":-1,
         "pressure":1009,
         "sea_level_pressure":1009,
         "humidity":98,
         "wind_deg":344,
         "wind_speed":0.76,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "10:00":{
         "weather_status":"broken clouds",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":1,
         "temperature_min":1,
         "temperature_max":1,
         "pressure":1007,
         "sea_level_pressure":1007,
         "humidity":87,
         "wind_deg":288,
         "wind_speed":1.41,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":71
      },
      "13:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":2,
         "temperature_min":2,
         "temperature_max":2,
         "pressure":1005,
         "sea_level_pressure":1005,
         "humidity":85,
         "wind_deg":235,
         "wind_speed":2.35,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":80
      },
      "16:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":1,
         "temperature_min":1,
         "temperature_max":1,
         "pressure":1003,
         "sea_level_pressure":1003,
         "humidity":81,
         "wind_deg":205,
         "wind_speed":2.79,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":93
      },
      "19:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-1,
         "temperature_min":-1,
         "temperature_max":-1,
         "pressure":1005,
         "sea_level_pressure":1005,
         "humidity":98,
         "wind_deg":214,
         "wind_speed":2.66,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":96
      },
      "22:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-1,
         "temperature_min":-1,
         "temperature_max":-1,
         "pressure":1006,
         "sea_level_pressure":1006,
         "humidity":98,
         "wind_deg":175,
         "wind_speed":1.17,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      }
   },
   "monday":{
      "01:00":{
         "weather_status":"overcast clouds",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-3,
         "temperature_min":-3,
         "temperature_max":-3,
         "pressure":1005,
         "sea_level_pressure":1005,
         "humidity":81,
         "wind_deg":130,
         "wind_speed":2.44,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "04:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-4,
         "temperature_min":-4,
         "temperature_max":-4,
         "pressure":1003,
         "sea_level_pressure":1003,
         "humidity":96,
         "wind_deg":126,
         "wind_speed":2.41,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "07:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-2,
         "temperature_min":-2,
         "temperature_max":-2,
         "pressure":1000,
         "sea_level_pressure":1000,
         "humidity":94,
         "wind_deg":143,
         "wind_speed":2.91,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "10:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":0,
         "temperature_min":0,
         "temperature_max":0,
         "pressure":998,
         "sea_level_pressure":998,
         "humidity":98,
         "wind_deg":172,
         "wind_speed":2.84,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "13:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":0,
         "temperature_min":0,
         "temperature_max":0,
         "pressure":995,
         "sea_level_pressure":995,
         "humidity":99,
         "wind_deg":216,
         "wind_speed":2.41,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "16:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-1,
         "temperature_min":-1,
         "temperature_max":-1,
         "pressure":995,
         "sea_level_pressure":995,
         "humidity":99,
         "wind_deg":281,
         "wind_speed":2.9,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "19:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-6,
         "temperature_min":-6,
         "temperature_max":-6,
         "pressure":996,
         "sea_level_pressure":996,
         "humidity":98,
         "wind_deg":12,
         "wind_speed":2.2,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":94
      },
      "22:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-4,
         "temperature_min":-4,
         "temperature_max":-4,
         "pressure":998,
         "sea_level_pressure":998,
         "humidity":98,
         "wind_deg":305,
         "wind_speed":1.73,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":99
      }
   },
   "tuesday":{
      "01:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-4,
         "temperature_min":-4,
         "temperature_max":-4,
         "pressure":999,
         "sea_level_pressure":999,
         "humidity":98,
         "wind_deg":307,
         "wind_speed":2.5,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "04:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-6,
         "temperature_min":-6,
         "temperature_max":-6,
         "pressure":1000,
         "sea_level_pressure":1000,
         "humidity":98,
         "wind_deg":317,
         "wind_speed":3.11,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "07:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-6,
         "temperature_min":-6,
         "temperature_max":-6,
         "pressure":1003,
         "sea_level_pressure":1003,
         "humidity":97,
         "wind_deg":321,
         "wind_speed":3.77,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "10:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-6,
         "temperature_min":-6,
         "temperature_max":-6,
         "pressure":1006,
         "sea_level_pressure":1006,
         "humidity":96,
         "wind_deg":332,
         "wind_speed":3.7,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "13:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-5,
         "temperature_min":-5,
         "temperature_max":-5,
         "pressure":1007,
         "sea_level_pressure":1007,
         "humidity":90,
         "wind_deg":336,
         "wind_speed":3.69,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "16:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-5,
         "temperature_min":-5,
         "temperature_max":-5,
         "pressure":1007,
         "sea_level_pressure":1007,
         "humidity":90,
         "wind_deg":338,
         "wind_speed":3.55,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":84
      },
      "19:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-9,
         "temperature_min":-9,
         "temperature_max":-9,
         "pressure":1010,
         "sea_level_pressure":1010,
         "humidity":93,
         "wind_deg":43,
         "wind_speed":2.54,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":83
      },
      "22:00":{
         "weather_status":"few clouds",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-10,
         "temperature_min":-10,
         "temperature_max":-10,
         "pressure":1012,
         "sea_level_pressure":1012,
         "humidity":80,
         "wind_deg":57,
         "wind_speed":2.72,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":11
      }
   },
   "wednesday":{
      "01:00":{
         "weather_status":"clear sky",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-11,
         "temperature_min":-11,
         "temperature_max":-11,
         "pressure":1012,
         "sea_level_pressure":1012,
         "humidity":77,
         "wind_deg":64,
         "wind_speed":2.73,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":5
      },
      "04:00":{
         "weather_status":"clear sky",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-10,
         "temperature_min":-10,
         "temperature_max":-10,
         "pressure":1011,
         "sea_level_pressure":1011,
         "humidity":75,
         "wind_deg":73,
         "wind_speed":2.87,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":0
      },
      "07:00":{
         "weather_status":"clear sky",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-9,
         "temperature_min":-9,
         "temperature_max":-9,
         "pressure":1011,
         "sea_level_pressure":1011,
         "humidity":65,
         "wind_deg":82,
         "wind_speed":2.47,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":0
      },
      "10:00":{
         "weather_status":"broken clouds",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-2,
         "temperature_min":-2,
         "temperature_max":-2,
         "pressure":1010,
         "sea_level_pressure":1010,
         "humidity":76,
         "wind_deg":302,
         "wind_speed":0.34,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":63
      },
      "13:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-1,
         "temperature_min":-1,
         "temperature_max":-1,
         "pressure":1009,
         "sea_level_pressure":1009,
         "humidity":99,
         "wind_deg":281,
         "wind_speed":1.59,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":81
      },
      "16:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-1,
         "temperature_min":-1,
         "temperature_max":-1,
         "pressure":1007,
         "sea_level_pressure":1007,
         "humidity":99,
         "wind_deg":298,
         "wind_speed":2.15,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "19:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-2,
         "temperature_min":-2,
         "temperature_max":-2,
         "pressure":1010,
         "sea_level_pressure":1010,
         "humidity":99,
         "wind_deg":357,
         "wind_speed":1.46,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "22:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-2,
         "temperature_min":-2,
         "temperature_max":-2,
         "pressure":1011,
         "sea_level_pressure":1011,
         "humidity":94,
         "wind_deg":3,
         "wind_speed":1.69,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      }
   },
   "thursday":{
      "01:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-4,
         "temperature_min":-4,
         "temperature_max":-4,
         "pressure":1011,
         "sea_level_pressure":1011,
         "humidity":92,
         "wind_deg":64,
         "wind_speed":2.18,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":96
      },
      "04:00":{
         "weather_status":"overcast clouds",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-2,
         "temperature_min":-2,
         "temperature_max":-2,
         "pressure":1011,
         "sea_level_pressure":1011,
         "humidity":86,
         "wind_deg":81,
         "wind_speed":1.93,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":97
      },
      "07:00":{
         "weather_status":"overcast clouds",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-2,
         "temperature_min":-2,
         "temperature_max":-2,
         "pressure":1009,
         "sea_level_pressure":1009,
         "humidity":83,
         "wind_deg":109,
         "wind_speed":1.67,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":98
      },
      "10:00":{
         "weather_status":"overcast clouds",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":1,
         "temperature_min":1,
         "temperature_max":1,
         "pressure":1007,
         "sea_level_pressure":1007,
         "humidity":98,
         "wind_deg":167,
         "wind_speed":1.63,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "13:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":0,
         "temperature_min":0,
         "temperature_max":0,
         "pressure":1006,
         "sea_level_pressure":1006,
         "humidity":100,
         "wind_deg":163,
         "wind_speed":2.72,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "16:00":{
         "weather_status":"moderate rain",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":1,
         "temperature_min":1,
         "temperature_max":1,
         "pressure":1003,
         "sea_level_pressure":1003,
         "humidity":99,
         "wind_deg":167,
         "wind_speed":2.74,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      }
   },
   "friday":"None",
   "today":{
      "19:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":6,
         "temperature_min":0,
         "temperature_max":6,
         "pressure":1009,
         "sea_level_pressure":1009,
         "humidity":97,
         "wind_deg":167,
         "wind_speed":2.95,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "22:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":5,
         "temperature_min":0,
         "temperature_max":5,
         "pressure":1010,
         "sea_level_pressure":1010,
         "humidity":99,
         "wind_deg":214,
         "wind_speed":2.32,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      }
   },
   "tomorrow":{
      "01:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":3,
         "temperature_min":0,
         "temperature_max":3,
         "pressure":1010,
         "sea_level_pressure":1010,
         "humidity":99,
         "wind_deg":251,
         "wind_speed":2.28,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "04:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":1,
         "temperature_min":-1,
         "temperature_max":1,
         "pressure":1009,
         "sea_level_pressure":1009,
         "humidity":99,
         "wind_deg":288,
         "wind_speed":1.71,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "07:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-1,
         "temperature_min":-1,
         "temperature_max":-1,
         "pressure":1009,
         "sea_level_pressure":1009,
         "humidity":98,
         "wind_deg":344,
         "wind_speed":0.76,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      },
      "10:00":{
         "weather_status":"broken clouds",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":1,
         "temperature_min":1,
         "temperature_max":1,
         "pressure":1007,
         "sea_level_pressure":1007,
         "humidity":87,
         "wind_deg":288,
         "wind_speed":1.41,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":71
      },
      "13:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":2,
         "temperature_min":2,
         "temperature_max":2,
         "pressure":1005,
         "sea_level_pressure":1005,
         "humidity":85,
         "wind_deg":235,
         "wind_speed":2.35,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":80
      },
      "16:00":{
         "weather_status":"light snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":1,
         "temperature_min":1,
         "temperature_max":1,
         "pressure":1003,
         "sea_level_pressure":1003,
         "humidity":81,
         "wind_deg":205,
         "wind_speed":2.79,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":93
      },
      "19:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-1,
         "temperature_min":-1,
         "temperature_max":-1,
         "pressure":1005,
         "sea_level_pressure":1005,
         "humidity":98,
         "wind_deg":214,
         "wind_speed":2.66,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":96
      },
      "22:00":{
         "weather_status":"snow",
         "sunset":"01:00",
         "sunrise":"01:00",
         "temperature":-1,
         "temperature_min":-1,
         "temperature_max":-1,
         "pressure":1006,
         "sea_level_pressure":1006,
         "humidity":98,
         "wind_deg":175,
         "wind_speed":1.17,
         "rainfall":"None",
         "snow":"None",
         "clouds_coverage":100
      }
   }
}
```

## License

Copyright (c) 2016. All rights reserved.

Kalliope is covered by the MIT license, a permissive free software license that lets you do anything you want with the source code, 
as long as you provide back attribution and ["don't hold you liable"](http://choosealicense.com/). For the full license text see the [LICENSE.md](LICENSE.md) file.
