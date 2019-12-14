#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""fn

Usage:
  fn [-t] [-m]
  fn -g
  fn -p
  fn -l [-a|-A] [<dir>]
  fn -r [-a|-A] [<dir>]
  fn -R [<dir>]
  fn -s [<dir>]


Options:
  -t          return timestamp only.
  -m          include milliseconds.
  -g          return current git sha.
  -p          return prochash.

  -l          list all files with current git sha.
  -r          list all files with the most recent prochash.

  -R          return most recent file name with no suffix.
  -s          return most recent prochash only.

  -A          absolute paths.
  -a          relative paths.

  -h --help   show this screen.
  --version   show version.

"""


from sys import stderr
from sys import exit
from traceback import print_exc

from docopt import docopt

from fn.fn import Fn
from fn.utils import genif
from fn.utils import get_time



def handle_args(fn, args):
  if args['-l']:
    return fn.lst(d=args['<dir>'], rel=args['-a'], _abs=args['-A'])
  if args['-r']:
    return fn.recent(d=args['<dir>'], rel=args['-a'], _abs=args['-A'])
  if args['-s']:
    return fn.recent_prochash(args['<dir>'])
  if args['-R']:
    return fn.recent_nosuffix(d=args['<dir>'])
  if args['-p']:
    return [fn.get_pid_sha()]
  if args['-g']:
    return [fn.get_sha()]
  return [fn.name(milli=args['-m'])]


def main():
  args = docopt(__doc__, version='fn 2.0.0')

  if args['-t']:
    print(get_time(milli=args['-m']))
    exit(0)

  try:
    with Fn() as fn:
      for r in genif(handle_args(fn, args)):
        print(r)
  except ValueError as e:
    print('err: ' + str(e), file=stderr)
    exit(1)
  except Exception as e:
    print_exc(file=stderr)
    exit(2)


if __name__ == '__main__':
  main()

