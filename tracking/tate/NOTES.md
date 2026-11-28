# Shirudo Tracking Notes

## 2026-11-28

### Project Status
- GitHub: 2421 stars, 258 forks, 124 open issues+PRs, last push 2026-11-28T04:56:30Z
- License: BSD-2-Clause
- Release: test-kernel-45212180772 (2026-11-23)
- Main branch commit: dbdb125 (ci: label and close issues and pull requests that went stale)

### Key Changes Since Last Check-in
- CI/CD improvements: automated labeling of stale PRs/issues, more focused builds
- Documentation: rewrite of CONTRIBUTING.md, FAQ expansion, community channel links
- New upatch features: Java XMLDecoder shield (PR #371), Base64 guard retention fix (PR #368)
- Kernel-related: bpffs ancestry sharing and pivot_root hooking (PR #213)
- Testing: improved status eventlog checking (PR #393)

### GitHub Issues
- #389: docs - clarify compatibility expectations for offline status JSON readers
- #370: upatches - Java XMLDecoder shield with allow list
- #368: upatches - Base64 guard lost after retransformation
- #366: upatches - Java XXE shield
- #379: TPM-checked tree operations, authorization questions

### GitHub PRs
- #77: BPF program targeting improvements
- #85: leverage gen loader attach
- #100: add ksock upatch
- #182: bind full task role to runtime image executables
- #150: docs - update index page copy
- #213: bpf2 - keep bpffs ancestry shared and hook pivot_root
- #251: completion - preserve spaces in completed filesystem paths
- #252: upatch - show listed name's stray bytes like info does

### Key Files/Dirs
- `upatches/`: Directory for shield definitions (e.g., java-base64, java-sql-inj)
- `include/shirudo/upatch.h`: Core upatch header
- `bpf/`: eBPF program files
- `.agents/skills/upatch/SKILL.md`: Agent skill documentation for upatches

### Observations
- Documentation work continues to improve clarity and community engagement
- Several Java-related issues (#366, #368, #370) are being actively addressed in PRs
- Build/test environments may not be fully accessible in this container (no kernel access)