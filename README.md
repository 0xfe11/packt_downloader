# Packtpub downloader

Simple script to download the free books from packtpub.

## Usage

For the first time, it will generate an empty access.json if it is not created, be sure to fill that up.

### Filling up access.json

```json
{
  "username": "myuser@host.com",
  "password": "mypassword"
}
```

### Commands

To download all the books,

```command line
  python main.py all
```

To download only one book,

```command line
  python main.py "Mastering Windows PowerShell Scripting - Third Edition" 9781789536669
```
