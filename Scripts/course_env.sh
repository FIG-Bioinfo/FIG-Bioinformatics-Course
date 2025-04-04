#!/usr/bin/env bash
shopt -s expand_aliases

if [ -f ~/.bashrc ]; then
  source ~/.bashrc
fi

export COURSE_HOME="${COURSE_HOME:-$PWD}"
cd "$COURSE_HOME"

cdcourse() {
  echo "✅ COURSE_HOME is: $COURSE_HOME"
  echo "🔁 Use 'cdcourse' anytime to return to this root."
  builtin cd "$COURSE_HOME"
  unset -f cdcourse  # only print once
  alias cdcourse='cd "$COURSE_HOME"'
}
alias cdcourse=cdcourse
