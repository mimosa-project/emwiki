#!/bin/bash

# Move to Working Directory
cd "$(dirname "$0")/../.."

# Main
npx eslint "emwiki/**/*.js"
