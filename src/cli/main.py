import argparse

def main():
    parser = argparse.ArgumentParser(description='view web docs in cli')

    subparsers = parser.add_subparsers(help='subcommand help')

    search_parser = subparsers.add_parser('search', help='search web for docs')
    search_parser.set_defaults(func=search)

    search_parser.add_argument('scraper', type=str, nargs=1, 
                        choices=['gfg', 'react', 'flutter', 'express', 'python'],
                        help='select documentation topic')

    search_parser.add_argument('query', type=str, nargs=1,
                        help='search query')

    doc_parser = subparsers.add_parser('doc', help='query cached docs')
    doc_parser.set_defaults(func=doc)

    doc_parser.add_argument('action', nargs=1, type=str, choices=['show', 'remove'], help='action to perform')
    doc_parser.add_argument('index', nargs='+', type=int, help='doc index')

    args = parser.parse_args()

    print(args)
    args.func(args)

def search(args):
    match args.scraper[0]:
        case 'gfg': 
            print('gfg')
        case 'react':
            print('react')
        case 'flutter':
            print('flutter')
        case 'express':
            print('express')
        case 'python':
            print('python')

def doc(args):
    match args.action[0]:
        case 'show':
            print('showing')
        case 'remove':
            print('removing')
    print(args.index[0])

def clean():
    print("cleaning")


if __name__ == "__main__":
    main()
