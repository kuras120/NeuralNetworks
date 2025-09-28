#!/bin/bash

# Get the current version
VERSION=$1

# Start multiline environment variable
echo "CHANGELOG<<EOF" >> $GITHUB_ENV

# Read changelog from file
if [ -f "games_theory/changelog" ]; then
  # Extract exactly the section for this version:
  # - start printing at the exact header line for $VERSION
  # - stop at the next header that starts with the same prefix
  VERSION_SECTION=$(awk -v ver="## What's Changed in $VERSION" -v prefix="## What's Changed in " '
    $0 == ver { printing=1; print; next }
    printing && index($0, prefix) == 1 { exit }
    printing { print }
  ' games_theory/changelog)

  if [ -n "$VERSION_SECTION" ]; then
    echo "$VERSION_SECTION" >> $GITHUB_ENV
  else
    # If no section for current version, show "No changelog available" message
    echo "## What's Changed in $VERSION" >> $GITHUB_ENV
    echo "* No changelog available for this release" >> $GITHUB_ENV
  fi
else
  # Fallback if changelog file doesn't exist
  echo "## What's Changed in $VERSION" >> $GITHUB_ENV
  echo "* No changelog file available" >> $GITHUB_ENV
fi

# End multiline environment variable (no extra blank line)
echo "EOF" >> $GITHUB_ENV