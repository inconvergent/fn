#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""fn

Description:
  `fn` is a tool for generating, and parsing, file names based on
  current date, time, process id and gitsha.

  use `fn` to generate a file name.
  use `fn -r [dir]` to get the most recent file (in dir).
  more options listed below.


Usage:
  fn [-m] [-t]
  fn -g
  fn -p
  fn -r [-a|-A] [<dir>]
  fn -l [-a|-A] [<dir>]
  fn -R [<dir>]
  fn -s [<dir>]


Options:
  -m          include milliseconds.
  -g          return current git sha.
  -p          return a prochash.
  -t          return timestamp only.

  -r          return all files with the most recent prochash.
  -R          return most recent file name with no suffix.
  -l          return all files with current git sha.
  -s          return most recent prochash.

  -a          show file name only.
  -A          show absolute paths.

  -h --help   show this screen.
  --version   show version.

"""


from sys import exit as pexit
from sys import stderr
from traceback import print_exc

from docopt import docopt

from fn.fn import Fn
from fn.utils import genif
from fn.utils import get_time
from fn.utils import overlay


def handle_path_args(args):
  # relative path style: dir/file.ext
  path_style = 'rel'
  if args['-a']:
    # file name only: file.ext
    path_style = 'file'
  elif args['-A']:
    # absolute path style: /a/b/file.ext
    path_style = 'abs'
  return overlay(args, {'path_style': path_style})

def handle_args(fn, args):
  args = handle_path_args(args)
  if args['-l']:
    return fn.lst(d=args['<dir>'], path_style=args['path_style'])
  if args['-r']:
    return fn.recent(d=args['<dir>'], path_style=args['path_style'])
  if args['-s']:
    return fn.recent_prochash(d=args['<dir>'])
  if args['-R']:
    return fn.recent_nosuffix(d=args['<dir>'])
  if args['-p']:
    return [fn.get_pid_sha()]
  if args['-g']:
    return [fn.get_sha()]
  return [fn.name(milli=args['-m'])]


def main():
  args = docopt(__doc__, version='fn 2.2.1')

  if args['-t']:
    print(get_time(milli=args['-m']))
    pexit(0)

  try:
    with Fn() as fn:
      for r in genif(handle_args(fn, args)):
        print(r)
  except ValueError as e:
    print('err: ' + str(e), file=stderr)
    pexit(1)
  except Exception as e:
    print_exc(file=stderr)
    pexit(2)


if __name__ == '__main__':
  main()

