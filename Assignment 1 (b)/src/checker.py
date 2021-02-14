#!/usr/bin/env python3

"""
Check whether query.sql file is of right format
Breaks into part-\d+.sql
Create a cleanup.sql

Checks Performed:

* Check whether all sections exist: Preamble, N sections, Cleanup
"""


import sys
import os
import re

TOTAL_QUESTIONS = 10

def err(*msg):
    print(*msg)
    exit(1)

def main(file):

    with open(file) as f:
        fcontents = f.read().strip()

    flines = list(map(lambda l: l.strip(), fcontents.split("\n")))

    if flines[0] != "--PREAMBLE--":
        err("Missing PREAMBLE")
    
    # int -> string
    parts = {}
    
    part = "preamble"
    data = flines[0] + "\n"

    # Build parts dict
    for l in flines[1:]:

        if not l:
            continue

        # Since we've already dealt with Preamble
        # A new section is either a question or cleanup
        m = re.match(r"--\s*(\d+|CLEANUP)\s*--", l)
        if m:
            # Save old part
            parts[part] = data
        
            # New part begins
            part = m.group(1).lower()
            data = l + "\n"
        else:
            data += l + "\n"

    # The last part is cleanup
    parts[part] = data

    # Dump parts dict into individual files
    valid_parts = list(map(str, range(1, TOTAL_QUESTIONS + 1)))
    valid_parts += ["preamble", "cleanup"]

    for part in valid_parts:

        if part not in parts:
            err(
                "Section not present: %s\n"
                "Make sure you create sections for each question, even if you leave them empty." % part.upper()
            )

        if part in ["preamble", "cleanup"]:
            fn = part + ".sql"
        else:
            fn = "part-%s.sql" % part

        # Write to separate file
        with open(fn, "w") as f:
            f.write(parts[part])

        # Remove this part from dict
        parts.pop(part)

    # Nothing should remain at this point
    if parts:
        err(
            "Extra sections present: %s \n" 
            "Remove them." % ",".join(parts.keys())
        )


if __name__ == "__main__":
    main(sys.argv[1])
