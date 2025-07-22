#!/bin/bash

# Get the current version
VERSION=$1

# Start multiline environment variable
echo "CHANGELOG<<EOF" >> $GITHUB_ENV

# Read changelog from file
if [ -f "games_theory/changelog" ]; then
  # Extract the section for the current version
  VERSION_SECTION=$(awk -v ver="## What's Changed in $VERSION" 'BEGIN{flag=0} $0 ~ ver {flag=1; print; next} /^## [0-9]+\.[0-9]+\.[0-9]+/ {flag=0} flag {print}' games_theory/changelog)
  
  # If version section found, use it
  if [ -n "$VERSION_SECTION" ]; then
    echo "$VERSION_SECTION" >> $GITHUB_ENV
  else
    # If no section for current version, show "No changelog available" message
    echo "## What's Changed in $VERSION" >> $GITHUB_ENV
    echo "" >> $GITHUB_ENV
    echo "* No changelog available for this release" >> $GITHUB_ENV
  fi
else
  # Fallback if changelog file doesn't exist
  echo "## What's Changed in $VERSION" >> $GITHUB_ENV
  echo "" >> $GITHUB_ENV
  echo "* No changelog available for this release" >> $GITHUB_ENV
fi

# End multiline environment variable
echo "" >> $GITHUB_ENV
echo "EOF" >> $GITHUB_ENV