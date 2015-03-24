#!/usr/bin/env python
from subprocess import call

def main():
    call(["./process_data.py"])
    call(["./make_pages.py"])

if __name__ == '__main__':
    main()
