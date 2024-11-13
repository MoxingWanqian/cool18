#!/bin/sh

script_path=$(realpath "$0")
script_dir=$(dirname "$script_path")

new_content="alias cool18='bash $script_path'"

if ! grep -qF -- "$new_content" ~/.bashrc; then
    echo "

# COOL18
$new_content" >> ~/.bashrc
    source ~/.bashrc
    echo "Command '$command' is available."
fi

python3 "$script_dir/start.py"