import argparse
import csv
import logging

import os

LABEL_SEPARATOR = ':'
ID_SEPARATOR = '_'


def read_data(directory):
    for subdir in next(os.walk(directory))[1]:
        label = subdir
        subpath = os.path.join(directory, subdir)
        for file in next(os.walk(subpath))[2]:
            filename = os.path.join(subpath, file)
            with open(filename, mode='r', encoding='utf-8') as inputfile:
                text = inputfile.read()
                yield directory + ID_SEPARATOR + file, text, label


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    parser.add_argument('name', help='name of the classification schema', type=str)
    parser.add_argument('output_file', help='output filename', type=str)
    parser.add_argument('directory',
                        help='Paths to dirs contaning the labeled documents (label=subdir, document=file in subdir)',
                        type=str,
                        nargs='+')
    args = parser.parse_args()

    logger = logging.getLogger('sys.argv[0]')
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    if args.verbose:
        logger.setLevel(logging.INFO)
        logger.info('Verbose output')

    schema_name = args.name

    with open(args.output_file, mode='w', encoding='utf-8') as output:
        csvout = csv.writer(output)
        labels = set()
        for directory in args.directory:
            data_generator = read_data(directory)
            for id, text, label in data_generator:
                labels.add(label)
                csvout.writerow([id, text, schema_name + LABEL_SEPARATOR + label])
