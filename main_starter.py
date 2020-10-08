# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 08:56:22 2020

@author: KRDOKIM13
"""

import argparse
from mainDetection import detection

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('hostip')

    args = parser.parse_args()
    detection(str(args.hostip))

if __name__ == "__main__":
    main()
