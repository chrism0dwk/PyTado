import urllib
import urllib2
from cookielib import CookieJar
import json

class Tado:
    """Interacts with a Tado thermostat via public API"""

    headers = { 'Referer' : 'https://my.tado.com/' }
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.HTTPSHandler())
    api2url = 'https://my.tado.com/api/v2/homes/'

    def _api2Call(self, cmd):
        url = '%s%i/%s' % (self.api2url, self.id, cmd)
        req = urllib2.Request(url, headers=self.headers)
        response = self.opener.open(req)
        data = json.loads(response.read())
        return data

    def _setOAuthHeader(self, data):
        access_token = data['access_token']
        self.headers['Authorization'] = 'Bearer ' + access_token
        
    def loginV2(self, username, password):
        url='https://my.tado.com/oauth/token'
        data = { 'client_id' : 'tado-webapp',
                 'grant_type' : 'password',
                 'password' : password,
                 'scope' : 'home.user',
                 'username' : username }
        data = urllib.urlencode(data)
        url = url + '?' + data
        req = urllib2.Request(url, data={}, headers=self.headers)
        response = self.opener.open(req)
        self._setOAuthHeader(json.loads(response.read()))
        return response
    
    def getMe(self):
        """Gets home information"""
        url = 'https://my.tado.com/api/v2/me'
        req = urllib2.Request(url, headers=self.headers)
        response = self.opener.open(req)
        data = json.loads(response.read())
        return data

    def getState(self, zone):
        """Gets current state of Zone zone."""
        cmd = 'zones/%i/state' % zone
        data = self._api2Call(cmd)
        return data
    
    def getCapabilities(self, zone):
        """Gets current capabilities of Zone zone."""
        cmd = 'zones/%i/capabilites' % zone
        data = self._api2Call(cmd)
        return data
    
    def __init__(self, username, password):
        """Performs login and save session cookie."""
        self.loginV2(username, password)
        self.id = self.getMe()['homes'][0]['id']

    def getClimate(self, zone):
        """Gets temp (centigrade) and humidity (% RH) for Zone zone."""
        cmd = 'zones/%i/state' % zone
        data = self.getState(zone)['sensorDataPoints']
        return { 'temperature' : data['insideTemperature']['celsius'],
                 'humidity'    : data['humidity']['percentage'] }
        
