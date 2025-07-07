#!/usr/bin/env bash

# === 0. Check if running inside Bash ===
if [ -z "$BASH_VERSION" ]; then
  echo "Error: This script requires Bash. Exiting." >&2
  exit 1
fi

# === 1. Try enabling alias expansion if possible ===
if command -v shopt >/dev/null 2>&1; then
  shopt -s expand_aliases
else
  echo "Warning: 'shopt' command not available. Alias support may not work fully." >&2
fi

# === 2. Source common bash configuration files ===
for f in /etc/bashrc /etc/bash.bashrc "${HOME}/.bashrc"; do
  if [ -f "$f" ]; then
    source "$f"
  fi
done

# === 3. Determine COURSE_HOME safely ===
# Fall back to 'pwd' command if $PWD is unset
if [ -z "$PWD" ]; then
  if command -v pwd >/dev/null 2>&1; then
    PWD="$(pwd)"
    echo "Info: \$PWD was unset. Recovered current directory: '$PWD'" >&2
  else
    echo "Error: Cannot determine working directory. Aborting." >&2
    exit 1
  fi
fi

export COURSE_HOME="${COURSE_HOME:-$PWD}"

# === 4. Move into COURSE_HOME ===
if ! cd "$COURSE_HOME"; then
  echo "Error: Failed to cd into '$COURSE_HOME'. Exiting." >&2
  exit 1
fi

# === 5. Extend PATH for Scripts and Code ===
export PATH="$COURSE_HOME/Scripts:$COURSE_HOME/Code:$PATH"

# === 6. Setup NCBI tools and SRA config ===
export NCBI_HOME="$COURSE_HOME/NCBI"
SRATOOLS_DIR="$NCBI_HOME/sratoolkit"

if [ -d "$SRATOOLS_DIR" ]; then
  # Extend PATH with sratoolkit and edirect
  if [[ "$(uname -s)" == "Linux" || "$(uname -s)" == "Darwin" ]]; then
    export PATH="$NCBI_HOME/sratoolkit/bin:$NCBI_HOME/edirect:$PATH"
    ROOT_PATH="$NCBI_HOME/public"
  else
    export PATH="$(cygpath -w "$NCBI_HOME/sratoolkit/bin"):$(cygpath -w "$NCBI_HOME/edirect"):$PATH"
    ROOT_PATH="$(cygpath -w "$NCBI_HOME/public")"
  fi

  # Force override and cleanup of legacy paths
  vdb-config --set "/repository/user/main/public/root=$ROOT_PATH"
  vdb-config --set "/repository/user/ad/public/root=$ROOT_PATH"
  vdb-config --set "/repository/user/ad/public/apps/sra/volumes/sraAd=$ROOT_PATH"

  # Persist config
  vdb-config --save

  # Confirm result
  echo "[INFO] vdb-config root set to:"
  vdb-config -p | grep root

  # Validate config
  if ! grep -q "$ROOT_PATH" <(vdb-config -p); then
    echo "[WARNING] vdb-config root appears misconfigured. Resetting..." >&2
    vdb-config --set "/repository/user/main/public/root=$ROOT_PATH"
  fi
else
  echo "SRA Toolkit is not yet installed --- please execute \"python Scripts/install_sra_toolkit.py\"" >&2
fi

# === 7. Setup 'cdcourse' command ===
function cdcourse() {
  echo "COURSE_HOME is: '$COURSE_HOME'"
  echo "Use 'cdcourse' anytime to return to this root."
  echo ""
  if ! builtin cd "$COURSE_HOME"; then
    echo "Error: Could not cd into COURSE_HOME during cdcourse()." >&2
    return 1
  fi
  unset -f cdcourse  # Only print once
  alias cdcourse='cd "$COURSE_HOME"'
}
alias cdcourse=cdcourse

# === 8. Automatically teleport user to course root ===
cdcourse
