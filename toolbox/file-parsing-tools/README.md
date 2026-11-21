# File Parsing Tools

Three read-only checks for local files before they reach a parser. Requires Python 3 on Linux and uses only the standard library. No installation is needed. Run these examples from the repository root.

| Script | Checks | Defaults |
| --- | --- | --- |
| `buffer_safety.py` | Regular file and input size | 10 MiB |
| `file_validation.py` | Regular file, filename extension, and input size | 50 MiB and `.txt`, `.pdf`, `.log`, `.xml`, `.json` |
| `safe_image_parser.py` | Regular file, PNG signature, IHDR fields and checksum, input size, and declared pixel count | 20 MiB and 25 million pixels |

```bash
python3 -B toolbox/file-parsing-tools/buffer_safety.py sample.bin --max-bytes 1048576
python3 -B toolbox/file-parsing-tools/file_validation.py sample.json --allow-extension .json
python3 -B toolbox/file-parsing-tools/safe_image_parser.py sample.png --max-pixels 2000000
```

Use `--help` on any script for its options. Repeat `--allow-extension` to specify multiple permitted extensions. Paths must refer to regular files, and symbolic links in the final path component are rejected. Exit status `0` means the checks passed, `1` means the input was rejected or could not be read, and `2` means the CLI arguments were invalid.

The filename policy only checks the suffix. The PNG check stops at the header and does not verify the image data or decode pixels. A passing result establishes only that the file met the checks listed above.

## Tests

```bash
python3 -B toolbox/file-parsing-tools/tests/test_cli.py
```

The suite creates temporary sample files and exercises size boundaries, symlink and FIFO rejection, the extension policy, PNG header and checksum checks, pixel limits, and CLI help.
