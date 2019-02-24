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
  -p          return proc:datetime sha.
  -m          include microseconds.

  -l          list all files with current git sha.
  -r          list all files with the most recent proc:datetime sha.

  -R          return most recent file name with no suffix.
  -s          return most recent file name, proc:datetime sha only.

  -A          absolute paths.
  -a          relative paths.

  -h --help   show this screen.
  --version   show version.

"""


from sys import stderr
from traceback import print_exc

from fn.fn import Fn
from fn.utils import short_ref
from fn.utils import get_time



def run():
  from docopt import docopt
  args = docopt(__doc__, version='fn 1.1.0')
  main(args)


def handle_args(fn, args):
  if args['-l']:
    return fn.lst(d=args['<dir>'], rel=args['-a'], _abs=args['-A'])
  if args['-r']:
    return fn.recent(d=args['<dir>'], rel=args['-a'], _abs=args['-A'])
  if args['-s']:
    return [short_ref(list(fn.recent(d=args['<dir>'])))]
  if args['-R']:
    return fn.recent_nopref(d=args['<dir>'])
  if args['-p']:
    return [fn.get_proc_sha()]
  if args['-g']:
    return [fn.get_sha()]
  return [fn.name(args['-m'])]


def genif(res):
  if res:
    for r in res:
      if r:
        yield r


def main(args):
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
  run()

