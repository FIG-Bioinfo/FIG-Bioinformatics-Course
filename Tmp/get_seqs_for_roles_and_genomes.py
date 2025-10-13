#!/usr/bin/env python3
import argparse
import subprocess
import sys
import csv
from io import StringIO

def run_command(command, input_data=None):
    """Run shell command with optional STDIN, returning stdout, stderr, and code."""
    try:
        result = subprocess.run(
            command,
            input=input_data,
            capture_output=True,
            text=True,
            shell=True,
            check=False
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        print(f"Error running command: {command}\n{str(e)}", file=sys.stderr)
        sys.exit(1)


def parse_role_list(role_file):
    """Extract roles from TSV file based on 'role_name' column."""
    roles = []
    with open(role_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if "role_name" not in reader.fieldnames:
            print(f"Error: role_name column not found in {role_file}", file=sys.stderr)
            sys.exit(1)
        for row in reader:
            role = row.get("role_name", "").strip()
            if role:
                roles.append(role)
    if not roles:
        print(f"Error: No roles found in {role_file}", file=sys.stderr)
        sys.exit(1)
    return roles


def filter_cmd1_output(output, role):
    """Filter cmd1 TSV output so only exact matches for feature.product == role remain."""
    lines = output.strip().splitlines()
    if not lines:
        return ""

    header = lines[0]
    filtered_lines = [header]
    reader = csv.reader(StringIO(output), delimiter="\t")
    header_fields = next(reader)

    try:
        product_idx = header_fields.index("feature.product")
    except ValueError:
        print("Error: 'feature.product' column not found in cmd1 output", file=sys.stderr)
        sys.exit(1)

    for row in reader:
        if len(row) > product_idx and row[product_idx].strip() == role:
            filtered_lines.append("\t".join(row))
    return "\n".join(filtered_lines) + "\n" if len(filtered_lines) > 1 else ""


def main():
    parser = argparse.ArgumentParser(description="Get sequences for roles and genomes.")
    parser.add_argument("-T", "--type", choices=["dna", "protein"], required=True, help="Sequence type: dna or protein")
    parser.add_argument("-G", "--genome-list", required=True, help="TSV file containing genome IDs")
    parser.add_argument("-R", "--role-list", required=True, help="TSV file containing roles")
    args = parser.parse_args()

    genome_file = args.genome_list
    role_file = args.role_list
    seq_type = args.type

    roles = parse_role_list(role_file)
    total_roles = len(roles)
    total_sequences = 0

    for idx, role in enumerate(roles, 1):
        print(f"[{idx}/{total_roles}] Processing role: {role}", file=sys.stderr)
        quoted_role = role.replace("'", "\\'")
        cmd1 = f"p3-get-genome-features --selective --input {genome_file} --col genome_id --eq product,'{quoted_role}' --attr patric_id,product"
        cmd2 = f"p3-get-feature-sequence --col feature.patric_id --{seq_type}"

        out1, err1, code1 = run_command(cmd1)
        if code1 != 0:
            print(f"Error running cmd1 for role '{role}':\n{err1}", file=sys.stderr)
            sys.exit(1)

        filtered = filter_cmd1_output(out1, role)
        if not filtered:
            print(f"No exact matches for role '{role}'", file=sys.stderr)
            continue

        out2, err2, code2 = run_command(cmd2, input_data=filtered)
        if code2 != 0:
            print(f"Error running cmd2 for role '{role}':\n{err2}", file=sys.stderr)
            sys.exit(1)

        sequences = [line for line in out2.splitlines() if line.startswith(">")]
        total_sequences += len(sequences)

        # Pass FASTA sequences directly to STDOUT
        sys.stdout.write(out2)
        sys.stdout.flush()

        # Forward STDERR
        if err1:
            sys.stderr.write(err1)
        if err2:
            sys.stderr.write(err2)

    print(f"\nProcessed {total_roles} roles.", file=sys.stderr)
    print(f"Total sequences retrieved: {total_sequences}", file=sys.stderr)


if __name__ == "__main__":
    main()
