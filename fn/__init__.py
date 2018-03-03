#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""fn

Usage:
  fn [-m]
  fn -s|-p
  fn -l [-a|-A] [<dir>]
  fn -r [-a|-A] [<dir>]
  fn -R [<dir>]
  fn --help
  fn --version


Options:
  -m          Include microseconds.
  -s          Return git sha only.
  -p          Return proc+date sha only.
  -l          List all files named after current git commit.
  -r          List most recent files (of all file types)
                named after current git commit.
  -R          List most recent file name with no suffix.
  -A          Return absolute paths.
  -a          Return relative paths.
  --help      Show this screen.
  --version   Show version.

"""


from sys import stderr
from traceback import print_exc
from fn.fn import Fn
from fn.fn import RepoException


__ALL__ = ['Fn']



def run():
  from docopt import docopt
  args = docopt(__doc__, version='fn 0.2.2')
  main(args)



def main(args):
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
      elif args['-R']:
        res = fn.recent_pref(d=args['<dir>'])
      elif args['-p']:
        res = [fn.get_proc_sha()]
      elif args['-s']:
        res = [fn.get_sha()]
      else:
        res = [fn.name()]

      for r in res:
        print(r)

  except RepoException as e:
    print('err: ' + str(e), file=stderr)
    exit(1)
  except Exception as e:
    print_exc(file=stderr)
    exit(1)


if __name__ == '__main__':
  run()

