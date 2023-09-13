import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="CAP RSS utilities")
    subparser_help = "Utilities for the CAP RSS API and CAP generator." \
        "Choose between the following modes: generate-alerts, "\
        "post-alerts, write-cap, test-server"
    subparsers = parser.add_subparsers(dest="entry", help=subparser_help)
    # TODO: complete


def main():
    pass


if __name__ == "__main__":
    main()
