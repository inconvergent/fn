from os import devnull
from subprocess import PIPE
from subprocess import Popen


def _run_cmd_wait(cmd):
  process = Popen(cmd, stdout=PIPE, stderr=open(devnull, 'w'))
  stdout = process.communicate()[0].decode('utf-8')
  rc = process.returncode
  return rc, stdout


def _init_git_sha_cmd(git_sha_size):
  cmd = ['git', 'rev-parse', '--short={:d}'.format(git_sha_size), 'HEAD']
  rc, sha = _run_cmd_wait(cmd)
  if rc == 0:
    return sha.strip()
  return ''

