# swapfile

```
# mkswap -U clear --size 4G --file /swapfile
# swapon /swapfile
```

`/etc/fstab`:

```
/swapfile none swap defaults 0 0
```

```
# swapoff /swapfile
# rm -f /swapfile
```
