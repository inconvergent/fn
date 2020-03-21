# -*- coding: utf-8 -*-

from glob import glob
from os import chdir
from os import getpid

from .git import _init_git_sha_cmd
from .utils import get_file_name_tokenizer
from .utils import get_time
from .utils import getsha
from .utils import rel_abs_path
from .utils import remove_extension
from .utils import sortfx

SEP = '-'


class Fn:
  def __init__(self, prefix='', postfix='', git_sha_size=7, pid_sha_size=8):
    self.git_sha_size = git_sha_size
    self.pid_sha_size = pid_sha_size
    self.postfix = postfix
    self.prefix = prefix
    self.tokenizer = get_file_name_tokenizer(SEP, git_sha_size, pid_sha_size)
    self.gitsha = _init_git_sha_cmd(self.git_sha_size)
    self.pid_sha = self.__get_pid_time_sha()

  def __enter__(self):
    return self

  def __exit__(self, t, value, traceback):
    return False

  def __is_git(self):
    if not self.gitsha:
      raise ValueError('not in a git repo')
    return self.gitsha

  def __get_pid_time_sha(self):
    return getsha([get_time(), getpid()])[:self.pid_sha_size]

  def name(self, milli=True, postfix=None):
    l = [self.prefix, get_time(milli=milli),
         SEP, self.gitsha, SEP, self.pid_sha]

    if postfix is not None:
      l.append(postfix)
    elif self.postfix:
      l.append(self.postfix)
    return ''.join(l)

  def __get_current_files(self, d=None, path_style='rel'):
    if d:
      try:
        chdir(d)
      except FileNotFoundError:
        raise ValueError('no folder: {:s}'.format(d))

    return rel_abs_path(
        d, path_style, sorted(self.tokenizer(glob('*')), key=sortfx))

  def get_pid_sha(self):
    return self.pid_sha

  def get_sha(self):
    return self.__is_git()

  def recent(self, **args):
    current = list(self.__get_current_files(**args))
    if not current:
      return []

    prochash = current[-1]['prochash']
    return map(
        lambda f: f['_raw'],
        filter(lambda f: f['prochash'] == prochash, current))

  def recent_nosuffix(self, d):
    current = list(self.__get_current_files(d, path_style='file'))
    if current:
      yield remove_extension(current[-1]['_raw'])

  def recent_prochash(self, d):
    current = list(self.__get_current_files(d))
    if current:
      yield current[-1]['prochash']

  def lst(self, **args):
    self.__is_git()
    files = list(self.__get_current_files(**args))
    if not files:
      return []
    prochash = files[-1]['gitsha']
    return map(
        lambda x: x['_raw'],
        filter(lambda x: x['gitsha'] == prochash, files))

