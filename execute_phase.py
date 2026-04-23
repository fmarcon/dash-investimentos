#!/usr/bin/env python3
"""Esqueleto de execução de fase para o projeto Dashboard de Investimentos.

Este script lê planos disponíveis em .planning/phases e executa uma versão
minimalista do fluxo de execução de fase, com suporte a:
- --wave N
- --gaps-only
- --interactive

A execução de fato não altera o código do projeto, mas cria um arquivo de
sumário em .planning/phases/<phase>/<plan>-SUMMARY.md com as decisões tomadas.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Optional, Tuple


def parse_value(raw_value: str) -> Any:
    if raw_value.startswith('"') and raw_value.endswith('"'):
        return raw_value[1:-1]
    if raw_value.startswith("'") and raw_value.endswith("'"):
        return raw_value[1:-1]
    if raw_value.lower() == "true":
        return True
    if raw_value.lower() == "false":
        return False
    if raw_value.isdigit():
        return int(raw_value)
    try:
        return float(raw_value)
    except ValueError:
        return raw_value


def parse_frontmatter(text: str) -> Mapping[str, Any]:
    match = re.search(r"^---\s*$([\s\S]*?)^---\s*$", text, re.MULTILINE)
    if not match:
        return {}

    raw = match.group(1)
    lines = raw.splitlines()
    result: Dict[str, Any] = {}
    stack: List[Tuple[int, Any, Optional[str]]] = [(0, result, None)]

    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        while stack and indent < stack[-1][0]:
            stack.pop()

        if not stack:
            stack = [(0, result, None)]

        current_indent, current_container, last_key = stack[-1]

        if stripped.startswith("- "):
            item_value = stripped[2:]
            if isinstance(current_container, dict):
                if last_key is None:
                    continue
                if not isinstance(current_container.get(last_key), list):
                    current_container[last_key] = []
                target_list = current_container[last_key]
            elif isinstance(current_container, list):
                target_list = current_container
            else:
                continue

            if ": " in item_value and not item_value.endswith(":"):
                key, _, raw_val = item_value.partition(":")
                target_list.append({key.strip(): parse_value(raw_val.strip())})
            else:
                target_list.append(parse_value(item_value))
            continue

        if ":" in stripped:
            key, _, raw_val = stripped.partition(":")
            key = key.strip()
            raw_val = raw_val.strip()
            if raw_val == "":
                new_item: Dict[str, Any] = {}
                if isinstance(current_container, dict):
                    current_container[key] = new_item
                    stack.append((indent + 2, new_item, key))
                continue
            if isinstance(current_container, dict):
                current_container[key] = parse_value(raw_val)
                stack[-1] = (current_indent, current_container, key)
            continue

    return result


def parse_tasks(text: str) -> List[str]:
    tasks: List[str] = []
    for task_header in re.findall(r"<task[^>]*>\s*([\s\S]*?)</task>", text):
        title_match = re.search(r"<name>\s*(.+?)\s*</name>", task_header)
        if title_match:
            tasks.append(title_match.group(1).strip())
    return tasks


def find_phase_dir(base: Path, phase_identifier: str) -> Optional[Path]:
    phases_dir = base / ".planning" / "phases"
    if not phases_dir.exists():
        return None

    if phase_identifier.isdigit():
        candidate = sorted(phases_dir.iterdir())
        index = int(phase_identifier) - 1
        if 0 <= index < len(candidate):
            return candidate[index]

    for candidate in phases_dir.iterdir():
        if candidate.name.startswith(phase_identifier) or phase_identifier in candidate.name:
            return candidate
    return None


def load_plans(phase_dir: Path) -> List[Tuple[Path, Mapping[str, Any], List[str]]]:
    plans: List[Tuple[Path, Mapping[str, Any], List[str]]] = []
    for plan_file in sorted(phase_dir.glob("*-PLAN.md")):
        content = plan_file.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)
        tasks = parse_tasks(content)
        plans.append((plan_file, frontmatter, tasks))
    return plans


def select_plans(
    plans: Iterable[Tuple[Path, Mapping[str, Any], List[str]]],
    wave: Optional[int],
    gaps_only: bool,
) -> List[Tuple[Path, Mapping[str, Any], List[str]]]:
    selected = []
    for plan_file, frontmatter, tasks in plans:
        if gaps_only and not frontmatter.get("gap_closure", False):
            continue
        plan_wave = frontmatter.get("wave")
        if wave is not None and plan_wave is not None and int(plan_wave) != wave:
            continue
        selected.append((plan_file, frontmatter, tasks))
    return selected


def summarize_execution(
    phase_name: str,
    selected_plans: List[Tuple[Path, Mapping[str, Any], List[str]]],
    wave: Optional[int],
    gaps_only: bool,
    interactive: bool,
) -> str:
    header_lines = [
        f"# Sumário de execução da fase {phase_name}",
        "",
        f"- data: {datetime.datetime.utcnow().isoformat()}Z",
        f"- wave: {wave if wave is not None else 'todas'}",
        f"- gaps_only: {gaps_only}",
        f"- interactive: {interactive}",
        "",
    ]

    if not selected_plans:
        header_lines.append("Nenhum plano selecionado para execução com os filtros informados.")
        return "\n".join(header_lines)

    for plan_file, frontmatter, tasks in selected_plans:
        header_lines.append(f"## Plano: {plan_file.name}")
        header_lines.append(f"- tipo: {frontmatter.get('type', 'desconhecido')}")
        header_lines.append(f"- wave: {frontmatter.get('wave', 'não definido')}")
        header_lines.append(f"- gap_closure: {frontmatter.get('gap_closure', False)}")
        header_lines.append(f"- arquivos afetados: {frontmatter.get('files_modified', [])}")
        header_lines.append("- tarefas:")
        if tasks:
            for task in tasks:
                header_lines.append(f"  - {task}")
        else:
            header_lines.append("  - Nenhuma tarefa encontrada no corpo do plano.")
        header_lines.append("")

    header_lines.append("---")
    header_lines.append("Este é um esqueleto de execução de fase. A implementação real deve ser adicionada nos arquivos do projeto, como backend/ e frontend/." )
    return "\n".join(header_lines)


def write_summary(phase_dir: Path, summary: str) -> Path:
    summary_path = phase_dir / "01-01-SUMMARY.md"
    summary_path.write_text(summary, encoding="utf-8")
    return summary_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Executor de fase esquelético para .planning/phases.",
    )
    parser.add_argument(
        "phase",
        help="Número ou identificador da fase (ex: 1 ou 01-mvp-de-operacoes-e-dashboard).",
    )
    parser.add_argument("--wave", type=int, help="Executa somente a wave informada.")
    parser.add_argument("--gaps-only", action="store_true", help="Executa apenas planos marcados como gap_closure.")
    parser.add_argument("--interactive", action="store_true", help="Executa em modo interativo de checkpoint.")

    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    phase_dir = find_phase_dir(base, args.phase)
    if phase_dir is None:
        print("Fase não encontrada em .planning/phases.")
        return 1

    plans = load_plans(phase_dir)
    if not plans:
        print("Nenhum plano encontrado na fase selecionada.")
        return 1

    selected_plans = select_plans(plans, args.wave, args.gaps_only)
    if not selected_plans:
        print("Nenhum plano corresponde aos filtros informados.")
        return 0

    print(f"Fase encontrada: {phase_dir.name}")
    print(f"Planos selecionados: {[plan_file.name for plan_file, _, _ in selected_plans]}")
    if args.interactive:
        for plan_file, frontmatter, tasks in selected_plans:
            print(f"\n>> Plano: {plan_file.name}")
            print(f"Tipo: {frontmatter.get('type', 'desconhecido')}")
            print(f"Wave: {frontmatter.get('wave', 'não definido')}")
            print("Tarefas:")
            for task in tasks:
                print(f"  - {task}")
            input("Pressione Enter para marcar este plano como verificado e continuar...")

    summary = summarize_execution(
        phase_name=phase_dir.name,
        selected_plans=selected_plans,
        wave=args.wave,
        gaps_only=args.gaps_only,
        interactive=args.interactive,
    )
    summary_path = write_summary(phase_dir, summary)
    print(f"Sumário de execução gerado em: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
