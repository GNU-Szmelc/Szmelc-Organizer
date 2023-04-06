# Szmelc-Organizer
Simple Python3 file sorter in CLI

### FILES
> `sorter.py` - Main sorting script\
> `config.yml` - YAML config file (specify file extensions / source & target paths)\
> [SZMELC COMMANDER SUPPORT COMING SOON]

### MISC
Default configuration will create `Sorted` folder tree inside script's directory\
Save output logs as `log-*.txt` in `logs` folder\
Delete all remaining empty folders\
For now, all incompatible files without `.format`, without name but with `format` or `.format` will remain as is.\
To add your own file formats / extensions, include them into `config.yml`
