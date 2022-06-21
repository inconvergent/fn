"""fn

Description:
  `fn` is a tool for generating, and parsing, file names based on
  current date, time, process id and gitsha.

  use `fn` to generate a file name.
  use `fn -r [dir]` to get the most recent file (in dir).
  more options listed below.


Usage:
  fn [-m] [-d]
  fn [-r | -l | -L] [-a|-A] [-f] [-n TAIL | -N HEAD] [-i] [DIR]
  fn -g
  fn -p
  fn -s [<dir>]


Options:
  -m          include milliseconds.
  -g          return current git sha.
  -p          return a prochash.
  -d          return timestamp only.

  -r          return all files with the most recent prochash.
                sorted by time, asc.
  -l          return all files with current git sha. sorted by time, asc.
  -L          return all files with most recent git sha. sorted by time, asc.

  -N HEAD     HEAD first rows.
  -n TAIL     TAIL last rows.
  -i          reverse output.

  -s          return most recent prochash.

  -a          show file name only.
  -A          show absolute paths.
  -f          remove filename extension. resulting duplicates will be removed.

  -h --help   show this screen.
  --version   show version.

"""


from sys import exit as pexit
from sys import stderr
from traceback import print_exc

from docopt import docopt

from fn.fn import Fn
from fn.utils import get_time
from fn.utils import head_tail
from fn.utils import overlay


def handle_path_args(args):
  path_style = 'rel' # relative path style: dir/file.ext
  if args['-a']: # file name only: file.ext
    path_style = 'file'
  elif args['-A']: # absolute path style: /a/b/file.ext
    path_style = 'abs'
  return overlay(args, path_style=path_style)

def handle_args(fn, args):
  args = handle_path_args(args)
  if args['-l']:
    return fn.lst(d=args['DIR'],
                  path_style=args['path_style'],
                  ext=not args['-f'])
  if args['-L']:
    return fn.lst_recent(d=args['DIR'],
                         path_style=args['path_style'],
                         ext=not args['-f'])
  if args['-r']:
    return fn.recent(d=args['DIR'],
                     path_style=args['path_style'],
                     ext=not args['-f'])
  if args['-s']:
    return fn.recent_prochash(d=args['DIR'])
  if args['-p']:
    return [fn.get_pid_sha()]
  if args['-g']:
    return [fn.get_sha()]
  return [fn.name(milli=args['-m'])]


def main():
  args = docopt(__doc__, version='fn 2.4.0')
  # print(args)
  if args['-d']:
    print(get_time(milli=args['-m']))
    pexit(0)

  try:
    fn = Fn()
    res = filter(bool, handle_args(fn, args))
    for r in head_tail(res, head=args['-N'], tail=args['-n'],
                       reverse=args['-i']):
      print(r)
  except ValueError as e:
    print('err: ' + str(e), file=stderr)
    pexit(1)
  except Exception as e:
    print_exc(file=stderr)
    pexit(2)


if __name__ == '__main__':
  main()

