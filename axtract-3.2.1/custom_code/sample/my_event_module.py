""" This is the module docstring """
#!/opt/axtract/bin/call_with_eggs

import ax.registry


class MyEventModule(object):
    """ This is the custom event module class """
    
    def __init__(self, name, conf, global_cfg):
        self.name = name 
        self.conf = conf
        self.global_cfg = global_cfg
        self.logger = ax.registry.build_logger()
        self.logger.debug("MyEventModule.__init__(): starting...")

        self.operation = str(self.conf["name_"])
        self.values = self.conf["value"]

        self.logger.debug("MyEventModule.__init__(): finished...")

    def process_event(self, event):
        """ This is the event processing """
        self.logger.info("There's an event: %s", event)

        if self.operation == "div":
            result = int(self.values[0]) / int(self.values[1])
            self.logger.debug("Resultado: %s ", result)

        return event

    def dummy(self):
        """ This is a dummy public method """
        pass


def my_event_module_factory(name, ev_cfg, global_cfg):
    """ This is the event factory for class """
    return MyEventModule(name, ev_cfg, global_cfg)
