rule GPGME_Receiver_Double_Free_Diagnostic
{
    meta:
        description = "Allocator error triage in logs, crash artifacts or memory from a verified OpenPGP receiver"
        reference = "https://lists.gnupg.org/pipermail/gnupg-announce/2026q4/000517.html"
        scope = "Generic diagnostic. Correlate with untrusted input and the loaded GPGME version."
    strings:
        $diagnostic1 = "double free or corruption" ascii nocase
        $diagnostic2 = "free(): double free detected" ascii nocase
    condition:
        any of them
}
