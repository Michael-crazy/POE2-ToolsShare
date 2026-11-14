"""Read-only structural and asset checks for local PoE2 loot filters."""

import argparse
from pathlib import Path
import re
import sys


TOKEN = re.compile(r'"[^"]*"|[^"\s#]+')
BLOCKS = {"show", "hide", "minimal"}
# Known commands are used for advisory diagnostics. The game evolves independently.
KNOWN = set("""
AlternateQuality AlwaysShow AnyEnchantment AreaLevel BaseArmour BaseDefencePercentile
BaseEnergyShield BaseEvasion BaseType Class Corrupted CorruptedMods
DisableDropSound DisableDropSoundIfAlertSound DropLevel EnableDropSound
EnableDropSoundIfAlertSound ExplicitMod FracturedItem GemLevel HasEaterOfWorldsImplicit
HasEnchantment HasExplicitMod HasImplicitMod HasInfluence HasSearingExarchImplicit
HasVaalUniqueMod Height Identified IsVaalUnique ItemLevel LinkedSockets MapTier
MinimapIcon PlayAlertSound PlayAlertSoundPositional PlayEffect Quality Rarity
Replica Scourged SetBackgroundColor SetBorderColor SetFontSize SetTextColor
SocketGroup Sockets StackSize SynthesisedItem TransfiguredGem TwiceCorrupted
UnidentifiedItemTier WaystoneTier Width
""".lower().split())


def tokens(line):
    """Read quoted paths literally and stop at the first unquoted comment."""
    line = line.lstrip()
    result = []
    while line and not line.startswith("#"):
        match = TOKEN.match(line)
        if not match:
            raise ValueError("unclosed quote")
        result.append(match.group())
        line = line[match.end():]
        line = line.lstrip()
    return result


def file_arg(args, usage):
    if not args or not args[0].startswith('"') or len(args[0]) <= 2:
        raise ValueError(usage)
    return args[0][1:-1].replace("\\", "/")


def inspect(path, sound_root, encoding, active, checked, stats):
    def report(number, severity, message):
        print(f"{path}:{number}: {severity}: {message}")
        stats[severity] += 1

    path = path.resolve()
    if path in checked:
        return
    try:
        lines = path.read_text(encoding=encoding).splitlines()
    except (OSError, UnicodeError, LookupError) as error:
        report(0, "error", str(error))
        return

    active.add(path)
    in_block = False
    has_block = False
    for number, line in enumerate(lines, 1):
        try:
            parts = tokens(line)
            if not parts:
                continue
            command, *args = parts
            command = command.lower()
            if command in BLOCKS:
                if args:
                    raise ValueError("block header takes no arguments")
                in_block = has_block = True
                stats["blocks"] += 1
            elif command == "import":
                in_block = False
                relative = file_arg(args, 'expected Import "file" [Optional]')
                optional = [arg.lower() for arg in args[1:]] == ["optional"]
                if len(args) > 1 and not optional:
                    raise ValueError('expected Import "file" [Optional]')
                target = (path.parent / relative).resolve()
                has_block = True
                if target in active:
                    raise ValueError(f"cyclic import: {relative}")
                if optional and not target.is_file():
                    report(number, "warning", f"optional import is absent: {relative}")
                else:
                    inspect(target, sound_root, encoding, active, checked, stats)
            elif not in_block:
                raise ValueError("command outside a Show, Hide, or Minimal block")
            elif command == "continue":
                if args:
                    raise ValueError("Continue takes no arguments")
            elif command in {"customalertsound", "customalertsoundoptional"}:
                relative = file_arg(args, 'expected a quoted sound path or "None"')
                if len(args) > 2 or (len(args) == 2 and not 0 <= int(args[1]) <= 300):
                    raise ValueError("volume must be an integer from 0 to 300")
                for sound in relative.split(";"):
                    if sound.lower() != "none" and not (sound_root / sound).is_file():
                        severity = "warning" if command.endswith("optional") else "error"
                        report(number, severity, f"missing sound: {sound}")
            elif command not in KNOWN:
                report(number, "warning", f"unrecognized command, verify with client: {command}")
            elif not args and command not in {
                "disabledropsound", "enabledropsound",
                "disabledropsoundifalertsound", "enabledropsoundifalertsound",
            }:
                raise ValueError(f"{command} requires arguments")
            if command == "hasexplicitmod":
                names = [arg for arg in args if arg.startswith('"')]
                if len(names) != len(set(names)):
                    report(number, "warning", "repeated modifier names, verify match count")
        except (ValueError, OSError) as error:
            report(number, "error", str(error))
    if not has_block:
        report(0, "error", "no filter blocks or imports")
    active.remove(path)
    checked.add(path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sound-root", type=Path, help="game filter directory or equivalent")
    parser.add_argument("--encoding", default="utf-8-sig")
    parser.add_argument("filters", nargs="+", type=Path)
    args = parser.parse_args()
    failed = False
    for path in args.filters:
        stats = {"error": 0, "warning": 0, "blocks": 0}
        inspect(path, args.sound_root or path.parent, args.encoding, set(), set(), stats)
        print(f"{path}: {stats['blocks']} blocks, {stats['error']} errors, "
              f"{stats['warning']} warnings")
        failed |= stats["error"] > 0
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
