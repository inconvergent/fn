# -*- coding: utf-8 -*-

from os import system
from os import devnull
from subprocess import Popen
from subprocess import PIPE


# from git import InvalidGitRepositoryError
# from git.repo import Repo

# def _init_repo(cwd):
#   try:
#     return Repo(cwd, search_parent_directories=True)
#   except InvalidGitRepositoryError:
#     return None
#   except Exception:
#     raise Exception('unexpected error when looking for git repo.')

# def _init_git_sha(repo, git_sha_size):
#   if repo is not None:
#     return repo.git.rev_parse('HEAD', short=git_sha_size)
#   return ''


def _run_cmd_wait(cmd):
  process = Popen(cmd, stdout=PIPE, stderr=open(devnull, 'w'))
  stdout = process.communicate()[0].decode('utf-8')
  rc = process.returncode
  return rc, stdout


def _init_git_sha_cmd(git_sha_size):
  rc, sha = _run_cmd_wait(['git', 'rev-parse',
                           '--short={:d}'.format(git_sha_size), 'HEAD'])
  if rc == 0:
    return sha.strip()
  return ''

