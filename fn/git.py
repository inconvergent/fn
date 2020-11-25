from os import devnull
from subprocess import PIPE
from subprocess import Popen


def _run_cmd_wait(cmd):
  process = Popen(cmd, stdout=PIPE, stderr=open(devnull, 'w'))
  stdout = process.communicate()[0].decode('utf-8')
  rc = process.returncode
  return rc, stdout


def _init_git_sha_cmd(git_sha_size):
  rc, sha = _run_cmd_wait(
      ['git', 'rev-parse', '--short={:d}'.format(git_sha_size), 'HEAD'])
  if rc == 0:
    return sha.strip()
  return ''

