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

## Windows MingW setup
If you use MingW (e.g., through git-bash), make sure to add `winpty` in front of the shebang of the script installed in your ${PythonInstall}/Scripts/gak. Here is a sample of the resulting script:

```
#!winpty c:\users\username\appdata\local\programs\python\python36-32\python.exe
# EASY-INSTALL-DEV-SCRIPT: 'gak==0.1.0','gak'
__requires__ = 'gak==0.1.0'
__import__('pkg_resources').require('gak==0.1.0')
__file__ = 'D:\\git\\gak\\scripts\\gak'
exec(compile(open(__file__).read(), __file__, 'exec'))
```

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
usage: gak [-h]
           {build,b,commit,list,ls,log,mkdev,md,open,o,start,switch,s,sw,to}
           ...

positional arguments:
  {build,b,commit,list,ls,log,mkdev,md,open,o,start,switch,s,sw,to}
                        Action to take
    build (b)           Build stuff
    commit              Commit the staged area with a prepared message based
                        on the branch name and corresponding JIRA issue
    list (ls)           List configurations defined for this project
    log                 Log time to Jira for a task
    mkdev (md)          Rename the current branch with a dev prefix
    open (o)            Open stuff
    start               Start a task by creating a branch with an appropriate
                        name
    switch (s, sw)      Interactive branch switching using wildcard
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
