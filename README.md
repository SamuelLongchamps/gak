# Gak
*Command-line tool to make local Git repo interaction more efficient*

## Goal
Allows to simplify some tasks usually done for a Git project through the command-line.
The tool uses per-repo as well as user-specific configuration to interact with a local clone.

## Setup
### Installing the tool
(Currently development-only)

* Clone the gak repository
* Run `pip install -e <path to gak repository>`

The command-line tool is usable through the command `gak`.

*Note that Windows' command-prompt is not supported: use git-bash.*

### Configuration files
* The repository can define configurations using .json files named after the supported commands and place them under a `gakconfig.d` folder in the root of the repository.
* For user-specific configurations, a single `.gakconfig.json` is expected in the user's home directory, with each supported command being the key entry. 

#### Example configurations
See gak's repo own `gakconfig.d` directory.

User configuration (`~/.gakconfig.json`):
```
{
"open": {
  "file": "start {}",
  "vscode": "code {}"
  }
}
```
This example is for a Windows user. For macOS, `file` could use `open` and GnuLinux could use `xdg-open`.

## Usage
```
usage: gak [-h] {build,b,list,ls,mkdev,md,open,o,to} ...

positional arguments:
  {build,p,list,ls,mkdev,md,open,o,to}
                        Action to take
    build (b)           Build stuff
    list (ls)           List configurations defined for this project
    mkdev (md)          Rename the current branch with a dev prefix
    open (o)            Open stuff
    to                  Go to places in the repo

optional arguments:
  -h, --help            show this help message and exit
```

Use `gak <action> --help` for usage of individual actions.

## Tips
* The `to` action cannot execute a `cd` in the caller's context. You may use a bash function defined in your `.bashrc` to accomplish the `cd`:
```bash
gakto() {
        DIR=`gak to $1`
        if [ -d "$DIR" ]; then
                cd $DIR
        fi
}
```
