#!/usr/bin/env python3
import argparse
import subprocess
import sys
import csv
import shutil
from io import StringIO


def ensure_p3_login():
    """Ensure that 'p3-login' command is available."""
    if shutil.which("p3-login") is None:
        print(
            "Error: 'p3-login' command not found.\n"
            "You must run this script inside the BV-BRC.app environment.\n"
            "Please login first using: p3-login <your_email>",
            file=sys.stderr,
        )
        sys.exit(1)


def parse_role_list(role_file):
    """Extract roles from TSV file based on 'role_name' column."""
    roles = []
    with open(role_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if "role_name" not in reader.fieldnames:
            print(f"Error: 'role_name' column not found in {role_file}", file=sys.stderr)
            sys.exit(1)
        for row in reader:
            role = row.get("role_name", "").strip()
            if role:
                roles.append(role)
    if not roles:
        print(f"Error: No roles found in {role_file}", file=sys.stderr)
        sys.exit(1)
    return roles


def run_command(cmd, input_data=None):
    """Run shell command safely with optional STDIN, return (stdout, stderr, code)."""
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            text=True,
            capture_output=True,
            shell=True,
            check=False,
        )
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        print(f"Command execution error for '{cmd}': {e}", file=sys.stderr)
        sys.exit(1)


def filter_cmd1_output(output, role):
    """Filter cmd1 TSV output keeping only exact matches for feature.product == role."""
    lines = output.strip().splitlines()
    if not lines:
        return ""

    header = lines[0]
    reader = csv.reader(StringIO(output), delimiter="\t")
    header_fields = next(reader)

    try:
        product_idx = header_fields.index("feature.product")
    except ValueError:
        print("Error: Missing 'feature.product' column in cmd1 output.", file=sys.stderr)
        sys.exit(1)

    filtered_lines = [header]
    for row in reader:
        if len(row) > product_idx and row[product_idx].strip() == role:
            filtered_lines.append("\t".join(row))
    return "\n".join(filtered_lines) + "\n" if len(filtered_lines) > 1 else ""


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve sequences for roles and genomes via PATRIC CLI."
    )
    parser.add_argument(
        "-T", "--type", choices=["dna", "protein"], required=True, help="Sequence type"
    )
    parser.add_argument(
        "-G", "--genome-list", required=True, help="TSV file containing genome IDs"
    )
    parser.add_argument(
        "-R", "--role-list", required=True, help="TSV file containing roles"
    )
    args = parser.parse_args()

    # Step 2: Check environment
    ensure_p3_login()

    seq_type = args.type
    genomes_file = args.genome_list
    roles_file = args.role_list

    roles = parse_role_list(roles_file)
    total_roles = len(roles)
    total_sequences = 0
    total_genomes = 0

    for idx, role in enumerate(roles, 1):
        print(f"[{idx}/{total_roles}] Processing role: {role}", file=sys.stderr)
        quoted_role = role.replace("'", "\\'")
        cmd1 = (
            f"p3-get-genome-features --selective --input {genomes_file} "
            f"--col genome_id --eq product,'{quoted_role}' --attr patric_id,product"
        )
        cmd2 = f"p3-get-feature-sequence --col feature.patric_id --{seq_type}"

        # Run cmd1
        out1, err1, code1 = run_command(cmd1)
        if code1 != 0:
            print(f"Error: cmd1 failed for role '{role}'\n{err1}", file=sys.stderr)
            sys.exit(1)

        # Filter results
        filtered = filter_cmd1_output(out1, role)
        if not filtered.strip():
            print(f"No exact matches for role '{role}'", file=sys.stderr)
            continue

        # Count unique genomes matched
        genome_reader = csv.DictReader(StringIO(filtered), delimiter="\t")
        genome_ids = {row["feature.patric_id"] for row in genome_reader if "feature.patric_id" in row}
        total_genomes += len(genome_ids)

        # Run cmd2 with filtered input
        out2, err2, code2 = run_command(cmd2, input_data=filtered)
        if code2 != 0:
            print(f"Error: cmd2 failed for role '{role}'\n{err2}", file=sys.stderr)
            sys.exit(1)

        seq_count = sum(1 for line in out2.splitlines() if line.startswith(">"))
        total_sequences += seq_count

        sys.stdout.write(out2)
        sys.stdout.flush()

        if err1:
            sys.stderr.write(err1)
        if err2:
            sys.stderr.write(err2)

    print(f"\nSummary:", file=sys.stderr)
    print(f"  Roles processed: {total_roles}", file=sys.stderr)
    print(f"  Genomes processed: {total_genomes}", file=sys.stderr)
    print(f"  FASTA sequences returned: {total_sequences}", file=sys.stderr)


if __name__ == "__main__":
    main()
