import hashlib
import datetime


# Create a random string based on timestamp
# Don't overload your system over get_random_string(1000000)
def get(length=8, prefix='', suffix='', invalid_chars=False):
    u = ''
    if (not isinstance(length, int)) or length < 4:
        length = 8
    while True:
        if len(u) < length:
            the_moment = str(datetime.datetime.now()).encode('utf-8')
            salt = hashlib.sha256(the_moment).hexdigest().encode('utf-8')
            u += hashlib.sha1(salt).hexdigest()
        else:
            break
    if invalid_chars and isinstance(invalid_chars, str):
        for ch in invalid_chars:
            u = u.replace(ch, "")
    return '{0}{1}{2}'.format(prefix, u[:length], suffix)