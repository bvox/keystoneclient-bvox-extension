# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''BVOX Keystone client extension tests'''
##############################################################################
# Moneky patch before any import
import keystoneclient_bvox_ext as bvox_ext
bvox_ext.monkey_patch()
# End monkey patch
##############################################################################
import copy
import json
import time
import urlparse

import mox
import requests
import unittest2 as unittest

from keystoneclient.v2_0 import client
from keystoneclient.v2_0 import tenants
from keystoneclient.v2_0 import users


# This is a copy & paste from Keystone client test.utils, since they don't
# provide their test case once installed.
class TestCase(unittest.TestCase):
    TEST_TENANT_ID = '1'
    TEST_TENANT_NAME = 'aTenant'
    TEST_TOKEN = 'aToken'
    TEST_USER = 'test'
    TEST_ROOT_URL = 'http://127.0.0.1:5000/'
    TEST_URL = '%s%s' % (TEST_ROOT_URL, 'v2.0')
    TEST_ROOT_ADMIN_URL = 'http://127.0.0.1:35357/'
    TEST_ADMIN_URL = '%s%s' % (TEST_ROOT_ADMIN_URL, 'v2.0')

    TEST_SERVICE_CATALOG = [{
        "endpoints": [{
            "adminURL": "http://cdn.admin-nets.local:8774/v1.0",
            "region": "RegionOne",
            "internalURL": "http://127.0.0.1:8774/v1.0",
            "publicURL": "http://cdn.admin-nets.local:8774/v1.0/"
        }],
        "type": "nova_compat",
        "name": "nova_compat"
    }, {
        "endpoints": [{
            "adminURL": "http://nova/novapi/admin",
            "region": "RegionOne",
            "internalURL": "http://nova/novapi/internal",
            "publicURL": "http://nova/novapi/public"
        }],
        "type": "compute",
        "name": "nova"
    }, {
        "endpoints": [{
            "adminURL": "http://glance/glanceapi/admin",
            "region": "RegionOne",
            "internalURL": "http://glance/glanceapi/internal",
            "publicURL": "http://glance/glanceapi/public"
        }],
        "type": "image",
        "name": "glance"
    }, {
        "endpoints": [{
            "adminURL": "http://127.0.0.1:35357/v2.0",
            "region": "RegionOne",
            "internalURL": "http://127.0.0.1:5000/v2.0",
            "publicURL": "http://127.0.0.1:5000/v2.0"
        }],
        "type": "identity",
        "name": "keystone"
    }, {
        "endpoints": [{
            "adminURL": "http://swift/swiftapi/admin",
            "region": "RegionOne",
            "internalURL": "http://swift/swiftapi/internal",
            "publicURL": "http://swift/swiftapi/public"
        }],
        "type": "object-store",
        "name": "swift"
    }]

    def setUp(self):
        super(TestCase, self).setUp()
        self.mox = mox.Mox()
        self._original_time = time.time
        time.time = lambda: 1234
        requests.request = self.mox.CreateMockAnything()
        self.client = client.Client(username=self.TEST_USER,
                                    token=self.TEST_TOKEN,
                                    tenant_name=self.TEST_TENANT_NAME,
                                    auth_url=self.TEST_URL,
                                    endpoint=self.TEST_URL)

    def tearDown(self):
        time.time = self._original_time
        super(TestCase, self).tearDown()
        self.mox.UnsetStubs()
        self.mox.VerifyAll()


class TestResponse(requests.Response):
    """ Class used to wrap requests.Response and provide some
        convenience to initialize with a dict """

    def __init__(self, data):
        self._text = None
        super(TestResponse, self)
        if isinstance(data, dict):
            self.status_code = data.get('status_code', None)
            self.headers = data.get('headers', None)
            # Fake the text attribute to streamline Response creation
            self._text = data.get('text', None)
        else:
            self.status_code = data

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @property
    def text(self):
        return self._text


class BvoxExtTests(TestCase):
    '''Tests our extension.'''
    # Copy & paste from Keystone client tests.v2_0.test_(users|tenants)
    def setUp(self):
        super(BvoxExtTests, self).setUp()
        self.TEST_REQUEST_HEADERS = {
            'X-Auth-Token': 'aToken',
            'User-Agent': 'python-keystoneclient',
        }

        self.TEST_REQUEST_BASE = {
            'config': {'danger_mode': False},
            'verify': True,
        }

        self.TEST_USERS = {
            "users": {
                "values": [
                    {
                        "email": "admin@example.com",
                        "enabled": True,
                        "id": 1,
                        "name": "admin",
                    },
                ]
            }
        }

        self.TEST_TENANTS = {
            "tenants": {
                "values": [
                    {
                        "enabled": True,
                        "description": "None",
                        "name": "admin",
                        "id": 1,
                    }
                ],
                "links": [],
            },
        }

    def test_get_user_by_name(self):
        resp = TestResponse({
            "status_code": 200,
            "text": json.dumps({
                'user': self.TEST_USERS['users']['values'][0],
            })
        })

        kwargs = copy.copy(self.TEST_REQUEST_BASE)
        kwargs['headers'] = self.TEST_REQUEST_HEADERS

        requests.request(
            'GET',
            urlparse.urljoin(self.TEST_URL, 'v2.0/BVOX/users?name=admin'),
            **kwargs).AndReturn((resp))

        self.mox.ReplayAll()

        u = self.client.users.get_by_name('admin')
        self.assertTrue(isinstance(u, users.User))
        self.assertEqual(u.id, 1)
        self.assertEqual(u.name, 'admin')
        self.assertEqual(u.email, 'admin@example.com')

    def test_get_tenant_by_name(self):
        resp = TestResponse({
            "status_code": 200,
            "text": json.dumps({
                'tenant': self.TEST_TENANTS['tenants']['values'][0],
            }),
        })

        kwargs = copy.copy(self.TEST_REQUEST_BASE)
        kwargs['headers'] = self.TEST_REQUEST_HEADERS

        requests.request(
            'GET',
            urlparse.urljoin(self.TEST_URL, 'v2.0/BVOX/tenants?name=admin'),
            **kwargs).AndReturn((resp))

        self.mox.ReplayAll()

        t = self.client.tenants.get_by_name('admin')
        self.assertTrue(isinstance(t, tenants.Tenant))
        self.assertEqual(t.id, 1)
        self.assertEqual(t.name, 'admin')


if __name__ == '__main__':
    unittest.main()
