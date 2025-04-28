#!/usr/bin/env bash

if [[ "$(uname -s)" == "Linux" || "$(uname -s)" == "Darwin" ]]; then
    export PATH="$COURSE_HOME/NCBI/sratoolkit/bin:$COURSE_HOME/NCBI/edirect:$PATH"
    vdb-config --set "/repository/user/main/public/root=$COURSE_HOME/NCBI/public"
else
    export PATH="$(cygpath -w "$COURSE_HOME/NCBI/sratoolkit/bin"):$(cygpath -w "$COURSE_HOME/NCBI/edirect"):$PATH"
    vdb-config --set "/repository/user/main/public/root=$(cygpath -w "$COURSE_HOME/NCBI/public")"
fi
