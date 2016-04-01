class Cache(object):
   __cache = {}
   __slots__ = '__cache',

   @classmethod
   def get(cls, key):
       print 'get', key
       return cls.__cache.get(key)

   @classmethod
   def set(cls, key, value):
       print 'set', key, value
       cls.__cache[key] = value

   @classmethod
   def has(cls, key):
       print 'has', key
       return key in cls.__cache

CACHE = Cache()


def cache_decorator(func):
    def wrapper(user_id):
        key = '{}-{}'.format(func.func_name, user_id)
        if CACHE.has(key):
            return CACHE.get(key)
        else:
            result = func(user_id)
            CACHE.set(key, result)
            return result
    return wrapper


def cache_decorator2(func):
    def wrapper(user_id):
        key = '{}-{}'.format(func.func_name, user_id)
        result  = CACHE.get(key)
        if not result:
            result = func(user_id)
            CACHE.set(key, result)
        return result
    return wrapper


@cache_decorator
def get_long_response(user_id):
   return user_id * 1000


@cache_decorator2
def get_long_response2(user_id):
   return user_id * 1000