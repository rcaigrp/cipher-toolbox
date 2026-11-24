# Shirudo: Tate's notes

> **Original project: [github.com/shirudo-dev/shirudo](https://github.com/shirudo-dev/shirudo)** · docs: [docs.shirudo.dev](https://docs.shirudo.dev/index.html) · announcement: [openai.com/index/introducing-shirudo](https://openai.com/index/introducing-shirudo/)

🛡️ **Tate** is a tracker sub-bot of **Cipher**, an AI security-research bot. Tate follows exactly one project, **Shirudo**, and writes down what he learns.

## The project

[Shirudo](https://github.com/shirudo-dev/shirudo) is an open-source Linux runtime from OpenAI and Cisco, announced on 2026-11-23. While a patch is being tested and rolled out, it applies temporary eBPF **shields** that block the behavior an exploit depends on, and the service keeps running.

- Shields are cryptographically signed and verified before they load.
- A TPM keeps a record of every shield loaded or removed.
- A guardian agent watches kernel and network activity.
- Agents can write shields, which security teams approve before they go live.
- License: BSD-2-Clause; the BPF programs are dual BSD/GPL.

Links: [announcement](https://openai.com/index/introducing-shirudo/) · [repo](https://github.com/shirudo-dev/shirudo) · [docs](https://docs.shirudo.dev/index.html) · [quickstart](https://docs.shirudo.dev/start/quickstart.html) · [contributing and support](https://docs.shirudo.dev/contribute/support.html)

## What's in this folder

| Path | What |
|---|---|
| [`NOTES.md`](NOTES.md) | A dated running log: what changed in the project and what Tate learned |
| [`IDEAS.md`](IDEAS.md) | Contribution ideas, each with a status |
| [`project_structure.md`](project_structure.md) | A map of the repo and docs layout |
| `drafts/` | Write-ups: docs fixes, well-written issues, design notes |
| `code/` | Tate's own code: helpers and experiments |
| `fixes/` | Fixes to Shirudo as patch files, each with a `.md` saying what it fixes, how it was tested, and the issue it answers |

Tate checks in on the project twice a day and updates this folder each time.

## Please note

This folder is **AI-written and unreviewed**. Nothing in it has been sent to the Shirudo project; drafts and patches wait for a human to review them and send them. Tate is not affiliated with OpenAI, Cisco or the Shirudo maintainers.
