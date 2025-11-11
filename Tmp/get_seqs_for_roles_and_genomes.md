# 🧬 `get_seqs_for_roles_and_genomes.py`

## 📘 Objective

Develop a **Python 3 command-line tool** named `get_seqs_for_roles_and_genomes.py` that retrieves **DNA** or **protein** sequences for specific biological roles across a set of genomes, using BV-BRC command-line utilities.

---

## 🧱 Functional Requirements

### 1. Command-Line Arguments

Use `argparse` to define the following **mandatory named arguments**:

| Short Flag | Long Flag       | Type      | Allowed Values   | Description                                                |
| ---------- | --------------- | --------- | ---------------- | ---------------------------------------------------------- |
| `-T`       | `--type`        | String    | `dna`, `protein` | Type of sequence to retrieve                               |
| `-G`       | `--genome-list` | File path | —                | TSV file containing genome IDs (with header)               |
| `-R`       | `--role-list`   | File path | —                | TSV file containing role names (with a `role_name` column) |

* If any argument is missing or invalid, print a descriptive usage error and exit with code **2**.

---

### 2. Environment Verification

Before proceeding, verify that the **BV-BRC CLI** environment is active by checking for the `p3-login` executable.

#### Expected Behavior

* Use:

  ```python
  shutil.which("p3-login")
  ```
* If not found, print this error message to `STDERR`:

  ```
  Error: 'p3-login' not found.
  Please run this script inside the BV-BRC.app environment and login first using:
      p3-login <your_email>
  ```
* Exit with status **1**.

---

### 3. Role List Parsing

Parse the `--role-list` TSV file as follows:

* Detect and use the `` column from the header.
* Extract all non-empty role values into a list.
* If the column is missing or the list is empty:

  * Print an error to `STDERR`.
  * Exit with status **1**.

---

### 4. Genome Feature Retrieval & Sequence Extraction

For each role in the parsed role list:

1. **Log progress** to `STDERR`:

   ```
   [N/M] Processing role: <role_name>
   ```

2. **Run the following commands sequentially**:

   ```python
   cmd1 = (
       f"p3-get-genome-features "
       f"--selective --input {genomes_filename} "
       f"--col genome_id --eq product,'{role}' "
       f"--attr patric_id,product"
   )

   cmd2 = f"p3-get-feature-sequence --col feature.patric_id --{type}"
   ```

   * Note: `role` values may include whitespace — ensure proper quoting.

3. **Error Handling**

   * If either command exits non-zero, print its error output to `STDERR` and exit with status **1**.

---

### 5. Output Filtering Logic

The STDOUT from `cmd1` must be filtered before passing it to `cmd2`.

#### Filtering Rules

* Keep the **header line** unchanged.
* Identify the column named `feature.product`.
* For each subsequent line:

  * Compare the `feature.product` value with the current `role`.
  * Include the line **only if the match is exact**.
  * Discard all non-exact matches.

The filtered data becomes the **STDIN** for `cmd2`.

---

### 6. Output Handling

* `cmd2` produces **FASTA-formatted** sequences as STDOUT.
* Behavior:

  * Forward the FASTA output directly to this program’s STDOUT.
  * Count the number of FASTA entries (lines starting with `>`).
  * Forward all STDERR output from both commands to this program’s STDERR.

---

### 7. Final Summary Report

After processing all roles, print a summary to `STDERR`:

```
Summary:
  Roles processed: <count_roles>
  Genomes processed: <count_genomes>
  FASTA sequences returned: <count_sequences>
```

Exit with status **0**.

---

## ⚙️ Implementation Guidelines

* Use `subprocess.run()` with `capture_output=True` and `text=True`.
* Handle all I/O in **UTF-8** encoding.
* Quote arguments safely when building command strings.
* Conform to **PEP 8**.
* Include a **Unix shebang** (`#!/usr/bin/env python3`).
* Exit cleanly on all error conditions with descriptive messages.

---

## 🤪 Example Usage

```bash
python3 get_seqs_for_roles_and_genomes.py \
  --type protein \
  --genome-list genomes.tsv \
  --role-list roles.tsv \
  > sequences.faa
```

### Expected Behavior

* Logs progress to STDERR.
* Outputs FASTA-formatted sequences to STDOUT.
* Prints a summary report at the end.
