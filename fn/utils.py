# -*- coding: utf-8 -*-

from datetime import datetime
from hashlib import sha1
from os.path import abspath
from os.path import normpath
from os.path import splitext
from re import DOTALL
from re import compile as rcompile


def genif(res):
  if res:
    for r in res:
      if r:
        yield r


def _getsha(v):
  h = sha1()
  h.update(':'.join([str(i) for i in v]).encode('utf-8'))
  return h.hexdigest()


def remove_extension(p):
  return splitext(p)[0]


def rel_abs_path(d, rel, _abs, files):
  if rel:
    fx = (('.' if d is None else d) + '/{:s}').format
  elif _abs:
    fx = abspath
  else:
    fx = lambda x: x

  for f in files:
    f['_raw'] = normpath(fx(f['_raw']))
    yield f


def get_time(milli=True, delimit='-'):
  now = datetime.now()
  if milli:
    return now.strftime('%Y%m%d{deli}%H%M%S_%f'.format(deli=delimit))
  return now.strftime('%Y%m%d{deli}%H%M%S'.format(deli=delimit))


def _get_num_or_zero(f):
  try:
    return int(f['num'])
  except (TypeError, KeyError):
    return 0

def sortfx(f):
  return (f['date'], f['time'], _get_num_or_zero(f))


def get_file_name_tokenizer(delimit, git_sha_size, pid_sha_size):
  groups = [
      r'^(?P<date>[0-9]{8})',
      r'(?P<time>([0-9]{6}(_[0-9]{6})?))',
      r'(?P<gitsha>[0-9a-z]{{{:d}}})'.format(git_sha_size),
      r'(?P<prochash>[0-9a-z]{{{:d}}})'.format(pid_sha_size),
      ]

  re_tokens = rcompile(
      delimit.join(groups) +
          r'(-(?P<num>[0-9]+))*' +
          r'(.(?P<ext>[a-zA-Z0-9_-]*$))*',
      flags=DOTALL)
  def fx(files):
    for f in files:
      res = re_tokens.search(f)
      if res is not None:
        d = res.groupdict()
        d['_raw'] = f
        yield d
  return fx

