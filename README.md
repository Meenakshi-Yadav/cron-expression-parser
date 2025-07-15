# Cron Parser
A Python CLI tool to parse and format cron expressions

## Overview
This tool parses a cron expression (e.g., */5 0 1,6 * 1-5 /usr/bin/find) and displays it in a human-readable table format like:

like this:

   ```
   minute        0 5 10 15 20 25 30 35 40 45 50 55
   hour          0
   day of month  1 6
   month         1 2 3 4 5 6 7 8 9 10 11 12
   day of week   1 2 3 4 5
   command       /usr/bin/find
   ```

It handles standard cron syntax, including:
```
wildcard       *

value lists    ,

ranges         -

step values   */n
```
## Installation
Clone this repository:
   ```bash
   git clone https://github.com/Meenakshi-Yadav/cron-expression-parser.git
   cd cron_parser
```
## Quick Start
Run it (Python 3.6+ required):

```bash
python parser.py "YOUR_CRON_EXPRESSION"
```

Test it:

```bash
python test_parser.py
```
## Features
1. Full cron syntax support: * (wildcards), , (lists), - (ranges), */n (steps)

2. Input validation: Catches errors like */0 or 5-1 with clear messages

3. Clean output: Human-readable aligned tables

4. Zero dependencies: Pure Python (3.6+)
