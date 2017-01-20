# -*- coding: utf-8 -*-

from datetime import datetime
from time import time


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
      utc=None
      ):
    self.cwd = self.__get_cwd()

    self.prefix = str(prefix)
    self.postfix = str(postfix)
    self.delimit = str(delimit)

    self.inc_size = int(inc_size)
    self.git_sha_size = int(git_sha_size)
    self.proc_sha_size = int(proc_sha_size)
    self.utc = utc

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

  def __get_cwd(self):
    from os import getcwd
    return getcwd()

  def __get_proc_time_sha(self):
    from os import getpid
    from hashlib import sha256

    h = sha256()
    p = str(getpid())
    t = self.__get_time()

    slug = '{:s}:{:s}'.format(t, p)
    h.update(slug.encode('utf-8'))
    r = h.hexdigest()[:self.proc_sha_size]
    return r

  def __init_repo(self):
    from git.repo import Repo

    try:
      repo = Repo(self.cwd, search_parent_directories=True)
      self.repo = repo
      self.top_level = repo.git.rev_parse('--show-toplevel')
    except Exception:
      raise RuntimeError(
          'fn: directory is not a git repository, or git is not installed.'
          )

  def __get_git_sha(self):
    self.sha = self.repo.git.rev_parse('HEAD', short=self.git_sha_size)

  def __get_time(self, ):
    d = self.delimit
    tf = '%Y%m%d{:s}%H%M%S{:s}%f'.format(d, d)
    if self.utc:
      return datetime.utcnow().strftime(tf)
    else:
      return datetime.now().strftime(tf)

  def name(
      self,
      postfix=None
      ):
    t = self.__get_time()
    d = self.delimit
    l = [self.prefix, t, d, self.sha, d, self.proc_sha]


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

  def __get_current_files(self, d=None):
    from glob import glob
    from os import chdir

    if d:
      chdir(d)

    p = '*{:s}*'.format(self.sha)
    res = sorted(glob(p))
    return res

  def get_sha(self):

    return self.sha

  def recent(self, d=None):
    current = list(self.__get_current_files(d))

    if len(current) > 0:
      name = current[-1].split('.')[0].strip()
      res = []

      for c in reversed(current):
        if c.split('.')[0].strip() == name:
          res.append(c)
      return res
    else:
      return []

  def list(self, d=None):
    return self.__get_current_files(d)

