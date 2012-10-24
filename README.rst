BVOX Keystone client extension
==============================

BVOX extension for Openstack Keystone client right now just implements
get_by_name and get_by_email for users and get_by_name for tenants. This
expects Keystone BVOX extension to be installed on Keystone server.


Python API
----------

In order to use the client library a monkey patch is provided::

   >>> from keystoneclient_bvox_ext import monkey_patch
   >>> monkey_patch()
   >>> from keystoneclient.v2_0 imoprt client
   >>> cli = client.Client(username='admin', password='secrete', tenant_name='admin', auth_url='http://localhost:35357/v2.0')
   >>> cli.users.get_by_name('demo')
   <User {u'id': u'74439b8d264545a19f76a0c0d379457e', u'tenantId': u'', u'enabled': True, u'name': u'demo', u'email': u'demo@example.com'}>
   >>> cli.users.get_by_email('demo@example.com')
   <User {u'id': u'74439b8d264545a19f76a0c0d379457e', u'tenantId': u'', u'enabled': True, u'name': u'demo', u'email': u'demo@example.com'}>
   >>> cli.tenants.get_by_name('demo')
   <Tenant {u'id': u'98ecc4b79d044d76b5597f2d7aa0e3c7', u'enabled': True, u'name': u'demo'}>

Command line API
----------------

Installing this package gets you a shell command, *keystone-bvox*, that you can
use to interact with Keystone's Identity API. The shell command is a thin
wrapper over *keystone* shell, just applying the monkey patching, so you can
use it as usual with some extra arguments for ``user-get`` and ``tenant-get``
subcommands::

  $ keystone-bvox help user-get
  usage: keystone user-get [--by_name] [--by_email] <user-identifier>

  Display user details.

  Positional arguments:
    <user-identifier>  Identifies the user to display (user ID, by default).

  Optional arguments:
    --by_name          The user identifier is treated as a username.
    --by_email         The user identifier is treated as an email.

  $ keystone-bvox help tenant-get
  usage: keystone tenant-get [--by_name] <tenant-identifier>

  Display tenant details

  Positional arguments:
    <tenant-identifier>  Identifies the tenant to display (tenant ID, by
                         default).

  Optional arguments:
    --by_name            The tenant identifier is treated as a tenant name.
