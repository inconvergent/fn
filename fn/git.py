# -*- coding: utf-8 -*-


from git import InvalidGitRepositoryError
from git.repo import Repo



def _init_repo(cwd):
  try:
    return Repo(cwd, search_parent_directories=True)
  except InvalidGitRepositoryError:
    return None
  except Exception:
    raise Exception('unexpected error when looking for git repo.')


def _init_git_sha(repo, git_sha_size):
  if repo is not None:
    return repo.git.rev_parse('HEAD', short=git_sha_size)
  return ''

