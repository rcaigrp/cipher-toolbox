# Hunts for predictable security tokens

These hunts assume an `AuthTokenEvents` table populated by the application with `TimeGenerated`, `Application`, `TokenType`, `Event`, `Outcome`, `TokenFingerprint`, `IssuanceId`, and `SourceIP`. Map the names and event values to your telemetry before running the queries. Populate `TokenFingerprint` only at issuance using a keyed HMAC with a dedicated telemetry key. Keep raw tokens, reset URLs, and the HMAC key out of logs. Use a stable issuance ID across telemetry retries.

## Same token issued by independent operations

```kusto
AuthTokenEvents
| where TimeGenerated > ago(7d)
| where Event == "issued" and isnotempty(TokenFingerprint) and isnotempty(IssuanceId)
| summarize by Application, TokenType, TokenFingerprint, IssuanceId
| summarize DistinctIssuances = count() by Application, TokenType, TokenFingerprint
| where DistinctIssuances > 1
| order by DistinctIssuances desc
```

Check whether retries reuse the issuance ID and whether intentional reissuance explains the match. An unexpected duplicate warrants review of token generation, invalidation, and redemption history. A predictable generator can produce distinct tokens, so a clean result does not rule out exposure.

## Failed redemptions followed by success from one source

```kusto
AuthTokenEvents
| where TimeGenerated > ago(24h)
| where Event == "redeemed" and isnotempty(SourceIP)
| summarize Failures = countif(Outcome == "failure"),
            LastFailure = maxif(TimeGenerated, Outcome == "failure"),
            LastSuccess = maxif(TimeGenerated, Outcome == "success")
    by Application, TokenType, SourceIP, Window = bin(TimeGenerated, 15m)
| where Failures >= 10 and LastSuccess > LastFailure
| order by Failures desc
```

Ten failures in 15 minutes is a starting threshold. Shared egress and routine user retries can produce matches. Fixed windows can split a burst, and successful prediction may leave no failed attempts. Use findings to prioritize review of issuance and redemption logs.

## Source review

Trace reset, invitation, session, and API token creation back to the randomness provider. Prioritize paths that draw from `Strong::Random`, Perl `rand`, Python `random`, PHP `mt_rand`, or JavaScript `Math.random`, or derive tokens from timestamps and public identifiers. Confirm that each candidate supplies bytes to a security token before recording exposure. The local check is a Perl-oriented inventory aid and requires this follow-up.

The queries are templates pending validation against the team's telemetry schema.
