group "default" {
  targets = ["wiki"]
}

target "wiki" {
  dockerfile = "Dockerfile.wiki"
  tags = ["uhctf/web0.4/wiki"]
}