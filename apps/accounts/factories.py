from django.contrib.auth.models import User
import factory
from .models import UserProfile


class UserFactory(factory.Factory):
    FACTORY_FOR = User

    first_name = factory.Sequence(lambda n: u'Student %s' % n)
    username = factory.Sequence(lambda n: u'student%s' % n)
    email = factory.Sequence(lambda n: u'user%s@pikaland.com' % n)


class UserProfileFactory(factory.Factory):
    FACTORY_FOR = UserProfile

    bio = factory.Sequence(lambda n: 'Profile {0}'.format(n))
