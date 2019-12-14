# FN—File Names


## What is it?

This is a tiny library to generate file names.

It will give you unique file names based on current git commit, as well as the
time and date.

When `fn` is called from the terminal, the file names look like this:

    20190126-142138-244db3e-5f3a90f9
    20190126-142155-244db3e-42464759

Which currently follows this format:

    yyyymmdd-hhmmss-gitsha-prochash

Where `gitsha` is the prefix of the git commit sha. And `prochash` is a hash of
the time when `Fn()` is called and the corresponding process id.

If you are not in a git repo, it looks like this:

    20190126-142213--cc607dd0

Use `fn -h` in the terminal to see other options.


## Why?

I have a lot of projects where I make large amounts of files (images, 3D
models, 2D vector files), and I've always wanted a more efficient way of
maintaining unique file names.

I got the idea for this when I saw how Vera Molar names her works in this
Periscope video https://twitter.com/inconvergent/status/700341427344113665


## Dependecies

The code runs on Linux (only, probably) and requires `git` to be installed. It
also uses `docopt`, installed via `setup.py`.


## Install

The easiest is to install with:

    ./setup.py [install | develop] [--user]

Unfortunately the command line support relies on `entry_points`, which is
rather slow. To make it run faster you can (for instance) add a symlink in your
local `bin` folder to `./run.py` in this repo.


## Does it guarantee unique file names in any way?

No. It only uses the current time to make a relatively distinct string—don't
use this for anything remotely important.


## On Use and Contributions

This code is a tool that I have written for my own use. I release it publicly
in case people find it useful. It is not however intended as a
collaboration/Open Source project. As such I am unlikely to accept PRs, reply
to issues, or take requests.

