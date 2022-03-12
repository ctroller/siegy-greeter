# SIEGY GREETER

Stupid Discord bot that sends audio files when a certain member connects.

## Installation
Requires python3 and pip3.

Requires Talk,Connect and Voice Activity bot permissions from Discord.

Rename `.env.template` to `.env` and fill in your details.

Add mp3 files (16Bit, 48Khz, Opus compatible) into `resources`.

```bash
pip3 install -r requirements.txt

python3 index.py <path_to_main_folder>
# e.g.
python3 index.py /opt/siegy-greeter
```
