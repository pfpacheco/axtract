#!/opt/axtract/bin/call_with_eggs

from ax.eventing.events import timer_event_factory
import logging
import time


class HelloFromAxtract(object):

    def __init__(self, caller, name, config, index, chain=None):
        """ This is the init method """
        # When you use this skeleton, move these imports to the top of the file.

        self.logger = logging.getLogger("%s.%s" % (__name__, name))
        self.logger.debug("HelloFromAxtract.__init__: starting...")

        # convert the config objects into a python dictionary
        config = {item['name_']: item['value'] for item in config.values()}

        self.caller = caller
        self.name = name
        self.config = config
        self.index = index
        self.ev_mod_chain = chain
        self.logger.debug("HelloFromAxtract.__init__: finished.")

    def run(self):
        self.logger.debug("HelloFromAxtract.run: starting...")

        while not self.caller.shutdown_requested:
            try:
                time.sleep(1)
                event = timer_event_factory(self.name)
                self.ev_mod_chain.run(event)
            except Exception as ex:
                self.logger.exception("Error while doing eternal loop: %s", str(ex))
            else:
                self.logger.debug("Event successfully created and processed")

            self.logger.debug("Message: %s", self.config.get("the_hello"))

        self.logger.debug("HelloFromAxtract.run: finished.")


def hello_from_axtract_factory(caller, name, config, index, chain=None):
    """ This is the standard factory name for hello """
    return HelloFromAxtract(caller, name, config, index, chain=chain)
