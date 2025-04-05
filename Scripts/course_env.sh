#!/usr/bin/env bash
shopt -s expand_aliases

export COURSE_HOME="${COURSE_HOME:-$PWD}"
cd "$COURSE_HOME"

# Create the cdcourse function.
cdcourse() {
  echo "COURSE_HOME is: $COURSE_HOME"
  echo "Use 'cdcourse' anytime to return to this root."
  echo ""
  builtin cd "$COURSE_HOME"
  unset -f cdcourse  # only print once
  alias cdcourse='cd "$COURSE_HOME"'
}

# This allows a student to return to the root of the course
# just by executing the command 'cdcourse' at the command line.
alias cdcourse=cdcourse

cdcourse