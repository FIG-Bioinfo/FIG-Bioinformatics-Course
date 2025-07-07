#!/usr/bin/env bash

# Detect platform
if [[ "$(uname -s)" == "Linux" || "$(uname -s)" == "Darwin" ]]; then
    export PATH="$COURSE_HOME/NCBI/sratoolkit/bin:$COURSE_HOME/NCBI/edirect:$PATH"
    ROOT_PATH="$COURSE_HOME/NCBI/public"
else
    export PATH="$(cygpath -w "$COURSE_HOME/NCBI/sratoolkit/bin"):$(cygpath -w "$COURSE_HOME/NCBI/edirect"):$PATH"
    ROOT_PATH="$(cygpath -w "$COURSE_HOME/NCBI/public")"
fi

# Force override and cleanup of legacy paths
vdb-config --set "/repository/user/main/public/root=$ROOT_PATH"
vdb-config --set "/repository/user/ad/public/root=$ROOT_PATH"
vdb-config --set "/repository/user/ad/public/apps/sra/volumes/sraAd=$ROOT_PATH"

# Optionally persist it
vdb-config --save

# Confirm result
echo "[INFO] vdb-config root set to:"
vdb-config -p | grep root
