#!/usr/bin/env python3

"""
Francesco Pallotta 2022
Why not use some random website to assemble shellcode?
This is exactly what this script does.
"""


from argparse import ArgumentParser
from lxml import html
from requests import post

from IPython import embed

URL = "https://defuse.ca/online-x86-assembler.htm"


def get_instructions(filepath):
    with open(filepath, "r") as filedata:
        instructions = filedata.read()
    return instructions


def run_query(instructions, arch, submit):
    payload = {"instructions": instructions, "arch": arch, "submit": submit}
    r = post(URL, data=payload)
    return r


def get_shellcode(response):
    sc_xpath = "/html/body/div[1]/div[3]/div[2]/div[2]/p[4]/text()"
    error_log_xpath = '//*[@id="content"]/div[2]/div[1]/text()'
    # now we want to parse the response and get the shellcode
    tree = html.fromstring(response.content)
    sc = tree.xpath(sc_xpath)
    if sc == []:
        for error in tree.xpath(error_log_xpath):
            print(error)
        exit(1)
    return sc[0]


def main():
    parser = ArgumentParser(
        description="Assemble or disassemble Intel formatted x86/x64 code using defuse.ca's online assembler"
    )
    submit_group = parser.add_mutually_exclusive_group(required=True)
    submit_group.add_argument(
        "-i", "--input_file", help="input file to be assembled/disassembled"
    )
    submit_group.add_argument(
        "-s", "--input_string", help="input string to be assembled/disassembled"
    )
    parser.add_argument(
        "-c",
        "--cpu-arch",
        help="architecture you're working with with (x86/x64)",
        required=True,
    )
    submit_group = parser.add_mutually_exclusive_group(required=True)
    submit_group.add_argument(
        "-a",
        "--assemble",
        help="submit the code to be assembled",
        action="store_const",
        const="Assemble",
    )
    submit_group.add_argument(
        "-d",
        "--disassemble",
        help="submit the code to be disassembled",
        action="store_const",
        const="Disassemble",
    )

    args = parser.parse_args()

    if args.input_file:
        instructions = get_instructions(args.input_file)
    else:
        instructions = args.input_string

    arch = args.cpu_arch
    submit = args.assemble or args.disassemble

    response = run_query(instructions, arch, submit)
    sc = get_shellcode(response)
    print(sc)


if __name__ == "__main__":
    main()
