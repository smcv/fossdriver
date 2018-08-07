# Copyright The Linux Foundation
# SPDX-License-Identifier: BSD-3-Clause

import json

class FossConfig(object):

    def __init__(self):
        self.serverUrl = ""
        self.username = ""
        self.password = ""

    def configure(self, configFilename):
        try:
            with open(configFilename, "r") as f:
                js = json.load(f)

                # pull out the expected parameters
                self.serverUrl = js.get("serverUrl", "")
                self.username = js.get("username", "")
                self.password = js.get("password", "")

                # check whether we got everything we expected
                isValid = True
                if self.serverUrl == "":
                    print(f"serverUrl not found in config file")
                    isValid = False
                if self.username == "":
                    print(f"username not found in config file")
                    isValid = False
                if self.password == "":
                    print(f"password not found in config file")
                    isValid = False

                return isValid

        except json.decoder.JSONDecodeError as e:
            print(f"Error loading or parsing {configFilename}: {str(e)}")
            return False
