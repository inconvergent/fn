#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from time import sleep


def main():
    from fn import Fn

    fn = Fn()
    for _ in range(20):
        print(fn.name())
        sleep(0.1)

    print()

    fn = Fn(append_inc=True)
    print(fn.name())
    print(fn.current)  # overwritten when you call fn.name()
    print(fn.name())
    print(fn.current)

    print()

    fn = Fn(inc_size=3, append_inc=True)
    for i in range(20):
        print(fn.name())
        sleep(0.1)

    print()

    # you can't override the prefix

    fn = Fn(delimit='.', prefix='/some/path/', postfix='.txt', git_sha_size=10)
    print(fn.name())
    print(fn.name(postfix=''))
    print(fn.name(postfix='.png'))

    print()


if __name__ == '__main__':
    main()
