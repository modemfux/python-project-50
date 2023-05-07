import argparse
from gendiff.scripts.gendiff import generate_diff


# Allow to show some help via key arguments
parser = argparse.ArgumentParser(
    description='Compares two configuration files and shows a difference.')
parser.add_argument('first_file')
parser.add_argument('second_file')
parser.add_argument('-f', '--format', default='plain')
args = parser.parse_args()


def main():
    return generate_diff(args.first_file, args.second_file)


if __name__ == '__main__':
    print(main())
