from utils import *
import pandas as pd
def main():
    args = parse()
    if not args.dir:
        if args.doc1 is None or args.doc2 is None:
            print("No doc entered")
            exit(0)
        print(twoDocs(args.doc1,args.doc2))
    else:
        if not (args.doc1 is None and args.doc2 is None):
            print("Ignoring mentioned doc and working on dir")
        finalOutput = traverseDir(args.dir, args.threshold)

if __name__ == "__main__":
    main()