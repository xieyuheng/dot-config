# 查看电池使用情况

## upower

```bash
$ upower --enumerate
/org/freedesktop/UPower/devices/battery_BAT1
/org/freedesktop/UPower/devices/line_power_ACAD
/org/freedesktop/UPower/devices/DisplayDevice
```

```bash
$ upower -i /org/freedesktop/UPower/devices/battery_BAT1
```

## acpi

```bash
$ acpi -b
Battery 0: Discharging, 79%, 04:35:52 remaining

$ acpi -t
Thermal 0: ok, 43.0 degrees C

$ acpi -i
Battery 0: Discharging, 79%, 04:51:36 remaining
Battery 0: design capacity 3615 mAh, last full capacity 2372 mAh = 65%
```

## gnome-power-manager

看耗电历史的统计图：

```bash
$ gnome-power-statistics
```

## tlp

- [项目主页](https://linrunner.de/tlp)

查看电池情况：

```bash
$ sudo tlp-stat -b
```
