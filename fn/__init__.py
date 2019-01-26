#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""fn

Usage:
  fn [-m]
  fn -g|-p
  fn -l [-a|-A] [<dir>]
  fn -r [-a|-A] [<dir>]
  fn -R [<dir>]
  fn -s [<dir>]
  fn --help
  fn --version


Options:
  -m          Include microseconds.
  -g          Return current git sha.
  -p          Return proc+datetime.

  -l          List all files named after current git commit.

  -r          List all files with the most recent procsha.
  -R          Return most recent file name with no suffix.
  -s          Return most recent file name, Proc+datetime sha only.

  -A          Return absolute paths.
  -a          Return relative paths.

  --help      Show this screen.
  --version   Show version.

"""


from sys import stderr
from traceback import print_exc
from fn.fn import Fn
from fn.fn import short_ref


__ALL__ = ['Fn']



def run():
  from docopt import docopt
  args = docopt(__doc__, version='fn 1.0.0')
  main(args)



def main(args):
  try:
    with Fn(milli=args['-m']) as fn:
      a = args['-a']
      A = args['-A']
      if args['-l']:
        res = fn.list(d=args['<dir>'], relative=a, absolute=A)
      elif args['-r']:
        res = fn.recent(d=args['<dir>'], relative=a, absolute=A)
      elif args['-s']:
        res = [short_ref(list(fn.recent(d=args['<dir>'])))]
      elif args['-R']:
        res = fn.recent_nopref(d=args['<dir>'])
      elif args['-p']:
        res = [fn.get_proc_sha()]
      elif args['-g']:
        res = [fn.get_sha()]
      else:
        res = [fn.name()]

      for r in res:
        if r:
          print(r)

  except ValueError as e:
    print('err: ' + str(e), file=stderr)
    exit(1)
  except Exception as e:
    print_exc(file=stderr)
    exit(1)


if __name__ == '__main__':
  run()

