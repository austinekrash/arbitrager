import importlib
from .exchange import Exchange

class ExchangeFactory:
    factories = {}

    @staticmethod
    def get(name, **kwargs):
        for ex in ExchangeFactory.list_exchanges():
            if ex.__name__.lower() == name.lower():
                return( ex(**kwargs) )
        raise NameError("Exchange {} is not currently supported.".format(name))

    @staticmethod
    def list_exchanges():
        return(Exchange.__subclasses__())

    @staticmethod
    def get_names():
        return([ex.__name__.lower() for ex in ExchangeFactory.list_exchanges()])