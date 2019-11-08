# pdfworkshop

PDF compress tool, using iLovePDF API

## Prerequisites
The application is compatible with Windows and Linux based systems.
Python version 3.5 or above is assumed to be installed, as well as pip package manager utility and setuptools module.
An updated version of the pylovepdf library is needed, which can be found [here](https://github.com/MarkHaakman/pylovepdf).

## Installation
```bash
pip install pdfworkshop
```
or
```bash
python setup.py install
```

or
```bash
pip install -e ~/local_fork_repo_path/
```

## How to run
```bash
pdfworkshop -h
```

## Configuration
| name       | default     | description                                                      |
|------------|-------------|------------------------------------------------------------------|
| input_dir  | ./          | Directory where PDF files will be collected from.                |
| output_dir | ./output/   | Directory where the compressed PDF files will be stored.         |
| public_key | ""          | Your public API key.                                                     |
| suffix     | _compressed | The suffix given to compressed files (before the extension).     |
| recursive  | False       | Boolean indicating if input_dir must be scanned recursively. |

The public_key value must be defined before using the tool for the first time.
The required public key can be obtained by creating a developer account on [iLovePDF](https://developer.ilovepdf.com/).
Any value can be configured using:
```bash
pdfworkshop config <config_name> <new_config_value>
```

## Commands
- list-config - list tool configuration values
- config \<option\> \<value\> - edit tool configuration values
- run - compress all PDF files stored in input_dir, storing the result in output_dir

## How to use
By default, the PDF files to compress should be on the directory from where the tool will be called.
After using the _run_ command, an _output_ directory will be created, where all compressed
files will be stored.

## Example run

To exercise some of the available commands, one can try to:

- List the current configuration
```bash
pdfworkshop list-config
```
- Define the API public_key value
```bash
pdfworkshop config public_key <new_public_key>
```
- Run PDF compress tool
```bash
pdfworkshop run
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.
