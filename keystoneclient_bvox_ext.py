# vim: tabstop=4 shiftwidth=4 softtabstop=4
'''OpenStack Keystone client BVOX extension.'''
import functools

from keystoneclient import utils
from keystoneclient.v2_0 import shell as v2_shell
from keystoneclient.v2_0 import tenants
from keystoneclient.v2_0 import users


@utils.arg('--by_name', required=False, action='store_true',
           help='The user identifier is treated as a username.')
@utils.arg('--by_email', required=False, action='store_true',
           help='The user identifier is treated as an email.')
@utils.arg('id', metavar='<user-identifier>',
           help='Identifies the user to display (user ID, by default).')
def do_user_get(kclient, args):
    """Display user details."""
    if args.by_name:
        user = kclient.users.get_by_name(args.id)
    elif args.by_email:
        user = kclient.users.get_by_email(args.id)
    else:
        user = kclient.users.get(args.id)
    utils.print_dict(user._info)


@utils.arg('--by_name', required=False, action='store_true',
           help='The tenant identifier is treated as a tenant name.')
@utils.arg('id', metavar='<tenant-identifier>',
           help='Identifies the tenant to display (tenant ID, by default).')
def do_tenant_get(kclient, args):
    """Display tenant details"""
    if args.by_name:
        tenant = kclient.tenants.get_by_name(args.id)
    else:
        tenant = kclient.tenants.get(args.id)
    utils.print_dict(tenant._info)


def user_get_by_name(self, user_name):
    '''Gets user by given name.'''
    return self._get('/BVOX/users?name=%s' % user_name, 'user')


def user_get_by_email(self, user_email):
    '''Gets user by given email.'''
    return self._get('/BVOX/users?email=%s' % user_email, 'user')


def tenant_get_by_name(self, tenant_name):
    '''Gets tenant by given name.'''
    return self._get('/BVOX/tenants?name=%s' % tenant_name, 'tenant')


##############################################################################
# Monkey patch keystone client
def monkey_patch():
    '''Monkey patchs python-keystoneclient v2.0 API.'''
    v2_shell.do_user_get = do_user_get
    v2_shell.do_tenant_get = do_tenant_get
    users.UserManager.get_by_name = user_get_by_name
    users.UserManager.get_by_email = user_get_by_email
    tenants.TenantManager.get_by_name = tenant_get_by_name
# End monkey patch
##############################################################################


def with_monkey_patch(func):
    '''Wraps `func` monkey patching python-keystoneclient first.'''
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        '''Real decorator.'''
        monkey_patch()
        return func(*args, **kwargs)
    return decorator

from keystoneclient import shell
MAIN = with_monkey_patch(shell.main)
