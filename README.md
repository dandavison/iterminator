#### Command-line color scheme selector for iTerm2

```sh
pip install iterminator
```

##### Examples

- `iterminator`

  Use <code>right/left</code> or <code>j/k</code> or <code>n/p</code> to move forwards/backwards through color schemes.

- `iterminator -a 2.5`

  Cycle through schemes automatically at 2.5 schemes/second. Use <code>space</code> to pause, <code>right/left</code> or <code>j/k</code> or <code>n/p</code> to move forwards/backwards through color schemes.

- `iterminator -s cobalt2`

  Select a single scheme (case-insensitive substring matching).

- `iterminator -i`

  Select color scheme interactively with tab completion.

- `iterminator -l`

  List color schemes.

- `iterminator --help`

  Show help.


##### Credits and contributions

The color schemes (and the script to issue the iterm2 escape sequences) are
from https://github.com/mbadolato/iTerm2-Color-Schemes, which is included as a
submodule. All credit for the schemes goes to the original scheme authors and
to the iTerm2-Color-Schemes project. To add a new scheme, please first create a
pull request against iTerm2-Color-Schemes to add your scheme, and then open a
pull request or issue against this repo to update the submodule.
