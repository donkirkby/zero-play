# Zero Play [![Build Badge]][build] [![Coverage Badge]][codecov] [![PyPI Badge]][pypi]
### Teach a computer to play any game

[Build Badge]: https://github.com/donkirkby/zero-play/actions/workflows/py-build.yml/badge.svg?branch=master
[build]: https://github.com/donkirkby/zero-play/actions
[Coverage Badge]: https://codecov.io/github/donkirkby/zero-play/coverage.svg?branch=master
[codecov]: https://codecov.io/github/donkirkby/zero-play?branch=master
[PyPI Badge]: https://badge.fury.io/py/zero-play.svg
[pypi]: https://badge.fury.io/py/zero-play
[journal]: docs/journal
[screenshot]: https://donkirkby.github.io/zero-play/images/screenshot.png

The zero play library is based on the ideas in the [AlphaGo Zero paper] and the
example Python code in the [alpha-zero-general project]. The goal of this
project is to make a reusable Python library that other projects can build on
to make powerful computer opponents for many different board games. An example
project that uses this library is [Shibumi Games].

It includes a graphical display that you can use to play against the computer
opponent or another human.

![screenshot]

[AlphaGo Zero paper]: https://deepmind.com/blog/alphago-zero-learning-scratch/
[alpha-zero-general project]: https://github.com/suragnair/alpha-zero-general
[Shibumi Games]: https://donkirkby.github.io/shibumi-games/

## Installing Zero Play
Even though Zero Play has a graphical display, it is a regular Python package,
so you can install it with `pip install zero-play`. If you haven't installed
Python packages before, read Brett Cannon's [quick-and-dirty guide].

Then run it with the `zero_play` command.

The default installation generates some errors about `bdist_wheel` that don't
seem to actually cause any problems. You can either ignore them, or install
`wheel` before installing Zero Play.

    pip install wheel
    pip install zero-play
    zero_play

Known bug on Ubuntu 20.04:

> qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though
> it was found.

This is a [PySide2 bug] that is missing some dependencies. You can work around
it by installing those dependencies like this:

    sudo apt install libxcb-xinerama0

[quick-and-dirty guide]: https://snarky.ca/a-quick-and-dirty-guide-on-how-to-install-packages-for-python/
[PySide2 bug]: https://bugreports.qt.io/browse/QTBUG-84749

## More Information
If you'd like to help out with the project, or add your own games, see the
`CONTRIBUTING.md` file in the source code. For all the details, look through the
design [journal] for the project.

## Related Projects
Here are some similar projects for inspiration or collaboration:

* I already mentioned the [alpha-zero-general project]. It was a big inspiration, but I'm trying to build something
    that's easier to add new games to, or use as a library within another project.
* [Galvanise] looks interesting. It's a mix of Python and C++, using Tensorflow. As of 2020, it looks like a single
    developer, without much documentation. The games are defined with GDL, not Python code.

[Galvanise]: https://github.com/richemslie/galvanise_zero
