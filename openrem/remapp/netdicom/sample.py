import argparse

def my_func_that_return_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('foo', default=False, help='foo help')
    parser.add_argument('bar', default=False)

    subparsers = parser.add_subparsers()

    subparser = subparsers.add_parser('install', help='install help')
    subparser.add_argument('ref', type=str, help='foo1 help')
    subparser.add_argument('--upgrade', action='store_true', default=False, help='foo2 help')

    return parser


if __name__ == '__main__':
    parser = my_func_that_return_parser()
    args = parser.parse_args()
    print(args.accumulate(args.path))
