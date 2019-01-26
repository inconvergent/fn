#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from time import sleep



def main():

  from fn import Fn

  fn = Fn()
  for _ in range(20):
    print(fn.name())
    sleep(0.01)

  print()

  fn = Fn()
  print(fn.name())

  print()

  # you can't override the prefix

  fn = Fn(delimit='.', prefix='/some/path/', postfix='.txt', git_sha_size=10)
  print(fn.name())
  print(fn.name(postfix=''))
  print(fn.name(postfix='.png'))


  fn = Fn(milli=False)
  print(fn.name())


  print()


if __name__ == '__main__':
  main()

