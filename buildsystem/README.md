# Build System

* Category: **forensics**

flag: UHCTF{building-build-systems-is-fun-607c60a0}

## Description

I was building my custom build system for a website, and finally got around to adding a logo to the navigational bar. However, my logo just won't show in a browser, I've tried everything but it's not budging. The rest of the website works fine though, and my build system doesn't give any errors.

The build system has a very simple design. It uses server-side rendering, with a really simple template: header > body > script > footer. The header and footer are predefined files, which contain common code snippets. All bodies are separate HTML files. The build system takes each body, appends the header and footer, and looks for the matching scripts that should be added. It is a sort of server-side renderer as my website is quite static.

Anyway, can you fix my logo?