# OpenWeatherMap API

## Synopsis 

Retrieve the weather for today, tomorrow or a forecast for 5 days at a specific day of the week with the related data (humidity, temperature, etc ...) for a given location. 

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
| wind_speed_unit | No       | meters_sec | meters_sec, miles_hour, km_hour, knots, beaufort |                                                                                                            |
| country         | No       | None       |                             | [ISO-3166 Country Code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2#Officially_assigned_code_elements)|
| 12h_format      | no       | False      | True/False                  | To get 12 hour format for sunrise and sunset return value                                                  |
| day             | No       | None       | today or a weekday          | Only needed if you want a single synapse to catch the day and translate it in a file_template (required)   |


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

| Time values     |
|-----------------|                                                 
|'02:00'          |
|'05:00'          |
|'08:00'          |
|'11:00'          |
|'14:00'          |
|'17:00'          |
|'20:00'          |
|'23:00'          |
|'daily_forecast' |


**Dict of weather data**

| Name               | Description                                                                              | Type   | Sample               |
|:-------------------|:-----------------------------------------------------------------------------------------|:-------|:---------------------|
| weather_status     | The weather conditions for the given day                                                 | String | heavy intensity rain |
| sunset             | Sunset time (only for daily_forecast and current weather)                                | String | 01:00                |
| sunrise            | Sunrise time (only for daily_forecast and current weather)                               | String | sunrise              |
| temperature        | The expected temperature                                                                 | Int    | 17                   |
| temperature_max    | The expected max. temperature. If time_value then for 3 hours, except for daily_forecast | Int    | 20                   |
| temperature_min    | The expected min. temperature. If time_value then for 3 hours, except for daily_forecast | Int    | 11                   |
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
      - order: "what weather is it"
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

We only get a forecast for 5 days, so if you ask for a day which is not in range it returns no data, for this case you can use a file template. 
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
    The weather today in the morning will be {{ today['08:00']['weather_status'] }} with temperatures from about {{ today['08:00']['temperature'] }} to {{ today['17:00']['temperature'] }} degree at afternoon

{% elif "tomorrow" == day_of_week  %} 
    The weather tomorrow will be {{ tomorrow['08:00']['weather_status'] }} with temperatures from about {{ tomorrow['08:00']['temperature'] }} to {{ tomorrow['17:00']['temperature'] }} degree at afternoon

    
{% elif "monday" == day_of_week  %}
    {% if monday['08:00']['weather_status'] %}
        The weather on Monday will be {{ monday['08:00']['weather_status'] }} with temperatures from about {{ monday['08:00']['temperature'] }} to {{ monday['17:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for monday
    {% endif %}
    
{% elif "tuesday" == day_of_week  %}
    {% if tuesday['08:00']['weather_status'] %} 
        The weather on Tuesday will be {{ tuesday['08:00']['weather_status'] }} with temperatures from about {{ tuesday['08:00']['temperature'] }} to {{ tuesday['17:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for tuesday
    {% endif %}
    
{% elif "wednesday" == day_of_week  %}
    {% if wednesday['08:00']['weather_status'] %}
        The weather on Wednesday will be {{ wednesday['08:00']['weather_status'] }} with temperatures from about {{ wednesday['08:00']['temperature'] }} to {{ wednesday['17:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for wednesday
    {% endif %}
    
{% elif "thursday" == day_of_week %}
    {% if thursday['08:00']['weather_status'] %}
        The weather on Thursday will be {{ thursday['08:00']['weather_status'] }} with temperatures from about {{ thursday['08:00']['temperature'] }} to {{ thursday['17:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for thursday
    {% endif %}
    
{% elif "friday" == day_of_week  %}
    {% if friday['08:00']['weather_status'] %}
        The weather on Friday will be {{ friday['08:00']['weather_status'] }} with temperatures from about {{ friday['08:00']['temperature'] }} to {{ friday['17:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for friday
    {% endif %}
    
{% elif "saturday" == day_of_week  %}
    {% if saturday['08:00']['weather_status'] %}
        The weather on Saturday will be {{ saturday['08:00']['weather_status'] }} with temperatures from about {{ saturday['08:00']['temperature'] }} to {{ saturday['17:00']['temperature'] }} degree at afternoon
    {% else %} 
        I'm sorry, there is no forecast for saturday
    {% endif %}
    
{% elif "sunday" == day_of_week  %}
    {% if sunday['08:00']['weather_status'] %} 
        The weather on Sunday will be {{ sunday['08:00']['weather_status'] }} with temperatures from about {{ sunday['08:00']['temperature'] }} to {{ sunday['17:00']['temperature'] }} degree at afternoon
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
 "location": "Grenoble",
 "latitude": 45.166672,
 "longitude": 5.71667,
 "current": {
  "weather_status": "overcast clouds",
  "sunset": "20:56",
  "sunrise": "06:09",
  "temperature": 7,
  "temperature_min": 6,
  "temperature_max": 13,
  "pressure": 1011,
  "sea_level_pressure": 1011,
  "humidity": 79,
  "wind_deg": 335,
  "wind_speed": 2.58,
  "snow": null,
  "rainfall": null,
  "clouds_coverage": 96
 },
 "thursday": {
  "17:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 7,
   "temperature_min": 7,
   "temperature_max": 7,
   "pressure": 1010,
   "sea_level_pressure": 1010,
   "humidity": 72,
   "wind_deg": 338,
   "wind_speed": 2.57,
   "snow": null,
   "rainfall": 0.14,
   "clouds_coverage": 83
  },
  "20:00": {
   "weather_status": "broken clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 6,
   "temperature_min": 5,
   "temperature_max": 6,
   "pressure": 1010,
   "sea_level_pressure": 1010,
   "humidity": 77,
   "wind_deg": 327,
   "wind_speed": 1.5,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 57
  },
  "23:00": {
   "weather_status": "scattered clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 1,
   "temperature_min": 1,
   "temperature_max": 1,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 90,
   "wind_deg": 105,
   "wind_speed": 1.47,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 30
  },
  "daily_forecast": {
   "weather_status": "rain and snow",
   "sunset": "20:56",
   "sunrise": "06:09",
   "temperature": 6,
   "temperature_min": 0,
   "temperature_max": 7,
   "pressure": 1011,
   "sea_level_pressure": null,
   "humidity": 82,
   "wind_deg": 336,
   "wind_speed": 2.61,
   "snow": 0.25,
   "rainfall": 5.03,
   "clouds_coverage": 96
  }
 },
 "friday": {
  "02:00": {
   "weather_status": "scattered clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 0,
   "temperature_min": 0,
   "temperature_max": 0,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 87,
   "wind_deg": 119,
   "wind_speed": 1.68,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 35
  },
  "05:00": {
   "weather_status": "scattered clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": -1,
   "temperature_min": -1,
   "temperature_max": -1,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 83,
   "wind_deg": 107,
   "wind_speed": 1.34,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 46
  },
  "08:00": {
   "weather_status": "broken clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 2,
   "temperature_min": 2,
   "temperature_max": 2,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 71,
   "wind_deg": 348,
   "wind_speed": 1.41,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 64
  },
  "11:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 6,
   "temperature_min": 6,
   "temperature_max": 6,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 69,
   "wind_deg": 324,
   "wind_speed": 2.41,
   "snow": null,
   "rainfall": 0.11,
   "clouds_coverage": 99
  },
  "14:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 89,
   "wind_deg": 318,
   "wind_speed": 2.71,
   "snow": null,
   "rainfall": 1.09,
   "clouds_coverage": 97
  },
  "17:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 85,
   "wind_deg": 337,
   "wind_speed": 2.55,
   "snow": null,
   "rainfall": 0.47,
   "clouds_coverage": 99
  },
  "20:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1013,
   "sea_level_pressure": 1013,
   "humidity": 87,
   "wind_deg": 354,
   "wind_speed": 2.12,
   "snow": null,
   "rainfall": 0.28,
   "clouds_coverage": 86
  },
  "23:00": {
   "weather_status": "scattered clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 1,
   "temperature_min": 1,
   "temperature_max": 1,
   "pressure": 1016,
   "sea_level_pressure": 1016,
   "humidity": 92,
   "wind_deg": 57,
   "wind_speed": 1.19,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 36
  },
  "daily_forecast": {
   "weather_status": "rain and snow",
   "sunset": "20:57",
   "sunrise": "06:08",
   "temperature": 5,
   "temperature_min": -1,
   "temperature_max": 6,
   "pressure": 1011,
   "sea_level_pressure": null,
   "humidity": 82,
   "wind_deg": 319,
   "wind_speed": 2.85,
   "snow": 0.12,
   "rainfall": 1.62,
   "clouds_coverage": 97
  }
 },
 "saturday": {
  "02:00": {
   "weather_status": "broken clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 0,
   "temperature_min": 0,
   "temperature_max": 0,
   "pressure": 1016,
   "sea_level_pressure": 1016,
   "humidity": 86,
   "wind_deg": 83,
   "wind_speed": 1.12,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 68
  },
  "05:00": {
   "weather_status": "overcast clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 1,
   "temperature_min": 1,
   "temperature_max": 1,
   "pressure": 1014,
   "sea_level_pressure": 1014,
   "humidity": 79,
   "wind_deg": 148,
   "wind_speed": 1.13,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 100
  },
  "08:00": {
   "weather_status": "overcast clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 3,
   "temperature_min": 3,
   "temperature_max": 3,
   "pressure": 1013,
   "sea_level_pressure": 1013,
   "humidity": 75,
   "wind_deg": 168,
   "wind_speed": 1.69,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 100
  },
  "11:00": {
   "weather_status": "overcast clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 6,
   "temperature_min": 6,
   "temperature_max": 6,
   "pressure": 1013,
   "sea_level_pressure": 1013,
   "humidity": 64,
   "wind_deg": 221,
   "wind_speed": 2.16,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 100
  },
  "14:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 3,
   "temperature_min": 3,
   "temperature_max": 3,
   "pressure": 1014,
   "sea_level_pressure": 1014,
   "humidity": 94,
   "wind_deg": 191,
   "wind_speed": 2.19,
   "snow": null,
   "rainfall": 1.13,
   "clouds_coverage": 100
  },
  "17:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 3,
   "temperature_min": 3,
   "temperature_max": 3,
   "pressure": 1013,
   "sea_level_pressure": 1013,
   "humidity": 97,
   "wind_deg": 165,
   "wind_speed": 1.83,
   "snow": null,
   "rainfall": 2.75,
   "clouds_coverage": 100
  },
  "20:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1013,
   "sea_level_pressure": 1013,
   "humidity": 98,
   "wind_deg": 173,
   "wind_speed": 1.75,
   "snow": null,
   "rainfall": 2.51,
   "clouds_coverage": 100
  },
  "23:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1014,
   "sea_level_pressure": 1014,
   "humidity": 98,
   "wind_deg": 159,
   "wind_speed": 1.45,
   "snow": null,
   "rainfall": 2.8,
   "clouds_coverage": 100
  },
  "daily_forecast": {
   "weather_status": "light rain",
   "sunset": "20:58",
   "sunrise": "06:07",
   "temperature": 3,
   "temperature_min": 0,
   "temperature_max": 6,
   "pressure": 1014,
   "sea_level_pressure": null,
   "humidity": 94,
   "wind_deg": 191,
   "wind_speed": 2.19,
   "snow": null,
   "rainfall": 9.19,
   "clouds_coverage": 100
  }
 },
 "sunday": {
  "02:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 97,
   "wind_deg": 148,
   "wind_speed": 1.26,
   "snow": null,
   "rainfall": 0.47,
   "clouds_coverage": 100
  },
  "05:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 98,
   "wind_deg": 157,
   "wind_speed": 1.87,
   "snow": null,
   "rainfall": 2.62,
   "clouds_coverage": 100
  },
  "08:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 5,
   "temperature_min": 5,
   "temperature_max": 5,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 96,
   "wind_deg": 150,
   "wind_speed": 1.6,
   "snow": null,
   "rainfall": 0.84,
   "clouds_coverage": 100
  },
  "11:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 8,
   "temperature_min": 8,
   "temperature_max": 8,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 88,
   "wind_deg": 217,
   "wind_speed": 2.22,
   "snow": null,
   "rainfall": 0.74,
   "clouds_coverage": 100
  },
  "14:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 9,
   "temperature_min": 9,
   "temperature_max": 9,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 79,
   "wind_deg": 213,
   "wind_speed": 2.66,
   "snow": null,
   "rainfall": 0.79,
   "clouds_coverage": 100
  },
  "17:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 8,
   "temperature_min": 8,
   "temperature_max": 8,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 91,
   "wind_deg": 210,
   "wind_speed": 1.91,
   "snow": null,
   "rainfall": 2.63,
   "clouds_coverage": 100
  },
  "20:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 6,
   "temperature_min": 6,
   "temperature_max": 6,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 96,
   "wind_deg": 235,
   "wind_speed": 1.28,
   "snow": null,
   "rainfall": 2.33,
   "clouds_coverage": 100
  },
  "23:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1014,
   "sea_level_pressure": 1014,
   "humidity": 97,
   "wind_deg": 307,
   "wind_speed": 0.34,
   "snow": null,
   "rainfall": 0.58,
   "clouds_coverage": 88
  },
  "daily_forecast": {
   "weather_status": "light rain",
   "sunset": "20:59",
   "sunrise": "06:06",
   "temperature": 9,
   "temperature_min": 4,
   "temperature_max": 9,
   "pressure": 1011,
   "sea_level_pressure": null,
   "humidity": 79,
   "wind_deg": 213,
   "wind_speed": 2.66,
   "snow": null,
   "rainfall": 11,
   "clouds_coverage": 100
  }
 },
 "monday": {
  "02:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 3,
   "temperature_min": 3,
   "temperature_max": 3,
   "pressure": 1015,
   "sea_level_pressure": 1015,
   "humidity": 96,
   "wind_deg": 276,
   "wind_speed": 0.38,
   "snow": null,
   "rainfall": 0.22,
   "clouds_coverage": 80
  },
  "05:00": {
   "weather_status": "broken clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 1,
   "temperature_min": 1,
   "temperature_max": 1,
   "pressure": 1015,
   "sea_level_pressure": 1015,
   "humidity": 97,
   "wind_deg": 85,
   "wind_speed": 0.76,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 74
  },
  "08:00": {
   "weather_status": "broken clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 3,
   "temperature_min": 3,
   "temperature_max": 3,
   "pressure": 1015,
   "sea_level_pressure": 1015,
   "humidity": 94,
   "wind_deg": 302,
   "wind_speed": 1.07,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 56
  },
  "11:00": {
   "weather_status": "scattered clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 7,
   "temperature_min": 7,
   "temperature_max": 7,
   "pressure": 1013,
   "sea_level_pressure": 1013,
   "humidity": 64,
   "wind_deg": 297,
   "wind_speed": 2.04,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 30
  },
  "14:00": {
   "weather_status": "few clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 10,
   "temperature_min": 10,
   "temperature_max": 10,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 42,
   "wind_deg": 323,
   "wind_speed": 2.69,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 20
  },
  "17:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 9,
   "temperature_min": 9,
   "temperature_max": 9,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 49,
   "wind_deg": 309,
   "wind_speed": 2.74,
   "snow": null,
   "rainfall": 0.12,
   "clouds_coverage": 58
  },
  "20:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1015,
   "sea_level_pressure": 1015,
   "humidity": 91,
   "wind_deg": 310,
   "wind_speed": 1.96,
   "snow": null,
   "rainfall": 1.5,
   "clouds_coverage": 75
  },
  "23:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 2,
   "temperature_min": 2,
   "temperature_max": 2,
   "pressure": 1018,
   "sea_level_pressure": 1018,
   "humidity": 97,
   "wind_deg": 311,
   "wind_speed": 1.49,
   "snow": null,
   "rainfall": 2.46,
   "clouds_coverage": 100
  },
  "daily_forecast": {
   "weather_status": "light rain",
   "sunset": "21:01",
   "sunrise": "06:05",
   "temperature": 10,
   "temperature_min": 1,
   "temperature_max": 10,
   "pressure": 1012,
   "sea_level_pressure": null,
   "humidity": 42,
   "wind_deg": 309,
   "wind_speed": 2.74,
   "snow": null,
   "rainfall": 4.3,
   "clouds_coverage": 20
  }
 },
 "tuesday": {
  "02:00": {
   "weather_status": "moderate rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 2,
   "temperature_min": 2,
   "temperature_max": 2,
   "pressure": 1019,
   "sea_level_pressure": 1019,
   "humidity": 99,
   "wind_deg": 318,
   "wind_speed": 1.82,
   "snow": null,
   "rainfall": 4.76,
   "clouds_coverage": 100
  },
  "05:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 1,
   "temperature_min": 1,
   "temperature_max": 1,
   "pressure": 1020,
   "sea_level_pressure": 1020,
   "humidity": 98,
   "wind_deg": 332,
   "wind_speed": 1.92,
   "snow": null,
   "rainfall": 1.44,
   "clouds_coverage": 100
  },
  "08:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 1,
   "temperature_min": 1,
   "temperature_max": 1,
   "pressure": 1021,
   "sea_level_pressure": 1021,
   "humidity": 98,
   "wind_deg": 336,
   "wind_speed": 2.27,
   "snow": null,
   "rainfall": 0.87,
   "clouds_coverage": 100
  },
  "11:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 1,
   "temperature_min": 1,
   "temperature_max": 1,
   "pressure": 1023,
   "sea_level_pressure": 1023,
   "humidity": 98,
   "wind_deg": 339,
   "wind_speed": 2.13,
   "snow": null,
   "rainfall": 0.86,
   "clouds_coverage": 100
  },
  "14:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 3,
   "temperature_min": 3,
   "temperature_max": 3,
   "pressure": 1023,
   "sea_level_pressure": 1023,
   "humidity": 91,
   "wind_deg": 346,
   "wind_speed": 2.6,
   "snow": null,
   "rainfall": 0.34,
   "clouds_coverage": 100
  },
  "daily_forecast": {
   "weather_status": "moderate rain",
   "sunset": "21:02",
   "sunrise": "06:04",
   "temperature": 3,
   "temperature_min": 0,
   "temperature_max": 7,
   "pressure": 1023,
   "sea_level_pressure": null,
   "humidity": 91,
   "wind_deg": 343,
   "wind_speed": 3.22,
   "snow": null,
   "rainfall": 8.45,
   "clouds_coverage": 100
  }
 },
 "wednesday": {
  "daily_forecast": {
   "weather_status": "overcast clouds",
   "sunset": "21:03",
   "sunrise": "06:03",
   "temperature": 13,
   "temperature_min": -1,
   "temperature_max": 14,
   "pressure": 1021,
   "sea_level_pressure": null,
   "humidity": 60,
   "wind_deg": 328,
   "wind_speed": 1.92,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 98
  }
 },
 "today": {
  "17:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 7,
   "temperature_min": 7,
   "temperature_max": 7,
   "pressure": 1010,
   "sea_level_pressure": 1010,
   "humidity": 72,
   "wind_deg": 338,
   "wind_speed": 2.57,
   "snow": null,
   "rainfall": 0.14,
   "clouds_coverage": 83
  },
  "20:00": {
   "weather_status": "broken clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 6,
   "temperature_min": 5,
   "temperature_max": 6,
   "pressure": 1010,
   "sea_level_pressure": 1010,
   "humidity": 77,
   "wind_deg": 327,
   "wind_speed": 1.5,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 57
  },
  "23:00": {
   "weather_status": "scattered clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 1,
   "temperature_min": 1,
   "temperature_max": 1,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 90,
   "wind_deg": 105,
   "wind_speed": 1.47,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 30
  },
  "daily_forecast": {
   "weather_status": "rain and snow",
   "sunset": "20:56",
   "sunrise": "06:09",
   "temperature": 6,
   "temperature_min": 0,
   "temperature_max": 7,
   "pressure": 1011,
   "sea_level_pressure": null,
   "humidity": 82,
   "wind_deg": 336,
   "wind_speed": 2.61,
   "snow": 0.25,
   "rainfall": 5.03,
   "clouds_coverage": 96
  }
 },
 "tomorrow": {
  "02:00": {
   "weather_status": "scattered clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 0,
   "temperature_min": 0,
   "temperature_max": 0,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 87,
   "wind_deg": 119,
   "wind_speed": 1.68,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 35
  },
  "05:00": {
   "weather_status": "scattered clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": -1,
   "temperature_min": -1,
   "temperature_max": -1,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 83,
   "wind_deg": 107,
   "wind_speed": 1.34,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 46
  },
  "08:00": {
   "weather_status": "broken clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 2,
   "temperature_min": 2,
   "temperature_max": 2,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 71,
   "wind_deg": 348,
   "wind_speed": 1.41,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 64
  },
  "11:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 6,
   "temperature_min": 6,
   "temperature_max": 6,
   "pressure": 1011,
   "sea_level_pressure": 1011,
   "humidity": 69,
   "wind_deg": 324,
   "wind_speed": 2.41,
   "snow": null,
   "rainfall": 0.11,
   "clouds_coverage": 99
  },
  "14:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 89,
   "wind_deg": 318,
   "wind_speed": 2.71,
   "snow": null,
   "rainfall": 1.09,
   "clouds_coverage": 97
  },
  "17:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1012,
   "sea_level_pressure": 1012,
   "humidity": 85,
   "wind_deg": 337,
   "wind_speed": 2.55,
   "snow": null,
   "rainfall": 0.47,
   "clouds_coverage": 99
  },
  "20:00": {
   "weather_status": "light rain",
   "sunset": null,
   "sunrise": null,
   "temperature": 4,
   "temperature_min": 4,
   "temperature_max": 4,
   "pressure": 1013,
   "sea_level_pressure": 1013,
   "humidity": 87,
   "wind_deg": 354,
   "wind_speed": 2.12,
   "snow": null,
   "rainfall": 0.28,
   "clouds_coverage": 86
  },
  "23:00": {
   "weather_status": "scattered clouds",
   "sunset": null,
   "sunrise": null,
   "temperature": 1,
   "temperature_min": 1,
   "temperature_max": 1,
   "pressure": 1016,
   "sea_level_pressure": 1016,
   "humidity": 92,
   "wind_deg": 57,
   "wind_speed": 1.19,
   "snow": null,
   "rainfall": null,
   "clouds_coverage": 36
  },
  "daily_forecast": {
   "weather_status": "rain and snow",
   "sunset": "20:57",
   "sunrise": "06:08",
   "temperature": 5,
   "temperature_min": -1,
   "temperature_max": 6,
   "pressure": 1011,
   "sea_level_pressure": null,
   "humidity": 82,
   "wind_deg": 319,
   "wind_speed": 2.85,
   "snow": 0.12,
   "rainfall": 1.62,
   "clouds_coverage": 97
  }
 }
}

```

## License

Copyright (c) 2016. All rights reserved.

Kalliope is covered by the MIT license, a permissive free software license that lets you do anything you want with the source code, 
as long as you provide back attribution and ["don't hold you liable"](http://choosealicense.com/). For the full license text see the [LICENSE.md](LICENSE.md) file.
