#!/bin/bash
# Clear Python cache and restart services

echo "Clearing Python cache..."
find /app -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find /app -name "*.pyc" -delete 2>/dev/null || true

echo "Cache cleared!"
