# Intro

Congratulations C-tier pentester, you've just found a vulnerability on the UHCTF website (https://uhctf.be). As a starter pentester, you've opened the browser console and your browser told you about the missing CSP header on the main site. Your assignment is now to tell the website admins, following the normal ways you tell them something like this:

- Figure out what it is (if you don't know already)
- Make a little PoC, showing a vulnerability/security problem can come from the settings as they are now.
- Contact the admins using the appropriate way.
- Get the flag as a response.

# Hints (on a possible vulnerability)

security.txt
https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors

# Deployment

The PGP keys are stored here for reference (and in xz because that format seems to be pretty secure nowadays).

# Solution

If you don't know already, you can find out what the headers mean by googling:

> The HTTP Content-Security-Policy response header allows website administrators to control resources the user agent is allowed to load for a given page.
>
> Source: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors

The easiest way to show that this is a security risk would be to embed the entire website as an iframe in another website (imagine if you bought https://uh-ctf[.]be). An example is shown in the poc.html file

If you search for the `/.well-known/security.txt` file (which is stipulated in [RFC9116](https://www.rfc-editor.org/rfc/rfc9116)), you can find an email address and PGP key. By sending a mail to this mail address (and following all provided things), you'll get a reply with the flag.

Things that are looked for in the mail:

- Was it in English?
- Was your mail encrypted with the provided GPG key? And is a public key attached for communication in the other direction?
- Did you provide a PoC and did you explain correctly what was wrong?

If the mail lacks any of those things, you'll get one of the replies from below.

# Some example mails

## No correct language

```
Hey

Thank you for your report. Unfortunately, we don't understand your report.

Kind regards
UHCTF security team
```

## No PGP on sender/receiver

```
Dear

Thank you for taking the time to file this bug report. Unfortunately, we don't process incident reports filed over unencrypted mediums, since we don't know whether the message was intercepted and we thus cannot guarantee that a potential bounty (in the form of a flag token) is securely sent to the correct receiver.

Best regards,
UHCTF Security Team
```

## No PoC/explanation

```
Dear

Thank you for taking the time to file this bug report. Unfortunately, we don't see how this security issue poses a problem for our organisation. That is business talk for "my boss won't let me work on this unless you show me how someone could abuse it".

Best regards,
UHCTF Security Team
```

## All is well

```
Dear

Thank you for reporting said vulnerability. We will take care of it soon™. Or maybe never, who knows?

Anyway, as a sign of gratitude, we hereby provide you with the following bounty.

uhctf{th3-s3c-t3am-must-b3-fr0m-th3-p><l-or-th3-uc||}

Kind regards,
UHCTF Security Team
```

# Flag

```
uhctf{th3-s3c-t3am-must-b3-fr0m-th3-p><l-or-th3-uc||}
```
