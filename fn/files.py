from os.path import abspath
from os.path import normpath
from os.path import splitext
from re import DOTALL
from re import compile as rcompile

from .utils import overlay


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


def deduplicate_files(files):
  d = set()
  for f in files:
    if f['_raw'] not in d:
      d.update([f['_raw']])
      yield f


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
        yield overlay(res.groupdict(), {'_raw': f})
  return fx

