import argparse
from rss.utils.post_alert import post_alert


def create_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CAP RSS utilities")
    subparser_help = "Utilities for the CAP RSS API and CAP generator." \
        "Choose between the following modes: generate-alerts, "\
        "post-alerts, write-cap, test-server"
    subparsers = parser.add_subparsers(dest="entry", help=subparser_help)

    # write_parser = subparsers.add_parser(
    #     "write", help="Write a CAP file with the specified parameters."
    # )
    # generate_parser = subparsers.add_parser(
    #     "generate", help="Generate new alerts and add the to the database. "
    #                      "Use only for development purposes"
    # )

    post_parser = subparsers.add_parser(
        "post", help="Post a new alert to the API."
    )

    post_parser.add_argument(
        "--date",
        "-d",
        type=str,
        help="Date time of the alert."
    )
    post_parser.add_argument(
        "--states",
        "-s",
        nargs="+",
        type=str,
        help="List of states where the alert was issued."
    )
    post_parser.add_argument(
        "--region",
        "-r",
        type=int,
        help="Region code of the alert."
    )
    post_parser.add_argument(
        "--id",
        "-i",
        type=str,
        help="Identifier of the alert."
    )
    post_parser.add_argument(
        "--event",
        "-e",
        action="store_true",
        help="Whether the alert is an event"
    )
    post_parser.add_argument(
        "--refs",
        "-rf",
        nargs="+",
        type=str,
        help="Identifiers of references of the alert (optional).",
        default=None
    )
    post_parser.add_argument(
        "--url",
        "-u",
        type=str,
        default="http://localhost:5000",
        help="The url of the API (default localhost:5000)."
    )

    args = parser.parse_args()
    return args


def main():
    args = create_parser()
    if args.entry == "post":
        post_alert(
            args.url,
            args.date,
            args.states,
            args.region,
            args.id,
            args.event,
            args.refs
        )
    else:
        raise ValueError(f"Invalid mode {args.entry}")


if __name__ == "__main__":
    main()
