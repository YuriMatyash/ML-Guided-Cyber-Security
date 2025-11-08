# Help Wanted: Vietnamese Actors Using Fake Job Posting Campaigns to Deliver Malware and Steal Credentials


[**https://cloud.google.com/blog/topics/threat-intelligence/vietnamese-actors-fake-job-posting-campaigns**](https://cloud.google.com/blog/topics/threat-intelligence/vietnamese-actors-fake-job-posting-campaigns)

## <u>students</u>
- Yuri Matyash
- Bar Sberro
- Sagi Pichon
- Guy Dazanshvili

## <u>Goal</u>

To trick people with fake job postings so they'll open a booby-trapped
file or log in to a fake portal, then steal their company
credentials/sessions and take over business ad/social accounts. The
point is to make money - either by running paid ads with the victim's
stolen money or by selling the stolen accounts.

## <u>Tactics, Techniques and the Behavior</u>
Here's a comprehensive list of the tactic, technique used
and the observed behavior order by the sequence of the events.

**Tactic:** Initial Access\
**Technique:** [T1566](https://attack.mitre.org/techniques/T1566/) - Phishing\
**Behavior:** The attackers initiate contact by sending messages on
LinkedIn or via email (\"Actors\... reach out to targets via email or
social media platforms like LinkedIn\"). They use social engineering to
\"Lure targets with legitimate-looking job descriptions\" to get them to
engage.

**Tactic:** Execution\
**Technique:** [T1204.002](https://attack.mitre.org/techniques/T1204/002/) - User Execution: Malicious File\
**Behavior:** The user is tricked into running the malware themselves.
The attacker provides a \"ZIP archive\... purport\[ing\] to be a
\'technical assessment\'\" and then the \"victim is instructed to open
the file\... (e.g., Questionare.exe).\"

**Tactic:** Defense Evasion\
**Technique:** [T1027](https://attack.mitre.org/techniques/T1027/) - Obfuscated Files or Information\
**Behavior:** The malware actively hides its true nature. \"The .NET
loader\... is obfuscated.\" It also evades disk-based scanners by
\"loads the second-stage payload, NVCRACK, into memory.\"

**Tactic:** Credential Access\
**Technique:** [T1555.003](https://attack.mitre.org/techniques/T1555/003/) - Credentials from Web Browsers\
**Behavior:** The backdoor steals saved login information, as it
\"steals browser data from web browsers\... including cookies and stored
credentials.\"

**Tactic:** Collection\
**Technique:** [T1005](https://attack.mitre.org/techniques/T1005/) - Data from Local System\
**Behavior:** The malware searches the victim\'s computer for specific
files related to the financial goal, as it \"steals data associated with
cryptocurrency wallets.\"

## <u>End Results</u>
They managed to compromise some corporate advertising/social media accounts, get around multi-factor
authentication in some cases (by grabbing sessions/credentials), and use
those accounts to run ad campaigns or resell the access for profit. In
short: real account takeovers and direct monetization.
