# Gmail Empty Trash

Python script to empty Gmail trash using the Gmail API.

## Install

```shell
pip install -r requirements.txt
```

Must enable Gmail API: https://developers.google.com/gmail/api

Then, it's necessary to adjust the `.sample` files with the corresponding information (and remove the `.sample` part of the filename).

## Run

```shell
python main.py
```

**Note**: Use Python 3

## Troubleshooting

### You can't sign in to this app because it doesn't comply with Google's OAuth 2.0 policy for keeping apps secure.

This errors appears sometimes when authenticating for the first time.

1. Make sure `run_local_server` starts a server in `localhost`.
2. `rm token.json`
3. Access `localhost`, but since it may be on a remote server, you need to create an SSH tunnel (apparently the URL must be `localhost`, or else it's seen as insecure by Google) using `ssh -L 8080:127.0.0.1:8080 USER@REMOTE_HOST -p PORT`
4. Start the script and open the URL in a browser.
5. You should see `The authentication flow has completed, you may close this window.` (URL of this page is `localhost`) after going through the dialog.
