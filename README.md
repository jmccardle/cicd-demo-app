# cicd-demo-app

A small guestbook web app, used to demo [cicd-ref-arch](https://forge.goblincorps.com/ffwf/cicd-ref-arch):
the code here belongs to the app's developers, and the platform builds, scans, deploys and gates it.

| You own (this repo) | The platform owns |
|---|---|
| `app.py`, `templates/`, `tests/` | build, scans, deploys, URLs, scale to zero |
| `Dockerfile`, `deploy/` (kustomize base) | the security policy floor and the prod gate |
| `cicd.yaml`: test command, URL patterns, idle time | promotion approval and scheduling |
| `security/`: suppressions with a reason and an expiry | `.forgejo/workflows/cicd.yaml` (installed at enrollment) |

- **Push to `main`:** tests, build, scans, then live at `https://demo-dev.<cluster>.<zone>/`.
- **Push another branch:** the same, at `https://demo-<branch>.<cluster>.<zone>/`. Deleting the branch removes it.
- **Prod** (`https://demo.<cluster>.<zone>/`): someone requests a promotion in cicd-ref-arch and someone else approves it.
  The platform re-scans the image then, and refuses it if a fixable high or critical vulnerability, a code or config
  finding, or a secret fails the prod policy.
- **Idle for 15 minutes:** scaled to zero. The next request wakes it, with no error page.

## Working on it

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/flask --app app run
git config core.hooksPath hooks      # secret check before each commit (needs gitleaks)
```

## When a scanner is wrong

Never change code to satisfy a scanner. Record the decision instead, and it is reviewed when the app is promoted:

- **A vulnerability that doesn't affect this app:** an OpenVEX statement in `security/vex.openvex.json`.
- **A code or config finding:** an `ignore` entry in `security/policy.yaml`, with `reason` and `expires`.
- **A secret that isn't one:** its `file:rule:line` fingerprint in `.gitleaksignore`, with a comment.

## Note

Until 0.2.0, `requirements.txt` pinned Werkzeug 3.0.1 on purpose: it has known vulnerabilities, so the demo had
something for the prod gate to refuse (see the history of `requirements.txt`). This app only runs on a private
test cluster.

MIT licensed.
