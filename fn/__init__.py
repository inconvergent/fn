#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""fn

Usage:
  fn [-m]
  fn -l [-a|-A] [<dir>]
  fn -r [-a|-A] [<dir>]
  fn -h | --help
  fn --version


Options:
  -l          List all files named after current git commit.
  -r          List most recent files (of all file types)
                named after current git commit.
  -A          Use absolute path.
  -a          Use relative path.
  -m          Include microseconds.
  -h --help   Show this screen.
  --version   Show version.

"""


__ALL__ = ['Fn']

from fn.fn import Fn



def run():
  from docopt import docopt
  args = docopt(__doc__, version='fn 0.2.2')
  main(args)



def main(args):

  from sys import stderr

  try:
    with Fn(milli=args['-m']) as fn:
      if args['-l']:
        res = fn.list(d=args['<dir>'],
                      relative=args['-a'],
                      absolute=args['-A'])
      elif args['-r']:
        res = fn.recent(d=args['<dir>'],
                        relative=args['-a'],
                        absolute=args['-A'])
      else:
        res = [fn.name()]

      for r in res:
        print(r)

  except Exception as e:
    print('err: ' + str(e), file=stderr)
    # from traceback import print_exc
    # print_exc(file=stderr)
    exit(1)


if __name__ == '__main__':
  run()

