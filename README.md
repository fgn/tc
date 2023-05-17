# tc: TokenCounter
`tc` is a Python tool, built as a wrapper around OpenAI's `tiktoken` library, that enables easy counting of tokens, lines, characters, and bytes in a text file or via standard input. It's conceived in the vein of the UNIX `wc` (word count) command, and it is particularly designed to assist developers and AI practitioners in quickly estimating token usage for different AI models.

However, it's essential to understand that `tc` is primarily intended for initial, quick estimates. Accurately calculating the total token count for complex AI tasks, such as chat completions, requires a more sophisticated approach. For a comprehensive guide on precise token counting in such scenarios, please refer to this [OpenAI Cookbook example](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb) that outlines the usage of `tiktoken`.

Here's a quick reference table for the encodings used by various models:

| Model | Encoding |
| ----- | -------- |
| gpt-4 | cl100k_base |
| gpt-3.5-turbo | cl100k_base |
| text-embedding-ada-002 | cl100k_base |
| Codex | p50k_base |

Please note that this project and its developer have no affiliation with OpenAI.


## Installation

To install the `tc` tool, you first need to clone the repository to your local machine. After cloning, navigate to the directory containing the setup file and install the package using pip.

```bash
git clone https://github.com/fgn/tc.git
cd tc
pip install -e .
```

## Usage

The `tc` tool can be used in two ways:

1. **Directly from the command line**: You can provide file names as arguments, and the tool will process each file and output the counts.

2. **Through standard input**: If no file names are provided or if '-' is provided as an argument, the tool will read the input from stdin.

You can control the output of the tool using command-line flags:

- `-t` or `--tokens`: Output the token counts.
- `-b` or `--bytes`: Output the byte counts.
- `-c` or `--chars`: Output the character counts.
- `-l` or `--lines`: Output the newline counts.
- `--model`: Specify the model to use for token counting. The default model is 'gpt-3.5-turbo-0301' or as defined in the config file.

If none of these flags are provided, the tool will output all counts by default.

Here's an example of how to use the tool:

```bash
$ tc test.txt setup.py LICENSE
1 17 72 72 bytes / token = 4.235 test.txt. # 1 line, 17 tokens, 72 char, 72 bytes
15 66 274 274 bytes / token = 4.152 setup.py
21 219 1060 1060 bytes / token = 4.840 LICENSE
```

## Output

The output is a series of numbers, each representing a count for the metric you've specified. Here's what each number means:

1. **Total lines**: This is the number of newlines in the text.
2. **Total tokens**: This is the number of tokens in the text, as counted by the specified model.
3. **Total chars**: This is the total number of characters in the text.
4. **Total bytes**: This is the total number of bytes in the text when encoded as UTF-8.
5. **Average bytes per token**: This is the average number of bytes per token in the text.

Each count is followed by the name of the file or `stdin` if the input came from standard input.

Please note, average bytes per token is only calculated and displayed if both `--bytes` and `--tokens` flags are set or if no flags are set (default behavior).

## Configuration

The tool uses a configuration file stored in `~/.config/tc/config.ini`. You can specify the default model to use for token counting in this file. If the model is not specified in the config file, the tool uses 'gpt-3.5-turbo-0301' as the default model.

Example config file:

```
[DEFAULT]
model = gpt-3.5-turbo-0301
```

You can also override the model specified in the config file by using the `--model` command-line flag.
