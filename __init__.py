# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.


# Visit https://docs.mycroft.ai/skill.creation for more detailed information
# on the structure of this skill and its containing folder, as well as
# instructions for designing your own skill based on this template.


# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import requests
import json
import re
import os

__author__ = 'brihopki'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)

# Function to get wait time
def get_wait_time(airport, api_key):
    # Getting the wait times for the airport code and getting the airport codes api so we can get the full airport
    # name for the response back
    LOGGER.debug("This is the api key from the function: {}".format(api_key))
    r_wait_times = requests.get('http://apps.tsa.dhs.gov/MyTSAWebService/GetTSOWaitTimes.ashx?ap=' + airport, verify=False)
    r_airport_codes = requests.get('https://iatacodes.org/api/v6/airports?api_key=' + api_key, verify=False)

    if r_wait_times.status_code != 200:
        return ("Cannot find {} airport code".format(airport))

    # Getting json format of the airport codes
    json_airport_codes = r_airport_codes.json()
    response = json_airport_codes['response']

    # Looping through airport codes finding the code we were spoken/manually set then using that to get full name
    for code in response:
        if airport == code['code']:
            airport_name = code['name']

    # Setting the output from the response text, then matching for wait times and taking first match for the response
    output = r_wait_times.text
    matchObj = re.search(r'<WaitTime>(\d+)</WaitTime>', output)
    current_wait_raw = matchObj.group()
    wait_time = re.search(r'(\d+)', current_wait_raw)
    LOGGER.debug(wait_time)
    # Simple if condition setting the minute to minutes if its greater than 1.
    if wait_time <= '1':
        output = ("The current wait time at {} is {} minute".format(airport_name, wait_time.group(1)))
    else:
        output = ("The current wait time at {} is {} minutes".format(airport_name, wait_time.group(1)))

    return output

# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class TsaWaitSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(TsaWaitSkill, self).__init__(name="TsaWaitSkill")
        self.api_key = self.config.get("airport_api_key")

    # This method loads the files needed for the skill's functioning, and
    # creates and registers each intent that the skill uses
    def initialize(self):
        self.load_data_files(dirname(__file__))

        wait_time_intent = IntentBuilder("WaitTimeIntent").\
            require("TsaWaitKeyword").optionally("Airport").build()
        self.register_intent(wait_time_intent, self.handle_wait_time_intent)


    # The "handle_xxxx_intent" functions define Mycroft's behavior when
    # each of the skill's intents is triggered: in this case, he simply
    # speaks a response. Note that the "speak_dialog" method doesn't
    # actually speak the text it's passed--instead, that text is the filename
    # of a file in the dialog folder, and Mycroft speaks its contents when
    # the method is called.
    def handle_wait_time_intent(self, message):
        airport = message.data["Airport"]
        LOGGER.debug("Airport Code is: %s" % airport)
        wait_time = get_wait_time(airport.upper(), self.api_key)
        self.speak(wait_time)


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return TsaWaitSkill()
