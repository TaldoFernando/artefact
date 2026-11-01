import argparse
import json
from pathlib import Path

from .agent import Agent


def main():
    parser = argparse.ArgumentParser(description="Empório da Música local assistant")
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--trace", action="store_true", help="Display retrieved evidence; local development only")
    args = parser.parse_args()
    try:
        agent = Agent(args.data_dir)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Cannot load source data: {exc}\n")
    print("Mel: Hi! Your music starts here. How can I help? (/reset, /quit)")
    while True:
        try:
            text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text == "/quit":
            break
        if text == "/reset":
            agent.history.clear()
            print("Mel: Conversation cleared.")
            continue
        print("Mel:", agent.reply(text))
        if args.trace:
            print(json.dumps(agent.last_trace, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
