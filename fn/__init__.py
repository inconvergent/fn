#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""fn

Usage:
  fn [-m]
  fn -g
  fn -p
  fn -t [-m]
  fn -l [-a|-A] [<dir>]
  fn -r [-a|-A] [<dir>]
  fn -R [<dir>]
  fn -s [<dir>]


Options:
  -t          return timestamp.
  -g          return current git sha.
  -p          return pid:datetime hash.
  -m          include microseconds.

  -l          list all files with current git sha.
  -r          list all files with the most recent pid:datetime hash.

  -R          return most recent file name with no suffix.
  -s          return most recent pid:datetime hash only.

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
from fn.utils import get_time
from fn.utils import short_ref



def handle_args(fn, args):
  if args['-l']:
    return fn.lst(d=args['<dir>'], rel=args['-a'], _abs=args['-A'])
  if args['-r']:
    return fn.recent(d=args['<dir>'], rel=args['-a'], _abs=args['-A'])
  if args['-s']:
    return [short_ref(list(fn.recent(d=args['<dir>'])))]
  if args['-R']:
    return fn.recent_nosuffix(d=args['<dir>'])
  if args['-p']:
    return [fn.get_pid_sha()]
  if args['-g']:
    return [fn.get_sha()]
  return [fn.name(args['-m'])]


def genif(res):
  if res:
    for r in res:
      if r:
        yield r


def main():
  args = docopt(__doc__, version='fn 1.1.3')

  # shortcut
  if args['-t']:
    print(get_time(args['-m']))
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

