from utils import parse, DocumentPair, traverseDir

def main():
    args = parse()
    flags = list((args.csv, args.xlsx, args.html))
    if not args.dir:
        if args.doc1 is None or args.doc2 is None:
            print("No doc entered")
            exit(0)
        twoDocs = DocumentPair(args.doc1, args.doc2)
        print(twoDocs.dotProduct())
    else:
        if not (args.doc1 is None and args.doc2 is None):
            print("Ignoring mentioned doc and working on dir")
        finalOutput = traverseDir(args.dir, flags, args.threshold)

if __name__ == "__main__":
    main()