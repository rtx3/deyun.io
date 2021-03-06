import requests
import logging
import os
import datetime
logger = logging.getLogger('api')
logger.setLevel(20)

class IndbException(Exception):
    pass


class Indb(object):

    def __init__(self, api_url='https://localhost:8086'):

        self.api_url = api_url

    def test(self):
        url = self.api_url + '/query?q=SHOW+DATABASES&db=_internal'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {'url': url,
                  'headers': headers,
                  'verify': False,
                  }
        try:
            resp = requests.get(**params)
            if resp.status_code == 401:
                raise IndbException(str(resp.status_code) +
                                    ':Authentication denied')
                return

            if resp.status_code == 500:
                raise IndbException(str(resp.status_code) + ':Server error.')
                return

            if resp.status_code == 404:
                raise IndbException(str(resp.status_code) +
                                    ' :This request returns nothing.')
                return
        except IndbException as e:
            logger.error('Error with request: {0}'.format(e))
            return
        logger.info('Test Comlpeted with sucess.')
        return resp.json()

    def get_hosts(self, table, db):

        url = self.api_url + '/query?q=SHOW+TAG+VALUES+FROM+%22' + \
            table + '%22+WITH+KEY+%3D+%22host%22&db=' + db
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {'url': url,
                  'headers': headers,
                  'verify': False,
                  }
        try:
            resp = requests.get(**params)
            if resp.status_code == 401:
                raise IndbException(str(resp.status_code) +
                                    ':Authentication denied')
                return

            if resp.status_code == 500:
                raise IndbException(str(resp.status_code) + ':Server error.')
                return

            if resp.status_code == 404:
                raise IndbException(str(resp.status_code) +
                                    ' :This request returns nothing.')
                return
        except IndbException as e:
            logger.error('Error with request: {0}'.format(e))
            return
        data =  resp.json()
        return data['results'][0]['series'][0]['values']

    def get_sync_data(self, table,time='55m', interval='1h'):
        #url = self.api_url + '/query?q=SELECT+MEAN(value)+FROM+' + table + '++WHERE+time+%3E+now()+-+' + time +'+and+host+%3D\'' + host + '\'+GROUP+BY+host%2Ctime(' + interval + ')+limit+1&db=graphite'
        url = self.api_url + '/query?q=SELECT+MEAN(value)+FROM+' + table + '++WHERE+time+%3E+now()+-+' + time + '++GROUP+BY+host%2Ctime(' + interval + ')+limit+1&db=graphite' 
        #http://123.56.195.220:8086/query?q=SELECT+MEAN(value)+FROM+cpu_system++WHERE+time+%3E+now()+-+12h+GROUP+BY+host%2Ctime(1h)&db=graphite
        #http://123.56.195.220:8086/query?q=SELECT+MEAN(value)+FROM+cpu_system++WHERE+time+%3E+now()++-+55m+and+host+%3D+'do.docker.us01'++GROUP+BY+time(60m)+limit+1&db=graphite
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {'url': url,
          'headers': headers,
          'verify': False,
          }
        try:
            resp = requests.get(**params)
        except Exception as e:
            logger.error('Error with request ' + url + ': {0}'.format(e))
            return e
        data = resp.json()
        try:
            logger.info({'ok':data})
            return data['results'][0]['series']
        except Exception as e:
            logger.error('Error with request ' + url + 'data:' + str(data) + ': {0}'.format(e))
            return None

        


    def get_data(self, table, db, host):

        url = self.api_url + '/query?q=select+*+from+' + \
            table + '++where++host+%3D\'' + host + '\'&db=' + db
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {'url': url,
                  'headers': headers,
                  'verify': False,
                  }
        try:
            resp = requests.get(**params)
            if resp.status_code == 401:
                raise IndbException(str(resp.status_code) +
                                    ':Authentication denied')
                return

            if resp.status_code == 500:
                raise IndbException(str(resp.status_code) + ':Server error.')
                return

            if resp.status_code == 404:
                raise IndbException(str(resp.status_code) +
                                    ' :This request returns nothing.')
                return
        except IndbException as e:
            logger.error('Error with request: {0}'.format(e))
            return
        return resp.json()

    def get_data_24h(self, table, db, host):
        url = self.api_url + '/query?q=select+*+from+' + table + \
            '+++where+time+%3E+now()+-+1d+and+host+%3D\'' + host + '\'&db=' + db
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {'url': url,
                  'headers': headers,
                  'verify': False,
                  }
        try:
            resp = requests.get(**params)
            if resp.status_code == 401:
                raise IndbException(str(resp.status_code) +
                                    ':Authentication denied')
                return

            if resp.status_code == 500:
                raise IndbException(str(resp.status_code) + ':Server error.')
                return

            if resp.status_code == 404:
                raise IndbException(str(resp.status_code) +
                                    ' :This request returns nothing.')
                return
        except IndbException as e:
            logger.error('Error with request: {0}'.format(e))
            return
        return resp.json()

    def get_data_24h_groupbytime(self, table, db, host):
        #data = self.get_data_24h(table, db, host)
        # http://123.56.195.220:8086/query?q=select+mean(value)+from+memory_percent_usedWOBuffersCaches+++where+time+%3E+now()+-+1d+and+host+%3D'Ali.master.cn00'+GROUP+BY+time(3h)&db=graphite
        url = self.api_url + '/query?q=select+mean(value)+from+' + table + \
            '+++where+time+%3E+now()+-+1d+and+host+%3D\'' + host + \
            '\'+GROUP+BY+time(1h)&db=' + db
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
        }
        params = {'url': url,
                  'headers': headers,
                  'verify': False,
                  }
        try:
            resp = requests.get(**params)
            if resp.status_code == 401:
                raise IndbException(str(resp.status_code) +
                                    ':Authentication denied')
                return

            if resp.status_code == 500:
                raise IndbException(str(resp.status_code) + ':Server error.')
                return

            if resp.status_code == 404:
                raise IndbException(str(resp.status_code) +
                                    ' :This request returns nothing.')
                return
        except IndbException as e:
            logger.error('Error with request: {0}'.format(e))
            return
        return resp.json()

    def ret_point_24h(self, table, db, host):
        ret = self.get_data_24h_groupbytime(table, db, host)
        data = ret['results'][0]['series'][0]['values']
        list_date = []
        list_lable = []
        if data == None:
            return [list_lable,list_date]
        for item in data:
            timea = item[0]
            timeArray = datetime.datetime.strptime(
                timea, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(seconds=60 * 60 * 8)
            timeo = timeArray.strftime("%H%M-%d")
            item[0] = timeo
           # item[1] = round(item[1], 2)
            if item[1] == None:
                item[1] = 0.00
            else:
                item[1] = '{:.2f}'.format(item[1])
            list_date.append(timeo)
            list_lable.append(item[1])
        result = [list_lable,list_date]
        return result


