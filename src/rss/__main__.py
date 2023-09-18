import argparse
from rss.utils.post_alert import post_alert
from rss.utils.fake import generate_fake_alerts
from rss.utils.write_feed import write_cap_file
from rss.test.server import start_server


def create_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CAP RSS utilities")
    subparser_help = "Utilities for the CAP RSS API and CAP generator."
    subparsers = parser.add_subparsers(dest="entry", help=subparser_help)

    write_parser = subparsers.add_parser(
        "write", help="Write a CAP file with the specified parameters."
    )
    write_parser.add_argument(
        "--date",
        "-d",
        type=str,
        help="Date time of the alert in iso-format."
    )
    write_parser.add_argument(
        "--states",
        "-s",
        nargs="+",
        type=str,
        help="List of states where the alert was issued."
    )
    write_parser.add_argument(
        "--region",
        "-r",
        type=int,
        help="Region code of the alert."
    )
    write_parser.add_argument(
        "--type",
        "-t",
        choices={"alert", "event", "test"},
        default="alert",
        help='The type of the alert. Can be "alert", "event", or "test" (default alert)'
    )
    write_parser.add_argument(
        "--file",
        "-f",
        type=str,
        help="The path of the file where the CAP will be written."
    )

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

    subparsers.add_parser(
        "generate", help="Generate new alerts and add them to the database. "
                         "Use only for development purposes"
    )

    subparsers.add_parser(
        "server", help="Start the test server that generates samples alerts."
                       " This can be used to test the integration of the CAP generator "
                       "with the API"
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
    elif args.entry == "generate":
        generate_fake_alerts()
    elif args.entry == "write":
        write_cap_file(
            args.date,
            args.states,
            args.region,
            args.type,
            args.file
        )
    elif args.entry == "server":
        start_server()
    else:
        raise ValueError(f"Invalid mode {args.entry}")


if __name__ == "__main__":
    main()
