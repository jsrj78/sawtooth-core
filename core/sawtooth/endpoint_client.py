# Copyright 2016 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

from sawtooth.client import SawtoothClient


class EndpointClient(SawtoothClient):
    """
    The EndpointClient is not like other SawtoothClient-derived
    classes in that it doesn't (currently) support actually performing
    transactions on the EndpointRegistryTransaction store.  It is a read-only
    client.

    Its main purpose in life is to make it easy to discover the validators in
    the network, or maybe more precisely, the list of endpoints that have
    registered with a validator.
    """
    def __init__(self, base_url):
        super(EndpointClient, self).__init__(
            base_url=base_url,
            store_name='EndpointRegistryTransaction',
            name='EndpointClient',
            txntype_name='/EndpointRegistryTransaction',
            msgtype_name='/ledger.transaction.EndpointRegistry/Transaction')

    def get_endpoint_list(self):
        """
        Retrieves the endpoint list from the validator.

        Args:
            N/A

        Returns:
            A list of endpoints.  Each endpoint is an OrderedDict of values
            from EndpointRegistryTransaction.
        """

        return [endpoint for endpoint in
                self.get_all_store_objects().itervalues()]

    def get_validator_url_list(self):
        """
        A convenience function that is a specialization of endpoint_list that
        extracts the 'Host' and 'HttpPort' values for each endpoint and
        concatenates them to make a list of validator URLs.

        Args:
            N/A

        Returns:
            A list of validator URLS, for example
            ['http://127.0.0.1:8800', ...]
        """

        # Rely upon base endpoint list fetch and simply create a new list
        # of validator URLs (i.e., the concatenation of host and HTTP port)
        return ['http://{0}:{1}'.format(e['Host'], e['HttpPort']) for e
                in self.get_endpoint_list()
                if 'HttpPort' in e and e['HttpPort'] != 0]
