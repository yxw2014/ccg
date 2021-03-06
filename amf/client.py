import logging
	
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)

from pyamf.remoting.client import RemotingService

url = 'http://127.0.0.1:8800/gateway'
gw = RemotingService(url, logger=logging)

service = gw.getService('cardService')

service2 = gw.getService('heroService')

#print service.getAllCards()
#print service2.getAllHeros()

print service.getAllCards(['51'])

#print service2.getAllSystemAndUserHeros(['51'])
