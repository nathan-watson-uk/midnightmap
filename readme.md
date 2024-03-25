# MidnightMap
## _Uncover Industrial Scale Web Attack Surfaces_

_A concept tool currently under development that provides intelligence into the attack surface of web applications
within geographic regions and/or TLDS_


## Current Features

- DuckDuckGo Lite Search Integration
- Removal of Common Domains for TLDs to refine results
- Country Based IP Address Checks / TLD Specification
- Translation to Local Language
- DuckDuckGo Advanced Search Capabilities

## Work In Progress

- Website Tech Stack Analysis - Soon
- Numerous TLDs in a Single Command
- Compiled Results
- Graphical Data Analytics

## Known Issues

- Random User Agent Library requires manual pip installation

## Installation

MighdnightMap requires [Python 3 - 3.10+](https://www.python.org/) to run.

Git Clone the repository & navigate to the directory

```bash
git clone https://github.com/nathan-watson-uk/MidnightMap.git

cd MidnightMap
```

Install the requirements

```bash
pip3 install -r requirements.txt
```

Install random-user-agent
```bash
pip3 install random-user-agent
```

Run the script and view the usage page
```bash
python3 midnightmap.py -h
```

## Disclaimer

The MidnightMap tool is provided for educational and research purposes only. By using this tool, you acknowledge and agree that:

- **User Responsibility**: You are solely responsible for your use of MidnightMap and any consequences thereof. The developers of MidnightMap shall not be responsible for any misuse or illegal use of this tool by users.

- **Legal Compliance**: You will comply with all applicable laws, regulations, and ethical standards governing your use of this tool, including but not limited to data protection laws and regulations.

