#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""fn

Usage:
  fn
  fn [-l | -L] [<dir>]
  fn [-r | -R] [<dir>]
  fn -h

Examples:

  fn            Get a distinct file name
  fn -l [<dir>] List all files named after current git commit.
  fn -L [<dir>] Same as -l, but with absolute path
  fn -r [<dir>] List most recent files named
                  after current git commit.
  fn -R [<dir>] Same as -r, but with absolute path
  -h            Show this screen.
  --version     Show version.
"""


__ALL__ = ['Fn']

from fn.fn import Fn



def run():

  from docopt import docopt
  args = docopt(__doc__, version='fn 0.1.2')
  main(args)



def main(args):

  from sys import stderr

  try:
    with Fn() as fn:
      if args['-l']:
        res = fn.list(d=args['<dir>'])
      if args['-L']:
        res = fn.list(d=args['<dir>'], absolute=True)
      elif args['-r']:
        res = fn.recent(d=args['<dir>'])
      elif args['-R']:
        res = fn.recent(d=args['<dir>'], absolute=True)
      else:
        res = [fn.name()]

      for r in res:
        print(r)

  except Exception as e:
    print(e, file=stderr)
    # from traceback import print_exc
    # print_exc(file=stderr)
    exit(1)


if __name__ == '__main__':
  run()

