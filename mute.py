import os
import re
import json
import pathlib
import argparse
import tempfile
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Input bodyfile generated from fls")
parser.add_argument("-o", "--output", help="Name of the output file. Without extension")
parser.add_argument("-b", "--bodyfile", help="Export the resulted bodyfile", action="store_true")
args = parser.parse_args()


if not args.file or not args.output:
    parser.print_help()
    exit(1)

with open(os.path.join(pathlib.Path(__file__).parent, "warning-dict-timeline.json"), "r") as read_file:
    warning_list = json.load(read_file)

try:
    with open(args.file, "r") as read_file:
        loc_file = read_file.readlines()
except:
    print("[-] File not found")
    exit(1)

final_file = []
deleted_lines = []
# warning_list["selected"].append("sys32")
# warning_list["selected"].append("sys64")
# warning_list["selected"].append("av")

for line in loc_file:
    loc_path = line.split("|")[1]
    flag = False
    for warn_list in warning_list["selected"]:
        for warn in warning_list[warn_list]:
            if re.match(r""+warn, loc_path):
                flag = True
    if not flag:
        final_file.append(line)
    else:
        deleted_lines.append(line)

if args.bodyfile:
    with open(os.path.join(pathlib.Path(__file__).parent, f"{args.output}.body"), "w") as write_file:
        for line in final_file:
            write_file.write(line)

    with open(os.path.join(pathlib.Path(__file__).parent, f"{args.output}_deleted.body"), "w") as write_file:
        for line in deleted_lines:
            write_file.write(line)


with tempfile.NamedTemporaryFile(mode='w+', delete=True) as body_file:
    # Write body data
    for line in final_file:
        body_file.write(line)
    body_file.flush()  # Make sure it's written

    # Run mactime, writing output to the output_file
    result = subprocess.run(
        ["mactime", "-b", body_file.name],
        text=True,
        check=True,
        timeout=None, stdout=subprocess.PIPE,
        errors='replace'
    )

    print("[+] Finished")

    with open(f"{args.output}.time", "w") as f:
        f.write(result.stdout)

with tempfile.NamedTemporaryFile(mode='w+', delete=True) as body_file:
    # Write body data
    for line in deleted_lines:
        body_file.write(line)
    body_file.flush()  # Make sure it's written

    # Run mactime, writing output to the output_file
    result = subprocess.run(
        ["mactime", "-b", body_file.name],
        text=True,
        check=True,
        timeout=None, stdout=subprocess.PIPE
    )

    with open(f"{args.output}_deleted.time", "w") as f:
        f.write(result.stdout)



