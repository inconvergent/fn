from copy import deepcopy
from datetime import datetime
from hashlib import sha1
from itertools import islice


def overlay(a, b):
  new = deepcopy(a)
  for k, v in b.items():
    new[k] = deepcopy(v)
  return new

def to_int(n):
  try:
    return int(n)
  except ValueError:
    raise ValueError('must provide an integer when using -n')

def inv_num(res, inv=False, n=None):
  if inv:
    if not isinstance(res, list):
      res = list(res)
    res.reverse()
  if n is not None:
    return islice(res, to_int(n))
  return res


def getsha(v):
  h = sha1()
  h.update(':'.join([str(i) for i in v]).encode('utf-8'))
  return h.hexdigest()


def get_time(milli=True, sep='-'):
  now = datetime.now()
  if milli:
    return now.strftime('%Y%m%d{deli}%H%M%S_%f'.format(deli=sep))
  return now.strftime('%Y%m%d{deli}%H%M%S'.format(deli=sep))


def _get_num_or_zero(f):
  try:
    return int(f['num'])
  except (TypeError, KeyError):
    return 0

def sortfx(f):
  return f['date'], f['time'], _get_num_or_zero(f)

