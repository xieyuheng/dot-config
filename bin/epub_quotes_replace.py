#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EPUB 引号替换工具：把全角弯引号替换成直角引号（含内层嵌套级）。

默认映射：
    “  (U+201C)  →  「  (U+300C)
    ”  (U+201D)  →  」  (U+300D)
    ‘  (U+2018)  →  『  (U+300E)
    ’  (U+2019)  →  』  (U+300F)

处理范围：epub 压缩包内的所有文本条目（.xhtml/.html/.htm/.ncx/.opf/.xml），
字体、图片等二进制条目原样复制，不做任何改动。

打包规则：强制 mimetype 为第一个条目且不压缩（ZIP_STORED），
其余条目保持原压缩方式 —— 这是 EPUB 规范硬性要求，否则部分阅读器拒读。

用法：
    python3 epub_quotes_replace.py 输入.epub                 # 输出 <输入名>-quotes.epub
    python3 epub_quotes_replace.py 输入.epub -o 输出.epub     # 指定输出路径
    python3 epub_quotes_replace.py 输入.epub --in-place       # 原地安全替换（临时文件+原子改名）
    python3 epub_quotes_replace.py 输入.epub --dry-run        # 只统计预览，不写任何文件
    python3 epub_quotes_replace.py 输入.epub --map '《:〈'    # 追加额外的成对映射

处理完成后自动验证：
    1) 所有被替换过的文本条目中源引号残留为 0；
    2) mimetype 是第一个条目且未压缩；
    验证失败则删除输出文件并返回非零退出码，绝不留下坏文件。
