#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from pathlib import Path
from typing import List


MODULE_BLOCK: str = f"        <module>core</module>\n"
DEPENDENCY_BLOCK: str = """
        <dependency>
            <groupId>net.runelite</groupId>
            <artifactId>Core</artifactId>
            <version>{version}</version>
            <scope>compile</scope>
        </dependency>
"""


@dataclass(frozen=True)
class ProgramArgs:
    version: str
    parent: Path
    client: Path


def get_program_args() -> ProgramArgs:
    parser: ArgumentParser = ArgumentParser(description="Script that inserts core dependency into pom files")
    parser.add_argument("--version", type=str, required=True, help="Runelite package version")
    parser.add_argument("--parent", type=Path, required=True, help="Path to parent pom.xml")
    parser.add_argument("--client", type=Path, required=True, help="Path to client pom.xml")

    args: Namespace = parser.parse_args()
    return ProgramArgs(**vars(args))


def add_dependency(pom_path: Path, version: str) -> None:
    with open(pom_path, "r", encoding="utf-8") as f:
        lines: List[str] = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() == "<dependencies>":
            lines.insert(i + 1, DEPENDENCY_BLOCK.format(version=version))
            break

    with open(pom_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print("Dependency 'net.runelite:Core' added successfully.")


def add_module(pom_path: Path) -> None:
    with open(pom_path, "r", encoding="utf-8") as f:
        lines: List[str] = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() == "<modules>":
            lines.insert(i + 1, MODULE_BLOCK)
            break

    with open(pom_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Module 'core' added successfully.")


def main():
    args: ProgramArgs = get_program_args()

    add_dependency(pom_path=args.client, version=args.version)
    add_module(pom_path=args.parent)


if __name__ == "__main__":
    main()
