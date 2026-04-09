# Conquest Profile Generator
>Documentation : https://github.com/jakobfriedl/conquest/blob/main/docs/3-PROFILE.md

This project is designed to be used with [Conquest C2](https://github.com/jakobfriedl/conquest).


## Install


```bash
python3 -m venv venv
source venv/bin/activat
pio install -r requirements.txt
```

## Usage

`python3 cli.py --generate jquery`

If you need to convert a Cobalt Strike profile to the Conquest (TOML) format, you can use the following command (recommended):

`python3 cli.py --cobalt-converter cobalt-profiles-test/amazon.profile > /tmp/amazon.toml`

![](/img/convert.png)

![](/img/working.png)

## GUI

`python3 app.py`

![](/img/gui.png)


### Credits

Thanks, @Jakob, for all the work you've done
