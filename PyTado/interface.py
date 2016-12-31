import urllib.request, urllib.parse, urllib.error

from http.cookiejar import CookieJar

import json


class Tado:
    """Interacts with a Tado thermostat via public API.
    Example usage: t = Tado('me@somewhere.com', 'mypasswd')
                   t.getClimate(1) # Get climate, zone 1.
    """
    # Instance-wide constant info
    headers = { 'Referer' : 'https://my.tado.com/' }
    api2url = 'https://my.tado.com/api/v2/homes/'
    mobi2url = 'https://my.tado.com/mobile/1.9/'


    # 'Private' methods for use in class, Tado mobile API V1.9.
    def _mobile_apiCall(self, cmd):
        url = '%s%s' % (self.mobi2url, cmd)
        req = urllib.request.Request(url, headers=self.headers)
        response = self.opener.open(req)
        str_response = response.read().decode('utf-8')
        data = json.loads(str_response)
        return data

    # 'Private' methods for use in class, Tado API V2.
    def _apiCall(self, cmd):
        url = '%s%i/%s' % (self.api2url, self.id, cmd)
        req = urllib.request.Request(url, headers=self.headers)
        response = self.opener.open(req)
        str_response = response.read().decode('utf-8')
        data = json.loads(str_response)
        return data

    def _setOAuthHeader(self, data):
        access_token = data['access_token']
        self.headers['Authorization'] = 'Bearer ' + access_token
        
    def _loginV2(self, username, password):
        url='https://my.tado.com/oauth/token'
        data = { 'client_id' : 'tado-webapp',
                 'grant_type' : 'password',
                 'password' : password,
                 'scope' : 'home.user',
                 'username' : username }
        data = urllib.parse.urlencode(data)
        url = url + '?' + data
        req = urllib.request.Request(url, data=json.dumps({}).encode('utf8'), method='POST',
                                 headers={'Content-Type': 'application/json', 'Referer' : 'https://my.tado.com/'})
        
        response = self.opener.open(req)
        str_response = response.read().decode('utf-8')
        self._setOAuthHeader(json.loads(str_response))
        return response
    
    # Public interface
    def getMe(self):
        """Gets home information."""
        url = 'https://my.tado.com/api/v2/me'
        req = urllib.request.Request(url, headers=self.headers)
        response = self.opener.open(req)
        str_response = response.read().decode('utf-8')
        data = json.loads(str_response)
        return data
    
    def getDevices(self):
        """Gets device information."""
        cmd = 'devices'
        data = self._apiCall(cmd)
        return data

    def getZones(self):
        """Gets zones information."""
        cmd = 'zones'
        data = self._apiCall(cmd)
        return data

    def getState(self, zone):
        """Gets current state of Zone zone."""
        cmd = 'zones/%i/state' % zone
        data = self._apiCall(cmd)
        return data
    
    def getCapabilities(self, zone):
        """Gets current capabilities of Zone zone."""
        cmd = 'zones/%i/capabilities' % zone
        data = self._apiCall(cmd)
        return data

    def getClimate(self, zone):
        """Gets temp (centigrade) and humidity (% RH) for Zone zone."""
        cmd = 'zones/%i/state' % zone
        data = self.getState(zone)['sensorDataPoints']
        return { 'temperature' : data['insideTemperature']['celsius'],
                 'humidity'    : data['humidity']['percentage'] }

    def getWeather(self):
        """Gets outside weather data"""
        cmd = 'weather'
        data = self._apiCall(cmd)
        return data

    def getAppUsers(self):
        """Gets getAppUsers data"""
        cmd = 'getAppUsers'
        data = self._mobile_apiCall(cmd)
        return data

    def getAppUsersRelativePositions(self):
        """Gets getAppUsersRelativePositions data"""
        cmd = 'getAppUsersRelativePositions'
        data = self._mobile_apiCall(cmd)
        return data

    # Ctor
    def __init__(self, username, password):
        """Performs login and save session cookie."""
        # HTTPS Interface
        cj = CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cj),
            urllib.request.HTTPSHandler())
        self._loginV2(username, password)
        self.id = self.getMe()['homes'][0]['id']
