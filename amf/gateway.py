# -*- coding: utf-8 -*-

import pyamf, json
from  pyamf.remoting.gateway.django import DjangoGateway
from  django.http import HttpResponse

from vo import makeVo, CardVO, HeroVO
import card
import hero


pyamf.register_class(CardVO, 'CardVO')

pyamf.register_class(HeroVO, 'HeroVO')

services = {
    "cardService.getAllCards":card.CardService.getAllCards, 
	
	#"heroService.getAllHeros":hero.HeroService.getAllHeros,

	"heroService.createUserHeros":hero.HeroService.createUserHeros,
	"heroService.updateUserHeros":hero.HeroService.updateUserHeros,
	"heroService.getAllSystemAndUserHeros":hero.HeroService.getAllSystemAndUserHeros,
	"heroService.deleteUserHeros": hero.HeroService.deleteUserHeros,
}
gateway = DjangoGateway(services, expose_request=False, debug=True)

