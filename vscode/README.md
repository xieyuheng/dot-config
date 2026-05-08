# vscode config sync

## Linux

sync:

```
cp ~/.config/Code\ -\ OSS/User/keybindings.json .
cp ~/.config/Code\ -\ OSS/User/settings.json .
code-oss --list-extensions > extensions.txt
```

install:

```
cp keybindings.json settings.json ~/.config/Code\ -\ OSS/User
cat extensions.txt | xargs -n 1 code-oss --install-extension
```

## Windows

install:

```
Get-Content .\extensions.txt | ForEach-Object { 
    code --install-extension $_ --force
    if ($LASTEXITCODE -ne 0) { Write-Host "安装失败: $_" -ForegroundColor Red }
}
```
