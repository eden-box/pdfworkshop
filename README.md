# pdfworkshop

PDF compress tool, using iLovePDF API

## Prerequisites
The application is compatible with Windows and Linux based systems.
Python version 3.4 or above is assumed to be installed, as well as pip package manager utility and setuptools module.

## Installation
```bash
pip install pdfworkshop
``` 
or
```bash
python setup.py install
``` 

## How to run
```bash
pdfworkshop -h
```

## Configuration
The public_key value must be defined before using the tool for the first time.
The required public key can be obtained by creating a developer account in [iLovePDF](https://developer.ilovepdf.com/).
The value can be configured using:
```bash
pdfworkshop config public_key new_public_key_value
``` 
The input/ouput directories can also be configured.
Their default values are set to a directory called 'input' and 'output'
according to the current path from where the tool was called.

## Commands
- list-config - list tool configuration values
- config \<option\> \<value\> - edit tool configuration values
- run - compress all PDF files stored in input_dir, storing the result in output_dir

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
