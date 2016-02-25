#### Command-line color scheme selector for iTerm2

```sh
pip install iterm2-color-scheme
```

With no arguments, use `j/k` or `n/p` to move through color schemes.

##### Examples

<table>
  <tr>
    <td><code>iterm2-color-scheme</code></td>
    <td>Use <code>j/k</code> or <code>n/p</code> to move through color schemes.</td>
  </tr>
  <tr>
    <td style="width:100%"><code>iterm2-color-scheme -a 2.5</code></td>
    <td>Cycle through schemes automatically at 2.5 schemes/second. Use <code>space</code> to pause, <code>j/k</code> or <code>n/p</code> to go forwards/backwards.</td>
  </tr>
  <tr>
    <td><code>iterm2-color-scheme -i</code></td>
    <td>Select color scheme interactively with tab completion.</td>
  </tr>
  <tr>
    <td><code>iterm2-color-scheme -s cobalt2</code></td>
    <td>Select a scheme (case-insensitive substring matching).</td>
  </tr>
  <tr>
    <td><code>--help</code></td>
    <td>Show help.</td>
  </tr>
</table>


##### Credits and contributions

The color schemes (and the script to issue the iterm2 escape sequences) are
from https://github.com/mbadolato/iTerm2-Color-Schemes, which is included as a
submodule. All credit for the schemes goes to the original scheme authors and
to the iTerm2-Color-Schemes project. To add a new scheme, please first create a
pull request against iTerm2-Color-Schemes to add your scheme, and then open a
pull request or issue against this repo to update the submodule.
