# OpenWeatherMap API

## Synopsis 

Give the today, tomorrow weather or a forecast for a specific day of the week with the related data (humidity, temperature, etc ...) for a given location. 

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

| name          | Description                               | Type   | sample                    |
| ------------- | ----------------------------------------- | ------ | ------------------------- |
| location      | The current location                      | String | Grenoble                  |
| longitude     | The current longitude                     | Float  | 5.73                      |
| latitude      | The current latitude                      | Float  | 45.18                     |
| sunset_today  | The sunset time for today                 | Time   | 20:52                     |
| sunrise_today | The sunrise time for today                | Time   | 06:31                     |
| current       | Dict of weather data for the current time | Dict   | {'evening_temp': 23, ...} |
| tomorrow      | Dict of weather data for tomorrow         | Dict   | {'evening_temp': 23, ...} |
| today         | Dict of weather data for today            | Dict   | {'evening_temp': 23, ...} |
| monday        | Dict of weather data for today            | Dict   | {'evening_temp': 23, ...} |
| tuesday       | Dict of weather data for tuesday          | Dict   | {'evening_temp': 23, ...} |
| wednesday     | Dict of weather data for wednesday        | Dict   | {'evening_temp': 23, ...} |
| thursday      | Dict of weather data for thursday         | Dict   | {'evening_temp': 23, ...} |
| friday        | Dict of weather data for friday           | Dict   | {'evening_temp': 23, ...} |
| saturday      | Dict of weather data for saturday         | Dict   | {'evening_temp': 23, ...} |
| sunday        | Dict of weather data for sunday           | Dict   | {'evening_temp': 23, ...} |


**Dict of weather data**

| name           | Description                              | Type   | sample               |
| -------------- | ---------------------------------------- | ------ | -------------------- |
| weather_status | The weather conditions for the given day | String | heavy intensity rain |
| temp           | The expected temperature                 | Int    | 17                   |
| max_temp       | The expected max. temperature            | Int    | 20                   |
| min_temp       | The expected min. temperature            | Int    | 11                   |
| morning_temp   | The expected temperature at the morning  | Int    | 20                   |
| evening_temp   | The expected temperature at the evening  | Int    | 16                   |
| night_temp     | The expected temperature at the night    | Int    | 11                   |
| humidity       | The expected humidity in percent         | Float  | 63                   |
| wind_speed     | The expected wind speed in meter/seconds | Float  | 0.87                 |
| wind_deg       | The expected wind directions in degree   | Float  | 163                  |
| pressure       | The expected pressure in hectopascals    | Float  | 857.32               |
| sea_level      | The expected sea level pressure in hpa   | Float  | None                 |
| rainfall       | The expected rainfall volume             | Float  | 13.76                |
| snowfall       | The expected snowfall volume             | Float  | None                 |

## Forecast
To get the forecast for each day of the week, replace today with: monday, tuesday, wednesday, thursday, friday, saturday or sunday

## Note:
It is possible that some data's are not available in this case it returns None


## Synapses example

Get the current weather
```
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
          - "Today at {{ location }}, the weather is {{ current['weather_status'] }} with a temperature of{{ current['temp'] }} degrees and toomorrow the weather will be {{ tomorrow['weather_status'] }} with a temperature of {{ tomorrow['temp']}} degrees"
```

Load the location from your order
```
  - name: "getthe-weather"
    signals:
      - order: "what is the weather in {{ location }}"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          temp_unit: "celsius"
          location: "{{ location }}"
          say_template:
          - "Today in {{ location }} the weather is {{ current['weather_status'] }} with a temperature of {{ current['temp'] }} degree and tomorrow the weather will be {{ tomorrow['weather_status'] }}  with a temperature of  {{ tomorrow['temp'] }} degree"
          
```

Forecast example for monday
```
  - name: "weather-forecast-daily"
    signals:
      - order: "How is the weather on Monday"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          location: "{{ location }}"
          say_template: "The weather on Monday will be {{ monday['weather_status'] }} with temperatures from  {{ monday['min_temp'] }}  to  {{ monday['max_temp'] }} degree"
```

Forecast example for today at a given location
```
  - name: "weather-forecast-daily"
    signals:
      - order: "How will be the weather be today"
    neurons:
      - openweathermap:
          api_key: "fdfba4097c318aed7836b2a85a6a05ef"
          lang: "en"
          temp_unit: "celsius"
          location : "grenoble"
          country: "FR"
          say_template: "The weather today will be {{ today['weather_status'] }} with temperatures from  {{ today['min_temp'] }}  to  {{ today['max_temp'] }} degree"
```

## Templates example 

```
Today in {{ location }} the weather is {{ current['weather_status'] }} with a temperature of  {{ current['temp'] }} degree
```

## Template and synapse example to get the forecast of a specific day with a single synapse

You need to translate all the days in the left column to your language in lowercase

```
{% set day_of_week = {
    "your_day_translation": "today",
    "your_day_translation": "monday",
    "your_day_translation": "tuesday",
    "your_day_translation": "wednesday", 
    "your_day_translation": "thursday",
    "your_day_translation": "friday",
    "your_day_translation": "saturday", 
    "your_day_translation": "sunday"
    }[day] | default("")
-%}


{% if "today" == day_of_week %} 
The weather today will be {{ today['weather_status'] }} with temperatures from {{ today['min_temp'] }} to {{ today['max_temp'] }} degree

{% elif "monday" == day_of_week %} 
The weather on Monday will be {{ monday['weather_status'] }} with temperatures from {{ monday['min_temp'] }} to {{ monday['max_temp'] }} degree

{% elif "tuesday" == day_of_week %} 
The weather on Tuesday will be {{ tuesday['weather_status'] }} with temperatures from {{ tuesday['min_temp'] }} to {{ tuesday['max_temp'] }} degree

{% elif "wednesday" == day_of_week  %} 
The weather on Wednesday will be {{ wednesday['weather_status'] }} with temperatures from {{ wednesday['min_temp'] }} to {{ wednesday['max_temp'] }} degree

{% elif "thursday" == day_of_week  %} 
The weather on Thursday will be {{ thursday['weather_status'] }} with temperatures from {{ thursday['min_temp'] }} to {{ thursday['max_temp'] }} degree

{% elif "friday" == day_of_week  %} 
The weather on Friday will be {{ friday['weather_status'] }} with temperatures from {{ friday['min_temp'] }} to {{ friday['max_temp'] }} degree

{% elif "saturday" == day_of_week  %} 
The weather on Saturday will be  {{ saturday['weather_status'] }} with temperatures from {{ saturday['min_temp'] }} to {{ saturday['max_temp'] }} degree

{% elif "sunday" == day_of_week  %} 
The weather on Sunday will be {{ sunday['weather_status'] }} with temperatures from {{ sunday['min_temp'] }} to {{ sunday['max_temp'] }} degree

{%else %}
    I could not find that day
{% endif %}

```

```
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

## License

Copyright (c) 2016. All rights reserved.

Kalliope is covered by the MIT license, a permissive free software license that lets you do anything you want with the source code, 
as long as you provide back attribution and ["don't hold you liable"](http://choosealicense.com/). For the full license text see the [LICENSE.md](LICENSE.md) file.
