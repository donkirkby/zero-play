"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup
from os import path
import zero_play

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='zero_play',
      version=zero_play.__version__,
      description='Play board games using the techniques from AlphaZero',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/donkirkby/zero-play',
      author='Don Kirkby',
      classifiers=[  # https://pypi.org/classifiers/
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Games/Entertainment :: Board Games',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7'],
      keywords='boardgames alphazero machine learning mcts',
      packages=['zero_play'],
      install_requires=['numpy'],
      extras_require={'dev': ['seaborn',
                              'matplotlib',
                              'pytest',
                              'coverage',
                              'mypy']},
      entry_points={
          'console_scripts': ['zero_play=zero_play.command.play:main',
                              'zero_train=zero_play.command.train:main',
                              'zero_strengths=zero_play.command.plot_strengths:main [dev]'],
          # The game entry point lets you add rules for new games.
          # The zero_play.game.Game class is a useful base class.
          'zero_play.game': ['tictactoe=zero_play.tictactoe.game:TicTacToeGame',
                             'connect4=zero_play.connect4.game:Connect4Game']},
      project_urls={
          'Bug Reports': 'https://github.com/donkirkby/zero-play/issues',
          'Source': 'https://github.com/donkirkby/zero-play'})
