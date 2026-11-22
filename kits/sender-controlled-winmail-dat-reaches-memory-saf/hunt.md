# Hunt for automatic TNEF processing

Use a seven-day lookback to identify TNEF deliveries to automatic processing mailboxes. Correlate with decoder crashes using the message or queue ID when available, or the worker and timestamp otherwise. A filename match indicates potential exposure. A nearby crash warrants investigation and has several possible causes.

## Splunk SPL

Replace the index and field names with your local mappings. Expand any multivalue attachment field before filtering if your ingestion groups attachments by message.

```spl
index=mail_logs earliest=-7d (attachment_name="winmail.dat" OR attachment_mime="application/ms-tnef" OR attachment_mime="application/vnd.ms-tnef")
| table _time host message_id sender recipient attachment_name attachment_mime
```

```spl
index=linux earliest=-7d "ytnef" ("segfault" OR "SIGSEGV" OR "SIGABRT" OR "heap-buffer-overflow" OR "out-of-bounds" OR "status=11/SEGV" OR "status=6/ABRT")
| table _time host source _raw
```

## Microsoft Defender XDR KQL

```kusto
EmailAttachmentInfo
| where Timestamp > ago(7d)
| where FileName =~ "winmail.dat"
| project Timestamp, NetworkMessageId, SenderFromAddress, RecipientEmailAddress, FileName, SHA256
| order by Timestamp desc
```

Match results against the mail-to-calendar or automated mailbox inventory. Review Linux worker logs in the platform that collects them.

## Local text and JSON logs

Substitute your log path. The JSON example expects one object per line with optional string fields named `attachment_name`, `attachment_mime`, and `message`.

```bash
grep -Ein 'winmail\.dat|application/(ms-tnef|vnd\.ms-tnef)' mail.log
grep -Ein 'ytnef' worker.log | grep -Ei 'segfault|SIGSEGV|SIGABRT|heap-buffer-overflow|out-of-bounds|status=11/SEGV|status=6/ABRT'
jq -c 'select(((.attachment_name // "") | ascii_downcase) == "winmail.dat" or ((.attachment_mime // "") | test("^application/(ms-tnef|vnd\\.ms-tnef)([[:space:]]*;|$)"; "i")) or (((.message // "") | test("ytnef"; "i")) and ((.message // "") | test("segfault|SIGSEGV|SIGABRT|heap-buffer-overflow|out-of-bounds|status=11/SEGV|status=6/ABRT"; "i"))))' events.jsonl
```
