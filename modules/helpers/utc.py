# from pytz import timezone
# from datetime import datetime

# format = "%Y-%m-%d %H:%M:%S %Z%z"

# # Current time in UTC
# now_utc = datetime.now(timezone('UTC'))
# print(now_utc.strftime(format))

# # Convert to Asia/Kolkata time zone
# now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
# print(now_asia.strftime(format))

# import pytz
  
  
# print('the supported timezones by the pytz module:',
#       pytz.all_timezones, '\n')

# argentina = ['America/Argentina/Buenos_Aires', 'America/Argentina/Catamarca', 'America/Argentina/ComodRivadavia', 'America/Argentina/Cordoba', 'America/Argentina/Jujuy', 'America/Argentina/La_Rioja', 'America/Argentina/Mendoza', 'America/Argentina/Rio_Gallegos', 'America/Argentina/Salta', 'America/Argentina/San_Juan', 'America/Argentina/San_Luis', 'America/Argentina/Tucuman', 'America/Argentina/Ushuaia']

from datetime import datetime
import pytz
# getting utc timezone
utc_time = pytz.utc
 
# getting timezone by name
arg_time = pytz.timezone('America/Argentina/Buenos_Aires')
us_time = pytz.timezone('US/Michigan') 
# getting datetime of specified timezone
print('Datetime of UTC Time-zone: ', datetime.now(tz=utc_time))
print('Datetime of IST Time-zone: ', datetime.now(tz=arg_time))
print('Datetime of EST Time-zone: ', datetime.now(tz=us_time))

hora_arg = datetime.now(tz=arg_time)
hora_us = datetime.now(tz=us_time)

print('Hora US Michigan', hora_us.astimezone(utc_time))
print('Hora Argentina', hora_arg.astimezone(utc_time))

#paso la hora argentina a utc

