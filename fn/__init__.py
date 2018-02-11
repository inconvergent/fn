#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""fn

Usage:
  fn
  fn -l [<dir>]
  fn -r [<dir>]
  fn -h

Examples:

  fn            Get a distinct file name
  fn -l [<dir>] List all files named after current git commit.
  fn -r [<dir>] List most recent files (if there are more file types) named
                  after current git commit.
  -h            Show this screen.
  --version     Show version.
"""

__ALL__ = ['Fn']

from fn.fn import Fn


def run():
    from docopt import docopt
    args = docopt(__doc__, version='fn 0.1.1')
    main(args)


def main(args):
    from sys import stderr

    try:
        with Fn() as fn:
            if args['-l']:
                res = fn.list(d=args['<dir>'])
            elif args['-r']:
                res = fn.recent(d=args['<dir>'])
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
