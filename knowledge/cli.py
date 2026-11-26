import argparse
import sys

from knowledge.db import SQLiteStorage
from knowledge.service import KnowledgeService


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="knowledge",
        description="A simple command-line knowledge base.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    add_parser = subparsers.add_parser(
        "add",
        help="Add a new knowledge item.",
    )
    add_parser.add_argument("title", help="Item title.")
    add_parser.add_argument("content", help="Item content.")

    subparsers.add_parser(
        "list",
        help="List all knowledge items.",
    )

    show_parser = subparsers.add_parser(
        "show",
        help="Show a knowledge item.",
    )
    show_parser.add_argument(
        "id",
        type=int,
        help="ID of the item.",
    )

    search_parser = subparsers.add_parser(
        "search",
        help="Search knowledge items.",
    )
    search_parser.add_argument(
        "query",
        help="Text to search for.",
    )

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete a knowledge item.",
    )
    delete_parser.add_argument(
        "id",
        type=int,
        help="ID of the item.",
    )

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    storage = SQLiteStorage("knowledge.db")
    service = KnowledgeService(storage)

    try:
        if args.command == "add":
            item = service.add_item(args.title, args.content)

            print(f"Knowledge item created successfully!")
            print(f"ID: {item.id}")
            print(f"Title: {item.title}")

        elif args.command == "list":
            items = service.list_all()

            if not items:
                print("No knowledge items found.")
                return

            for item in items:
                print(f"{item.id} | {item.title}")

        elif args.command == "show":
            item = service.get_by_id(args.id)

            print(f"ID: {item.id}")
            print(f"Title: {item.title}")
            print(f"Content: {item.content}")

        elif args.command == "search":
            items = service.search_items_by_word(args.query)

            if not items:
                print("No matching knowledge items found.")
                return

            for item in items:
                print(f"{item.id} | {item.title}")

        elif args.command == "delete":
            service.delete_item(args.id)
            print(f"Knowledge item {args.id} deleted successfully.")

    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()