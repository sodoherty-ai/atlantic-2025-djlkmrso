#!/bin/bash
CURRENT_DIR="$(pwd)"
PARENT_DIR="$(dirname "$CURRENT_DIR")"
PYTHONPATH="$PARENT_DIR:$CURRENT_DIR:$PYTHONPATH" uvicorn example:app --reload
