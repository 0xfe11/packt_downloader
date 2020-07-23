# Packtpub downloader

Simple script to download the free books from packtpub. Currently there are two versions, async and non async versions of the downloader.
The async version currently is useful for batch downloading all the books but is experimental. The non async version is useful for downloading
one book.

All files will be downloaded to downloaded folder.

## Requirements

Following packages are needed,

- requests
- aiohttp

```bash
pip install requests aiohttp
```

## Usage

For the first time, it will generate an empty access.json if it is not created, be sure to fill that up.

### Creating access.json

```json
{
  "username": "myuser@host.com",
  "password": "mypassword"
}
```

### Commands for non-async version

To download all the books,

```bash
  python main.py all
```

To download only one book, specify name of book to save as and the product id,

```bash
  # e.g.         "Mastering Python"     epub_id
  python main.py "book_name_to_save_as" 1234567891234
```

More details on how to get the product id can be found here on my [blog](https://0xfe11.github.io/posts/downloading-free-books-from-packt/).

### Commands for async version

To download all the books,

```bash
python main_async.py
```
