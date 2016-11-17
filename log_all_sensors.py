#!/usr/bin/python
import interrupt_client, MCP342X, wind_direction, HTU21D, bmp085, tgs2600, ds18b20_therm
import database # requires MySQLdb python 2 library which is not ported to python 3 yet

pressure = bmp085.BMP085()
temp_probe = ds18b20_therm.DS18B20("28-000006e169d1")
air_qual = tgs2600.TGS2600(adc_channel = 0)
int_probe = ds18b20_therm.DS18B20("28-0316710891ff")
humidity = HTU21D.HTU21D()
wind_dir = wind_direction.wind_direction(adc_channel = 0, config_file="wind_direction.json")
interrupts = interrupt_client.interrupt_client(port = 49501)

db = database.weather_database() #Local MySQL db

wind_average = wind_dir.get_value(10) #ten seconds

print("Inserting...")
db.insert(int_probe.read_temp(), temp_probe.read_temp(), air_qual.get_value(), pressure.get_pressure(), humidity.read_humidity(), wind_average, interrupts.get_wind(), interrupts.get_wind_gust(), interrupts.get_rain())
idquery = db.db.query("SELECT ID FROM WEATHER_MEASUREMENT ORDER BY ID DESC LIMIT 1")
#print(idquery[0]["ID"]) #dbg
db.db.execute("INSERT INTO oldsensor (HTtemp, idMain) VALUES (%s, %s)", (humidity.read_temperature(), idquery[0]["ID"]));
print("done")

interrupts.reset()
