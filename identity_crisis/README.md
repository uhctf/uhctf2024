# Identity Crisis

<!-- crypto, forensics, osint, reversing, stegano, websec, misc -->
* Category: **reversing**

<!-- * "uhctf{...}": must match regex "uhctf{([a-z0-9]+-)*[0-9a-f]{6}}" -->
<!-- * "free-form": anything goes, mention in description what to look for -->
* Flag Format: **uhctf{...}**

<!-- {{FLAG_TYPE}} can be "static" or "regex" -->
* Flags: <details><summary>CLICK TO SHOW</summary><ul><ul>
<li>static: <code>uhctf{wh0-3v3n-u535-w1nd0w5-882cb2}</code></li>
</ul></ul></details>

<!-- Only enter people's first name in lowercase, it will be changed later -->
* Credits:
    * Mihály

<!-- {{HINT_COST}} is a percentage of the challenge's total value -->
<!-- {{HINT_DESCRIPTION}} explains what exactly the hint will help with -->
* Hints: <ul><ul>
<li><details>
    <summary><strong>10%</strong>: Handy tool</summary>
    [CFF Explorer](https://ntcore.com/?page_id=388) is a PE viewer and editor. It allows us to easily change even headers of a PE file!
</details></li>
<li><details>
    <summary><strong>25%</strong>: What should I look for?</summary>
    The PE file format is a generic container used by Windows. A PE is pretty flexible! An EXE is a type of directly executable PE, but a DLL is executable code that should be called by other programs. A PE can also just store binary data and not be executable at all! All of this is indicated by various "characteristics" in the PE file header. Maybe the DLL you were given should not be seen as a DLL after all...? Read more about the PE file type here: https://learn.microsoft.com/en-us/windows/win32/debug/pe-format#file-headers.
</details></li>
</ul></ul>

## Description
I've been feeling off lately... Everyone says I'm a DLL. In the morning in the mirror, the *header* I see is a DLL. But deep inside there is a different person. Maybe... just maybe I am something after all? Maybe I can change this *characteristic* about myself? Would that be okay?

Note: no decompiler or debugger is required for this challenge.
