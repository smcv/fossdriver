# Copyright The Linux Foundation
# SPDX-License-Identifier: BSD-3-Clause
#
# Based in significant part on fossup from Togán Labs,
# https://gitlab.com/toganlabs/fossup, with the following copyright notice:
#
# Copyright (C) 2016-2018, Togan Labs Ltd. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import requests
import urllib
import logging
import time
import bs4
from requests_toolbelt.multipart.encoder import MultipartEncoder

class FossServer(object):

    def __init__(self, config):
        # connection data
        self.config = config
        self.session = requests.Session()

    def _get(self, endpoint):
        """Helper function: Make a GET call to the Fossology server."""
        url = self.config.serverUrl + endpoint
        r = self.session.get(url)
        logging.debug("GET: " + url + " " + str(r))
        return r

    def _post(self, endpoint, values):
        """Helper function: Make a POST call to the Fossology server."""
        url = self.config.serverUrl + endpoint
        data = values
        r = self.session.post(url, data=data)
        logging.debug("POST: " + url + " " + str(r))

    def _postFile(self, endpoint, values):
        """Helper function: Make a POST call to the Fossology server with multipart data."""
        url = self.config.serverUrl + endpoint
        data = MultipartEncoder(fields=values)
        headers = {
            'Content-Type': data.content_type,
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'Referer': url,
        }
        # FIXME is this next line necessary?
        # cookies = self.session.cookies.get_dict()

        r = self.session.post(url, data=data, headers=headers)
        logging.debug("POST (file): " + url + " " + str(r))

    def Login(self):
        """Log in to Fossology server. Should be the first call made."""
        endpoint = "/?mod=auth"
        values = {
            "username": self.config.username,
            "password": self.config.password,
        }
        self._post(endpoint, values)
        # FIXME check for success?

    def GetFolderNum(self, folderName):
        """Find folder ID number for given folder name from Fossology server."""
        # retrieve from upload_file, since that provides the list of all folders
        endpoint = "/?mod=upload_file"
        results = self._get(endpoint)
        c = results.content
        soup = bs4.BeautifulSoup(c, "lxml")
        folders = soup.findAll("select", {"name":"folder"})
        if folders is None:
            return None
        for folder in folders:
            for option in folder.findAll("option"):
                if option.text.strip() == folderName:
                    return option["value"]
        return None
