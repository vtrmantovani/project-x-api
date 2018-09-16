#!/usr/bin/env python
import sys

from flask_script import Manager

from pxa import create_app

app = create_app()

manager = Manager(app)


@manager.option('-u', dest='user', help='User name')
@manager.option('-e', dest='environment', help='Environment name [Development | Staging | Production]')  # noqa
def generate_api_key(environment, user):
    if environment not in ['Development', 'Staging', 'Production']:
        print('Invalid environment')
        sys.exit(1)

    from itsdangerous import TimestampSigner
    from pxa import config

    config_env = getattr(config, '{0}Config'.format(environment))

    signer = TimestampSigner(config_env.SIGNER_KEY)
    print('APIKEY: {0}'.format(signer.sign(user)))


if __name__ == '__main__':
    manager.run()