"""

import argparse
import os
import sys
import tempfile
import zipfile

DEFAULT_MAP = {
    "“": "「",  # U+201C -> U+300C
    "”": "」",  # U+201D -> U+300D
    "‘": "『",  # U+2018 -> U+300E
    "’": "』",  # U+2019 -> U+300F
}
TEXT_EXTS = (".xhtml", ".html", ".htm", ".ncx", ".opf", ".xml")
MIMETYPE_NAME = "mimetype"


def parse_extra_map(pairs):
    """解析 --map '源:目标' 参数，追加到默认映射。"""
    extra = {}
    for pair in pairs:
        if ":" not in pair:
            sys.exit(f"[错误] --map 格式应为 源字符:目标字符，收到：{pair!r}")
        src, dst = pair.split(":", 1)
        if len(src) != 1 or len(dst) != 1:
            sys.exit(f"[错误] --map 每一项必须恰好一个字符，收到：{pair!r}")
        if src == dst:
            sys.exit(f"[错误] --map 源与目标相同：{pair!r}")
        extra[src] = dst
    return extra


def scan_text_entries(zf):
    """返回 epub 中所有候选文本条目的文件名列表（按压缩包内顺序）。"""
    return [zi.filename for zi in zf.infolist()
            if not zi.filename.endswith("/")
            and zi.filename.lower().endswith(TEXT_EXTS)]


def decode_or_none(data):
    """尝试解码为 UTF-8（容忍 BOM）。失败返回 None。"""
    try:
        if data.startswith(b"\xef\xbb\xbf"):
            return data.decode("utf-8-sig")
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def count_quotes(text, mapping):
    """统计文本中各源字符出现次数。"""
    return {ch: text.count(ch) for ch in mapping}


def summarize(mapping, counts):
    """把各源字符计数整理成可打印摘要。"""
    return "；".join(f"{src}({n})→{dst}" for src, dst in mapping.items()
                    if (n := counts.get(src, 0)) > 0) or "（无）"


def report_pairing(texts_by_name, mapping, label):
    """报告引号配对失衡的文件（仅作提示，不影响替换）。"""
    open_chars = {ch: dst for ch, dst in mapping.items() if ch in "“‘"}
    close_chars = {ch: dst for ch, dst in mapping.items() if ch in "”’"}
    for name, text in texts_by_name.items():
        for oc, cc in ((open_chars, close_chars),):
            for o, c in zip(oc, cc):
                d = text.count(o) - text.count(c)
                if d:
                    print(f"  [提示] {name}: {o}(开)= {text.count(o)}，"
                          f"{c}(闭)= {text.count(c)}，不平衡 {d:+d}（源文档既有瑕疵）")
    # 仅统计与 label 无关，此函数只负责打印


def replace_in_epub(src_path, dst_path, mapping, do_verify):
    """执行替换并打包。返回 (总替换数, 处理条目数, 跳过条目数)。"""
    total_replaced = 0
    processed = 0
    skipped_decode = []
    with zipfile.ZipFile(src_path, "r") as zin:
        infos = zin.infolist()
        # 强制 mimetype 排第一：单独处理
        mi = next((i for i in infos if i.filename == MIMETYPE_NAME), None)
        if mi is None:
            sys.exit(f"[错误] {src_path} 不是合法的 EPUB：缺少 {MIMETYPE_NAME} 条目")
        rest = [i for i in infos if i.filename != MIMETYPE_NAME]

        with zipfile.ZipFile(dst_path, "w") as zout:
            # 1) mimetype：必须第一个写入，且不压缩
            zout.writestr(zipfile.ZipInfo(MIMETYPE_NAME, mi.date_time),
                          zin.read(mi), zipfile.ZIP_STORED)

            # 2) 其余条目按原顺序复制
            for zi in rest:
                name = zi.filename
                data = zin.read(zi)
                info = zipfile.ZipInfo(name, zi.date_time)
                info.external_attr = zi.external_attr
                info.compress_type = zi.compress_type

                if name.lower().endswith(TEXT_EXTS):
                    text = decode_or_none(data)
                    if text is None:
                        skipped_decode.append(name)
                        zout.writestr(info, data)
                        continue
                    counts = count_quotes(text, mapping)
                    if any(counts.values()):
                        new_text = text.translate(str.maketrans(mapping))
                        data2 = new_text.encode("utf-8")
                        processed += 1
                        total_replaced += sum(counts.values())
                        zout.writestr(info, data2)
                    else:
                        zout.writestr(info, data)
                else:
                    zout.writestr(info, data)

    # ---- 自验收 ----
    if do_verify:
        problems = []
        with zipfile.ZipFile(dst_path, "r") as zout:
            # 结构检查
            first = zout.infolist()[0]
            if first.filename != MIMETYPE_NAME:
                problems.append(f"mimetype 不是第一个条目（实际为 {first.filename}）")
            if first.compress_type != zipfile.ZIP_STORED:
                problems.append("mimetype 没有使用 STORED（不压缩）")
            # 内容检查：候选文本条目中不允许残留源引号
            for name in scan_text_entries(zout):
                if name in skipped_decode:
                    continue
                text = decode_or_none(zout.read(name))
                if text is None:
                    continue
                for ch in mapping:
                    if text.count(ch):
                        problems.append(f"{name} 中仍残留源字符 {ch!r} （{text.count(ch)} 个）")
        if problems:
            os.remove(dst_path)
            sys.exit("[验证失败] 已删除输出文件：\n  - " + "\n  - ".join(problems))
        print("[验证] 通过：mimetype 结构正确，文本条目中无源引号残留。")

    return total_replaced, processed, skipped_decode


def main():
    ap = argparse.ArgumentParser(
        description="EPUB 引号替换工具：全角弯引号 → 直角引号（“”→「」，“‘’”→『』）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例：\n"
               "  python3 epub_quotes_replace.py  book.epub\n"
               "  python3 epub_quotes_replace.py  book.epub -o out.epub\n"
               "  python3 epub_quotes_replace.py  book.epub --dry-run\n")
    ap.add_argument("epub", help="输入 epub 文件路径")
    ap.add_argument("-o", "--output", help="输出路径（默认 <输入名>-quotes.epub）")
    ap.add_argument("--in-place", action="store_true", help="原地替换（自动备份到 .bak）")
    ap.add_argument("--dry-run", action="store_true", help="只统计预览，不写任何文件")
    ap.add_argument("--map", action="append", default=[], metavar="S:D",
                    help="追加映射对（可多次），格式 源字符:目标字符")
    ap.add_argument("--no-verify", action="store_true", help="跳过打包后的自动验证（不推荐）")
    ap.add_argument("--quiet", action="store_true", help="只输出错误信息")
    args = ap.parse_args()

    mapping = dict(DEFAULT_MAP)
    mapping.update(parse_extra_map(args.map))

    # 参数合法性校验（提前到解析阶段，避免被统计逻辑短路）
    if args.in_place and args.output:
        sys.exit("[错误] --in-place 与 -o 不能同时使用")

    if not os.path.isfile(args.epub):
        sys.exit(f"[错误] 文件不存在：{args.epub}")

    # ---- 预览 / 统计阶段（dry-run 与正式运行都要先看一下）----
    try:
        zin = zipfile.ZipFile(args.epub, "r")
    except zipfile.BadZipFile:
        sys.exit(f"[错误] {args.epub} 不是有效的 ZIP/EPUB 文件")

    with zin:
        names = scan_text_entries(zin)
        if not names:
            sys.exit(f"[错误] {args.epub} 中未找到任何文本条目（{TEXT_EXTS}）")
        texts = {}
        totals = {ch: 0 for ch in mapping}
        for name in names:
            text = decode_or_none(zin.read(name))
            if text is None:
                print(f"  [跳过] {name}：无法按 UTF-8 解码，保持不变", file=sys.stderr)
                continue
            texts[name] = text
            c = count_quotes(text, mapping)
            for ch, n in c.items():
                totals[ch] += n

    total_src = sum(totals.values())
    if total_src == 0:
        print(f"[结论] {args.epub} 中未找到任何待替换的字符（"
              + summarize(mapping, totals) + "），无需处理。")
        return 0

    print(f"[统计] 待替换 {total_src} 个字符，分布在 {len(texts)} 个文本条目中：")
    print("  " + summarize(mapping, totals))
    print("[配对] 引号配对检查（仅提示，不影响替换）：")
    report_pairing(texts, mapping, "引号")

    if args.dry_run:
        print("\n[预览模式] 未写任何文件。实际执行将输出：",
              args.output or os.path.splitext(args.epub)[0] + "-quotes.epub")
        return 0

    # ---- 确定输出路径 ----
    if args.in_place:
        # 先备份
        bak = args.epub + ".bak"
        import shutil
        shutil.copy2(args.epub, bak)
        print(f"[备份] 原文件已备份到 {bak}")
        work = tempfile.NamedTemporaryFile(
            dir=os.path.dirname(os.path.abspath(args.epub)),
            prefix=".epub_tmp_", suffix=".epub", delete=False)
        work.close()
        tmp_path = work.name
        final_path = args.epub
    else:
        final_path = args.output or (os.path.splitext(args.epub)[0] + "-quotes.epub")
        if os.path.abspath(final_path) == os.path.abspath(args.epub):
            sys.exit("[错误] 输出路径与输入相同，请使用 --in-place 或换一个 -o")
        tmp_path = final_path

    # ---- 执行替换 ----
    try:
        replaced, processed, skipped = replace_in_epub(
            args.epub, tmp_path, mapping, do_verify=not args.no_verify)
        if args.in_place:
            # 恢复原文件的权限位，避免临时文件默认 0600 被带入
            os.chmod(tmp_path, os.stat(args.epub).st_mode)
            os.replace(tmp_path, final_path)
    except Exception as e:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        sys.exit(f"[错误] 处理失败：{e}")

    total_out = 0
    with zipfile.ZipFile(final_path, "r") as zf:
        for name in scan_text_entries(zf):
            t = decode_or_none(zf.read(name))
            if t:
                for dst in set(mapping.values()):
                    total_out += t.count(dst)
    if not args.quiet:
        print(f"\n[完成] 替换 {replaced} 个字符（{processed} 个条目，"
              f"{len(skipped)} 个条目因编码问题跳过）")
        print(f"[完成] 输出：{final_path}（目标引号共 {total_out} 个）")
    return 0


if __name__ == "__main__":
    sys.exit(main())