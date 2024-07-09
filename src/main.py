import argparse
import os
import pathlib

DATA_DIR = '.local/share/webman/'
parser = None
scrapers=['gfg', 'react', 'flutter', 'express', 'python']

def main():
    HOME = os.getenv('HOME')

    if HOME == None:
        print('Error: HOME environment not set')
        return
    else:
        global DATA_DIR
        DATA_DIR = os.path.join(HOME, DATA_DIR)

    global parser
    parser = argparse.ArgumentParser(description='view web docs in cli')

    subparsers = parser.add_subparsers()

    search_parser = subparsers.add_parser('search', help='search web for docs')
    search_parser.set_defaults(func=search)

    search_parser.add_argument('scraper', type=str, nargs=1, 
                        choices=scrapers,
                        help='select documentation topic')

    search_parser.add_argument('query', type=str, nargs=1,
                        help='search query')

    doc_parser = subparsers.add_parser('doc', help='query cached docs')
    doc_parser.set_defaults(func=doc)

    doc_parser.add_argument('action', nargs=1, type=str, choices=['show', 'remove'], help='action to perform')
    doc_parser.add_argument('source', nargs=1, choices=scrapers, help='target source')

    cli_parser = subparsers.add_parser('cli', help='run as interactive cli')
    cli_parser.set_defaults(func=cli)

    args = parser.parse_args()
    args.func(args)

def search(args):
    target_dir = os.path.join(DATA_DIR, args.scraper[0])
    target_path = os.path.join(target_dir, args.query[0])
    if os.path.exists(target_path):
        print('Article already cached, displaying it..')
        cat_file(target_path)
        return
        
    article = None
    match args.scraper[0]:
        case 'gfg': 
            article = f'gfg {args.query[0]}'
        case 'react':
            article = f'react {args.query[0]}'
        case 'flutter':
            article = f'flutter {args.query[0]}'
        case 'express':
            article = f'express {args.query[0]}'
        case 'python':
            article = f'python {args.query[0]}'

    if article == None:
        article = f'ai {args.query[0]}'

    print(article)
    
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

    with open(target_path, 'w') as f:
        f.write(article)

def doc(args):
    match args.action[0]:
        case 'show':
            show(args)
        case 'remove':
            remove(args)

def cli(ar):
    exit = False
    while not exit:
        print('uwu ', end='')
        command = input()
        match command.strip():
            case 'exit':
                exit = True
            case 'cli':
                print('Already running a cli session!!')
            case _: 
                args = None
                try:
                    args = parser.parse_args(command.split())
                except SystemExit:
                    continue
                args.func(args)

def show(args):
    path = os.path.join(DATA_DIR, args.source[0])
    files = os.listdir(path)
    file_name = pick_file(files)
    cat_file(os.path.join(path, file_name))

def cat_file(path):
    file = open(path, "r")
    print(file.read())
    file.close()

def remove(args):
    path = os.path.join(DATA_DIR, args.source[0])
    files = os.listdir(path)
    file_name = pick_file(files)
    file = os.path.join(path, file_name)
    pathlib.Path(file).unlink()

def pick_file(files):
    for index, file in enumerate(files):
        print(f'{index} {file}')
    return files[get_index(len(files))]
    
def get_index(range):
    while True:
        print('Which file:')
        index = input()
        try:
            index = int(index)
        except ValueError:
            print('Index not number')
            continue
        if index < 0 or index > range:
            print('Index out of bounds')
        else:
            return index

if __name__ == "__main__":
    main()
