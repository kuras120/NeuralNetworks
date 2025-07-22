#!/bin/bash

# Get the current version
VERSION=$(python games_theory/version_bump.py version)
echo "Current version: $VERSION"

# Set up environment variable for testing
export GITHUB_ENV="test_env.txt"
echo "" > $GITHUB_ENV

# Run the generate_changelog.sh script
./games_theory/generate_changelog.sh $VERSION

# Display the result
echo -e "\nTest completed. Environment file content:"
cat $GITHUB_ENV

# Clean up
rm $GITHUB_ENV