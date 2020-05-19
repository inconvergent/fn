#!/usr/bin/env python3

from time import sleep
from fn import Fn


def main():
  fn = Fn()
  for _ in range(20):
    print(fn.name())
    sleep(0.1)

  print()

  fn = Fn()
  print(fn.name())

  print()

  fn = Fn(prefix='/some/path/', postfix='.txt', git_sha_size=10)
  print(fn.name())
  # note: you can't override the prefix
  print(fn.name(postfix=''))
  print(fn.name(postfix='.png'))

  print()


if __name__ == '__main__':
  main()

