# -*- coding: utf-8 -*-


from datetime import datetime
from hashlib import sha1
from os.path import normpath
from os.path import splitext
import ntpath


def _getsha(v):
  h = sha1()
  h.update(':'.join([str(i) for i in v]).encode('utf-8'))
  return h.hexdigest()


def get_file_name(p):
  h, t = ntpath.split(p)
  return t or ntpath.basename(h)


def remove_extension(p):
  return splitext(p)[0]


def norm_path_gen(ll):
  for l in ll:
    yield normpath(l)


def short_ref(i):
  if not i:
    return None
  try:
    return remove_extension(get_file_name(list(i)[0])).split('-')[3]
  except IndexError:
    return None


def get_time(milli, delimit='-'):
  return datetime.now().strftime(
      ('%Y%m%d{deli}%H%M%S_%f' if milli
       else '%Y%m%d{deli}%H%M%S').format(deli=delimit))

