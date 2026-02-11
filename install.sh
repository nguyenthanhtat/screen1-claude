#!/bin/bash
# Quick installation script for Claude Code skills
# Usage: curl -s https://raw.githubusercontent.com/nguyenthanhtat/screen1-claude/main/install.sh | bash

set -e

echo "🚀 Installing Claude Code Skills..."
echo ""

# Clone repository
echo "📦 Cloning repository..."
if [ -d ~/claude-skills ]; then
    echo "⚠️  ~/claude-skills already exists. Updating..."
    cd ~/claude-skills
    git pull origin main
else
    git clone https://github.com/nguyenthanhtat/screen1-claude.git ~/claude-skills
fi

# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy skills
echo "📋 Installing BigQuery Skill Suite..."
cp -r ~/claude-skills/skills/bigquery ~/.claude/skills/

echo "📋 Installing Test-Fully Skill..."
cp -r ~/claude-skills/skills/test-fully ~/.claude/skills/

echo "📋 Installing Git Skill Suite..."
cp -r ~/claude-skills/skills/git ~/.claude/skills/

echo ""
echo "✅ Installation complete!"
echo ""
echo "📖 Test your installation:"
echo "   /bigquery"
echo "   /test-fully"
echo "   /git"
echo ""
echo "📚 Documentation: https://github.com/nguyenthanhtat/screen1-claude"
echo ""
