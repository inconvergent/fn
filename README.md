# FN

## What is it?

This is a tiny library to generate file names.

It will give you unique file names based on current git commit, as well as the
time and date. You can also set your own prefix and/or postfix.

When `fn` is called from the terminal, the file names look like this:

    20160428-001056-597392-2d95c86-b775190
    20160428-001056-153234-2d95c86-b775190

Which currently follows this format:

    yyyymmdd-hhmmss-10^(-6)seconds-gitsha-proctimesha

Where `gitsha` is the prefix of the git commit sha. And `proctimesha` is a hash
of the time when `Fn()` is called and the process id of the calling python
script.

If you are not in a git repo, it looks like this:

    20160428-001056-153234--b775190

If you use the package within python you can also:

  - Pass your own prefix and postfix.
  - Override the postfix.
  - Append incremental numbers.
  - Change the delimiter.
  - Override the length of the git sha.

Se `./example.py` for some usage.

Use `fn -h` in the terminal to see other options.

## Why?

I have a lot of projects where I make large amounts of files (images, 3D
models, 2D vector files), and I've always wanted a more efficient way of
maintaining unique file names.

I got inspired to write this when I saw this tweet about how Vera Molar names
her works this Periscope video
https://twitter.com/inconvergent/status/700341427344113665

## Install

Install using either

  `./setup.py install`

Or

  `./setup.py develop`

The latter is most convenient if you will be editing the code.

## Does it guarantee unique file names in any way?

No. It only uses the current time to make a relatively distinct string—don't
use this for anything remotely important.

## On Use and Contributions

This code is a tool that I have written for my own use. I release it publicly
in case people find it useful. It is not however intended as a
collaboration/Open Source project. As such I am unlikely to accept PRs, reply
to issues, or take requests.

