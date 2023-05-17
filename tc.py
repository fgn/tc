#!/usr/bin/env python3

import sys
import tiktoken
from argparse import ArgumentParser
from pathlib import Path
import configparser

class TokenCounter:
    def __init__(self, model):
        self.model = model

    def count_tokens(self, content):
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            encoding = tiktoken.get_encoding(self.model)
        return len(encoding.encode(content))

class ConfigManager:
    @staticmethod
    def read_config():
        home = Path.home()
        config_path = home / ".config" / "tokencounter"
        config_path.mkdir(parents=True, exist_ok=True)
        config_file = config_path / "config.ini"
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    @staticmethod
    def get_model_name(config):
        return config.get('DEFAULT', 'model', fallback='gpt-3.5-turbo-0301')

def print_results(file, content, args, counter):
    results = []
    if args.lines or not any([args.tokens, args.chars, args.bytes]):
        total_lines = content.count('\n')
        results.append(total_lines)
    if args.tokens or not any([args.lines, args.chars, args.bytes]):
        total_tokens = counter.count_tokens(content)
        results.append(total_tokens)
    if args.chars or not any([args.lines, args.tokens, args.bytes]):
        total_chars = len(content)
        results.append(total_chars)
    if args.bytes or not any([args.lines, args.tokens, args.chars]):
        total_bytes = len(content.encode('utf-8'))
        results.append(total_bytes)

    if (args.bytes and args.tokens) or not any([args.lines, args.tokens, args.chars]):
        avg_bytes_per_token = total_bytes / total_tokens
        formatted_result = f"{avg_bytes_per_token:.3f}"
        results.append(f"bytes / token = {formatted_result}")

    results.append(file)
    print(*results)

def main():
    parser = ArgumentParser(description="Count tokens in a text using a specific model.")
    parser.add_argument("files", type=str, nargs='*', help="The files to count tokens.")
    parser.add_argument("-t", "--tokens", action="store_true", help="Print the token counts.")
    parser.add_argument("-b", "--bytes", action="store_true", help="Print the byte counts.")
    parser.add_argument("-c", "--chars", action="store_true", help="Print the character counts.")
    parser.add_argument("-l", "--lines", action="store_true", help="Print the newline counts.")
    parser.add_argument("--model", type=str, help="The model to use for token counting.")
    args = parser.parse_args()

    config = ConfigManager.read_config()
    model_name = ConfigManager.get_model_name(config)

    if args.model:
        model_name = args.model

    counter = TokenCounter(model_name)

    if not args.files or '-' in args.files:
        content = sys.stdin.read()
        print_results("stdin", content, args, counter)
    else:
        for file in args.files:
            with open(file, 'r') as f:
                content = f.read()
            print_results(file, content, args, counter)

if __name__ == "__main__":
    main()
