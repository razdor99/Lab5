#!/usr/bin/python37all
import cgi
import cgitb
import json
cgitb.enable()

data = cgi.FieldStorage()

s1 = data.getvalue('slider1')
button = data.getvalue('button')

data = {"slider1":s1,"button":button}
with open('stepper.txt', 'w') as f:
  json.dump(data,f)


print('Content-type: text/html\n\n')
print('<html>')
print('<form action="/cgi-bin/led-pwm.py" method="POST">')
print('<input type="range" name="slider1" min ="0" max="360" value ="0"><br>')
print('<input type="submit" name="button" value="Change Angle">')
print('<input type="submit" name="button" value="Zero">')
print('<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1555747/widgets/375153"></iframe>')
print('<iframe width="450" height="260" style="border: 1px solid #cccccc;" src="https://thingspeak.com/channels/1555747/charts/1?bgcolor=%23ffffff&color=%23d62020&dynamic=true&results=60&type=line&update=15"></iframe>')
print('</form>')
print('</html>')