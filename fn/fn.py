# -*- coding: utf-8 -*-


from datetime import datetime
from glob import glob
from hashlib import sha256
from os import chdir
from os import getcwd
from os import getpid
from os.path import abspath
from os.path import normpath
from os.path import splitext
from time import time
import ntpath



class RepoException(Exception):
  pass

def get_file_name(p):
  h, t = ntpath.split(p)
  return t or ntpath.basename(h)

def get_only_file_name(p):
  return '-'.join(splitext(p)[0].split('-')[:4])

def norm_path_gen(ll):
  for l in ll:
    yield normpath(l)


def short_ref(i):
  print(i)
  if not i:
    return None
  try:
    return list(i)[0].split('-')[3]
  except IndexError:
    return None


class Fn:
  def __init__(
      self,
      prefix='',
      postfix='',
      delimit='-',
      inc_size=5,
      git_sha_size=7,
      proc_sha_size=7,
      append_inc=False,
      milli=True,
      utc=None
      ):
    self.cwd = getcwd()

    self.prefix = str(prefix)
    self.postfix = str(postfix)
    self.delimit = str(delimit)

    self.inc_size = int(inc_size)
    self.git_sha_size = int(git_sha_size)
    self.proc_sha_size = int(proc_sha_size)
    self.utc = utc

    self.milli = milli

    self.repo = None
    self.top_level = None

    self.append_inc = bool(append_inc)

    self.__init_repo()
    self.__get_git_sha()
    self.proc_sha = self.__get_proc_time_sha()

    self.inc = 0

    self.time = time()
    self.name()

  def __enter__(self):
    return self

  def __exit__(self, t, value, traceback):
    return False

  def __get_proc_time_sha(self):
    h = sha256()
    p = str(getpid())
    t = self.__get_time()

    slug = '{:s}:{:s}'.format(t, p)
    h.update(slug.encode('utf-8'))
    r = h.hexdigest()[:self.proc_sha_size]
    return r

  def __init_repo(self):
    from git.repo import Repo
    from git import InvalidGitRepositoryError

    try:
      repo = Repo(self.cwd, search_parent_directories=True)
      self.top_level = repo.git.rev_parse('--show-toplevel')
      self.repo = repo
    except InvalidGitRepositoryError:
      # git sha will be '' if we are not in a git repo
      pass
    except Exception:
      raise Exception('unexpected error when looking for git repo.')

  def __get_git_sha(self):
    if self.repo is None:
      self.sha = None
    else:
      self.sha = self.repo.git.rev_parse('HEAD', short=self.git_sha_size)

  def __get_time(self):
    d = self.delimit

    if self.milli:
      tf = '%Y%m%d{deli}%H%M%S{deli}%f'.format(deli=d)
    else:
      tf = '%Y%m%d{deli}%H%M%S'.format(deli=d)

    if self.utc:
      return datetime.utcnow().strftime(tf)
    return datetime.now().strftime(tf)

  def name(
      self,
      postfix=None,
      ):
    t = self.__get_time()
    d = self.delimit
    l = [self.prefix, t, d,
         self.sha if self.sha is not None else '',
         d, self.proc_sha]

    if self.append_inc:
      l.extend([d, ('{:0'+str(self.inc_size)+'d}').format(self.inc)])

    if isinstance(postfix, str):
      l.append(postfix)
    elif self.postfix:
      l.append(self.postfix)

    fn = ''.join(l)
    self.current = fn
    self.inc += 1
    return fn

  def name_gen(self, prefix=None):
    while True:
      yield self.name(prefix)

  def __get_current_files(self, d=None, relative=False, absolute=False):
    if self.sha is None:
      raise RepoException('not a git repo')

    if d:
      chdir(d)

    p = '*{:s}*'.format(self.sha)
    res = sorted(glob(p))

    gen = res

    if relative:
      gen = ['{:s}/{:s}'.format(d, f) for f in res]
    elif absolute:
      gen = [abspath(f) for f in res]

    return norm_path_gen(gen)

  def get_proc_sha(self):
    return self.proc_sha

  def get_sha(self):
    if self.sha is None:
      raise RepoException('not a git repo')
    return self.sha

  def recent(self, **args):
    current = list(self.__get_current_files(**args))
    if not current:
      return []

    name = get_file_name(current[-1])
    only_name = get_only_file_name(name)
    return filter(lambda x: only_name in x, reversed(current))

  def recent_pref(self, d):
    current = list(self.__get_current_files(d))
    if not current:
      return []

    name = get_file_name(current[-1])
    only_name = get_only_file_name(name)
    return [only_name]

  def list(self, **args):
    return self.__get_current_files(**args)

