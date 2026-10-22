import sys

from tally import total


def main():
    print(total(open(path).read() for path in sys.argv[1:]))


if __name__ == "__main__":
    main()
