from os.path import abspath
from os.path import splitext
from pathlib import Path
from re import compile as rcompile

from .utils import overlay


def remove_extension(p):
  return splitext(p)[0]


def get_path_fx(d, path):
  rel = Path('.' if d is None else d)
  try:
    return {
      'file': lambda p: Path(p).name,
      'rel': lambda p: rel / Path(p).name,
      'abs': abspath,
    }[path]
  except KeyError:
    return 'incorrect path arguments. use [-a|-A] or neither'


def rel_abs_path(d, path, files):
  fx = get_path_fx(d, path)
  for f in files:
    yield overlay(f, _raw=str(fx(f['_raw'])))


def deduplicate_files(files):
  d = set()
  for f in files:
    if f['_raw'] not in d:
      d.update([f['_raw']])
      yield f


def get_file_name_tokenizer(sep, git_size, pid_size):
  tokens = rcompile(
    sep.join([
      r'(?P<date>[0-9]{8})',
      r'(?P<time>([0-9]{6}(_[0-9]{6})?))',
      r'(?P<gitsha>[0-9a-z]{{{:d}}})?'.format(git_size),
      r'(?P<prochash>[0-9a-z]{{{:d}}})'.format(pid_size),
    ]) +
    ''.join([
      r'(-(?P<num>[0-9]+))*',
      r'(.(?P<ext>[a-zA-Z0-9_-]*$))*'
    ]))

  def fx(files):
    for f in files:
      res = tokens.search(f)
      if res is not None:
        yield overlay(res.groupdict(), _raw=f)
  return fx

