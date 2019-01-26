# -*- coding: utf-8 -*-


from datetime import datetime
from glob import glob
from hashlib import sha1
from os import chdir
from os import getcwd
from os import getpid
from os.path import abspath
from os.path import normpath
from os.path import splitext
import ntpath



def get_file_name(p):
  h, t = ntpath.split(p)
  return t or ntpath.basename(h)

def get_only_file_name(p):
  return splitext(p)[0]

def norm_path_gen(ll):
  for l in ll:
    yield normpath(l)


def short_ref(i):
  if not i:
    return None
  try:
    return get_only_file_name(get_file_name(list(i)[0])).split('-')[-1]
  except IndexError:
    return None


def _get_time(milli, delimit):
  return datetime.now().strftime(
      ('%Y%m%d{deli}%H%M%S{deli}%f'
       if milli else '%Y%m%d{deli}%H%M%S').format(deli=delimit))


class Fn:
  def __init__(self, prefix='', postfix='', delimit='-',
               git_sha_size=7, proc_sha_size=8, milli=True):
    self.cwd = getcwd()

    self.prefix = prefix
    self.postfix = postfix
    self.delimit = delimit
    self.git_sha_size = git_sha_size
    self.proc_sha_size = proc_sha_size

    self.milli = milli

    self.repo = None
    self.sha = ''

    self.__init_repo()
    self.__get_git_sha()

    self.proc_sha = self.__get_proc_time_sha()
    self.inc = 0

  def __enter__(self):
    return self

  def __exit__(self, t, value, traceback):
    return False

  def __get_proc_time_sha(self):
    h = sha1()
    h.update('{:s}:{:d}'.format(_get_time(True, self.delimit),
                                getpid()).encode('utf-8'))
    return h.hexdigest()[:self.proc_sha_size]

  def __init_repo(self):
    from git.repo import Repo
    from git import InvalidGitRepositoryError

    try:
      self.repo = Repo(self.cwd, search_parent_directories=True)
    except InvalidGitRepositoryError:
      # git sha will be '' if we are not in a git repo
      pass
    except Exception:
      raise Exception('unexpected error when looking for git repo.')

  def __get_git_sha(self):
    if self.repo is not None:
      self.sha = self.repo.git.rev_parse('HEAD', short=self.git_sha_size)

  def name(self, postfix=None):
    d = self.delimit
    l = [self.prefix, _get_time(self.milli, self.delimit),
         d, self.sha, d, self.proc_sha]

    if postfix is not None:
      l.append(postfix)
    elif self.postfix:
      l.append(self.postfix)

    self.inc += 1
    return ''.join(l)

  def name_gen(self, prefix=None):
    while True:
      yield self.name(prefix)

  def __get_current_files(self, d=None, relative=False, absolute=False):
    if not self.sha:
      raise ValueError('not a git repo')

    if d:
      try:
        chdir(d)
      except FileNotFoundError:
        raise ValueError('no folder, {:s}'.format(d))

    res = sorted(glob('*{:s}*'.format(self.sha)))
    gen = res
    if relative:
      gen = ['{:s}/{:s}'.format(d, f) for f in res]
    elif absolute:
      gen = [abspath(f) for f in res]

    return norm_path_gen(gen)

  def get_proc_sha(self):
    return self.proc_sha

  def get_sha(self):
    if not self.sha:
      raise ValueError('not a git repo')
    return self.sha

  def recent(self, **args):
    current = list(self.__get_current_files(**args))
    if not current:
      return []

    name = get_file_name(current[-1])
    only_name = get_only_file_name(name)
    return filter(lambda x: only_name in x, reversed(current))

  def recent_nopref(self, d):
    current = list(self.__get_current_files(d))
    if not current:
      return []

    name = get_file_name(current[-1])
    only_name = get_only_file_name(name)
    return [only_name]

  def list(self, **args):
    return self.__get_current_files(**args)

