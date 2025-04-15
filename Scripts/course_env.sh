#!/usr/bin/env bash
shopt -s expand_aliases

for f in /etc/bashrc /etc/bash.bashrc ${HOME}/.bashrc; do
  if [ -f "$f" ]; then
    source "$f"
  fi
done

export COURSE_HOME="${COURSE_HOME:-$PWD}"
cd "$COURSE_HOME"

export PATH="$COURSE_HOME/Scripts:$COURSE_HOME/Code:$PATH"

function cdcourse() {
  echo "COURSE_HOME is: '$COURSE_HOME'"
  echo "Use the command 'cdcourse' anytime to return to this root."
  echo ""
  builtin cd "$COURSE_HOME"
  unset -f cdcourse  # only print once
  alias cdcourse='cd "$COURSE_HOME"'
}
alias cdcourse=cdcourse

cdcourse
