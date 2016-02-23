#### Command-line color scheme selector for iTerm2

```sh
pip install iterm2-color-scheme
```

##### Interactive usage
With no arguments, the command runs in interactive mode: use tab to complete color scheme names (other readline key bindings are also available).

##### Non-interactive usage

<table>
  <tbody>
    <tr>
      <td><code>--scheme &lt;scheme&gt;</code></td>
      <td>Select the specified scheme (case-insensitive substring matching)</td>
    </tr>
    <tr>
      <td><code>--list</code></td>
      <td>List available schemes</td>
    </tr>
    <tr>
      <td><code>--help</code></td>
      <td>Show help</td>
    </tr>
    <tr>
      <td><code>--quiet</code></td>
      <td>Don't show tip</td>
    </tr>
  </tbody>
</table>

##### Credits and contributions

The color schemes (and the script to issue the iterm2 escape sequences) are
from https://github.com/mbadolato/iTerm2-Color-Schemes, which is included as a
submodule. All credit for the schemes goes to the original scheme authors and
to the iTerm2-Color-Schemes project. To add a new scheme, please first create a
pull request against iTerm2-Color-Schemes to add your scheme, and then open a
pull request or issue against this repo to update the submodule.
