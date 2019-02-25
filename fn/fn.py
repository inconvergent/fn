# -*- coding: utf-8 -*-


from glob import glob
from os import chdir
from os import getcwd
from os import getpid

# from .git import _init_git_sha
# from .git import _init_repo
from .git import _init_git_sha_cmd

from .utils import _getsha
from .utils import get_file_name
from .utils import get_time
from .utils import norm_path_gen
from .utils import rel_abs_path
from .utils import remove_extension

DELIMIT = '-'


class Fn:
  def __init__(self, prefix='', postfix='', git_sha_size=7, proc_sha_size=8):
    self.prefix = prefix
    self.postfix = postfix
    self.git_sha_size = git_sha_size
    self.proc_sha_size = proc_sha_size

    # self.gitsha = _init_git_sha(_init_repo(getcwd()), self.git_sha_size)
    self.gitsha = _init_git_sha_cmd(self.git_sha_size)
    self.proc_sha = self.__get_proc_time_sha()

  def __enter__(self):
    return self

  def __exit__(self, t, value, traceback):
    return False

  def __get_proc_time_sha(self):
    return _getsha([get_time(True, DELIMIT),
                    getpid()])[:self.proc_sha_size]

  def name(self, milli=False, postfix=None):
    l = [self.prefix, get_time(milli, DELIMIT),
         DELIMIT, self.gitsha, DELIMIT, self.proc_sha]

    if postfix is not None:
      l.append(postfix)
    elif self.postfix:
      l.append(self.postfix)
    return ''.join(l)

  def __get_current_files(self, d=None, rel=False, _abs=False):
    if not self.gitsha:
      raise ValueError('not in a git repo')

    if d:
      try:
        chdir(d)
      except FileNotFoundError:
        raise ValueError('no folder, {:s}'.format(d))

    return norm_path_gen(
        rel_abs_path(d, rel, _abs, sorted(glob('*{:s}*'.format(self.gitsha)))))

  def get_proc_sha(self):
    return self.proc_sha

  def get_sha(self):
    if not self.gitsha:
      raise ValueError('not in a git repo')
    return self.gitsha

  def recent(self, **args):
    current = list(self.__get_current_files(**args))
    if not current:
      return []

    procsha = remove_extension(get_file_name(current[-1]))\
        .split(DELIMIT)[-1]
    return filter(lambda x: procsha in x, current)

  def recent_nopref(self, d):
    current = list(self.__get_current_files(d))
    if current:
      yield remove_extension(get_file_name(current[-1]))

  def lst(self, **args):
    return self.__get_current_files(**args)

