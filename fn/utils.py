from copy import deepcopy
from datetime import datetime
from hashlib import sha1
from itertools import islice


def overlay(a, **b):
  new = deepcopy(a)
  for k, v in b.items():
    new[k] = deepcopy(v)
  return new

def _to_int(n):
  try:
    return int(n)
  except ValueError as e:
    raise ValueError('must provide an integer when using -n') from e

def head_tail(a, head=None, tail=None, reverse=False):
  assert not (head and tail), 'must proved head, tail or neither'
  res = a
  if head:
    res = islice(res, 0, _to_int(head))
  elif tail:
    res = reversed(list(islice(reversed(list(res)), 0, _to_int(tail))))
  if reverse:
    return reversed(res)
  return res

def getsha(v):
  h = sha1()
  h.update(':'.join([str(i) for i in v]).encode('utf-8'))
  return h.hexdigest()

def get_time(milli=True, sep='-', utc=True):
  now = datetime.utcnow() if utc else datetime.now()
  return now.strftime(
    '%Y%m%d{deli}%H%M%S{milli}'.format(deli=sep, milli='_%f' if milli else ''))

def _int_or_zero(f):
  try:
    return int(f['num'])
  except (TypeError, KeyError):
    return 0

def sortfx(f):
  return f['date'], f['time'], _int_or_zero(f)

