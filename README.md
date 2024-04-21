# Discord AI Reply Bot

## Description

This is a Discord Selfbot that uses Bing AI Chat (Sdyney) model to auto reply messages in Discord servers.

## Usage

1. Create a Discord bot and get the token. (Self bot is supported too, meaning you can use personal account tokens)
2. write your setting in `config.json`.
3. Create `basePrompt.txt`, and write whatever you want in.
3. Install the dependencies by running `pip install -r requirements.txt`.
4. Run `main.py`.

## NOTICE

**Since discord.py-self don't update anymore, you should edit the source code to make it work properly.**

*utils.py*

line 1474 `build_url = 'https://discord.com/assets/' + re.compile(r'assets/+([a-z0-9]+\.[a-z0-9]+)\.js').findall(login_page)[-2] + '.js'`

line 1477 `build_index = build_file.find('buildNumber') + 26`

## License

[GNU General Public License v3.0](LICENSE)

## Contact

Discord: @t.tw
