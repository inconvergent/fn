# -*- coding: utf-8 -*-

from copy import deepcopy
from datetime import datetime
from hashlib import sha1
from os.path import abspath
from os.path import normpath
from os.path import splitext
from re import DOTALL
from re import compile as rcompile


def overlay(a, b):
  new = deepcopy(a)
  for k, v in b.items():
    new[k] = deepcopy(v)
  return new


def genif(res):
  if res:
    for r in res:
      if r:
        yield r


def getsha(v):
  h = sha1()
  h.update(':'.join([str(i) for i in v]).encode('utf-8'))
  return h.hexdigest()


def remove_extension(p):
  return splitext(p)[0]


def get_path_fx(d, path):
  try:
    return {
        'file': lambda x: x,
        'rel': (('.' if d is None else d) + '/{:s}').format,
        'abs': abspath,
        }[path]
  except KeyError:
    return 'incorrect path arguments. use [-a|-A] or neither'


def rel_abs_path(d, path, files):
  fx = get_path_fx(d, path)
  for f in files:
    yield overlay(f, {'_raw': normpath(fx(f['_raw']))})


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
  return (f['date'], f['time'], _get_num_or_zero(f))


def get_file_name_tokenizer(sep, git_size, pid_size):
  def _groups():
    return sep.join([
        r'^(?P<date>[0-9]{8})',
        r'(?P<time>([0-9]{6}(_[0-9]{6})?))',
        r'(?P<gitsha>[0-9a-z]{{{:d}}})?'.format(git_size),
        r'(?P<prochash>[0-9a-z]{{{:d}}})'.format(pid_size),
        ])
  def _end():
    return ''.join([
        r'(-(?P<num>[0-9]+))*',
        r'(.(?P<ext>[a-zA-Z0-9_-]*$))*'
        ])

  tokens = rcompile(_groups() + _end(), flags=DOTALL)
  def fx(files):
    for f in files:
      res = tokens.search(f)
      if res is not None:
        d = res.groupdict()
        yield overlay(d, {'_raw': f})
  return fx

