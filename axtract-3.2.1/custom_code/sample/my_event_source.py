#!/opt/axtract/bin/call_with_eggs

from ax.eventing.events import timer_event_factory
import logging
import time


class MyEventSource(object):
    """ This is the HelloFromAxtract source event class """

    def __init__(self, caller, name, config, index, chain=None):
        """ This is the init method """

        # When you use this skeleton, move these imports to the top of the file.

        self.logger = logging.getLogger("%s.%s" % (__name__, name))
        self.logger.debug("MyEventSource.__init__: starting...")

        # convert the config objects into a python dictionary
        config = {item["operation"]: item["values"] for item in config.values()}

        self.caller = caller
        self.name = name
        self.config = config
        self.index = index
        self.ev_mod_chain = chain
        self.logger.debug("MyEventSource.__init__: finished.")

    def run(self):
        """ This is the run method and must be overri """

        self.logger.debug("MyEventSource.run: starting...")

        while not self.caller.shutdown_requested:
            try:
                time.sleep(1)
                event = timer_event_factory(self.name)
                self.ev_mod_chain.run(event)
            except Exception as ex:
                self.logger.exception("Error while doing eternal loop: %s", str(ex))
            else:
                self.logger.debug("Event successfully created and processed")

            self.logger.debug("Operation: %s and %s" % (self.config.get("operation"), self.config.get("values")))

        self.logger.debug("MyEventSource.run: finished.")


def my_event_source_factory(caller, name, config, index, chain=None):
    """ This is the standard factory name for hello """
    return MyEventSource(caller, name, config, index, chain=chain)
