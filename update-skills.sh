#!/usr/bin/env bash

# Office Skills Auto-Update Script
# Works on Windows (Git Bash/WSL), macOS, and Linux

SKILLS_DIR="$HOME/.config/opencode/skills/office"
REPO="anthropics/skills"
BRANCH="main"

echo "Updating office skills from $REPO..."

mkdir -p "$SKILLS_DIR"

# Download docx.md
echo "Downloading docx.md..."
curl -sL "https://raw.githubusercontent.com/$REPO/$BRANCH/skills/docx/SKILL.md" -o "$SKILLS_DIR/docx.md" && echo "  [OK] docx.md updated" || echo "  [FAIL] docx.md"

# Download pdf.md
echo "Downloading pdf.md..."
curl -sL "https://raw.githubusercontent.com/$REPO/$BRANCH/skills/pdf/SKILL.md" -o "$SKILLS_DIR/pdf.md" && echo "  [OK] pdf.md updated" || echo "  [FAIL] pdf.md"

# Download pdf_forms.md
echo "Downloading pdf_forms.md..."
curl -sL "https://raw.githubusercontent.com/$REPO/$BRANCH/skills/pdf/forms.md" -o "$SKILLS_DIR/pdf_forms.md" && echo "  [OK] pdf_forms.md updated" || echo "  [FAIL] pdf_forms.md"

# Download pdf_reference.md
echo "Downloading pdf_reference.md..."
curl -sL "https://raw.githubusercontent.com/$REPO/$BRANCH/skills/pdf/reference.md" -o "$SKILLS_DIR/pdf_reference.md" && echo "  [OK] pdf_reference.md updated" || echo "  [FAIL] pdf_reference.md"

# Download pptx.md
echo "Downloading pptx.md..."
curl -sL "https://raw.githubusercontent.com/$REPO/$BRANCH/skills/pptx/SKILL.md" -o "$SKILLS_DIR/pptx.md" && echo "  [OK] pptx.md updated" || echo "  [FAIL] pptx.md"

# Download pptx_editing.md
echo "Downloading pptx_editing.md..."
curl -sL "https://raw.githubusercontent.com/$REPO/$BRANCH/skills/pptx/editing.md" -o "$SKILLS_DIR/pptx_editing.md" && echo "  [OK] pptx_editing.md updated" || echo "  [FAIL] pptx_editing.md"

# Download pptx_pptxgenjs.md
echo "Downloading pptx_pptxgenjs.md..."
curl -sL "https://raw.githubusercontent.com/$REPO/$BRANCH/skills/pptx/pptxgenjs.md" -o "$SKILLS_DIR/pptx_pptxgenjs.md" && echo "  [OK] pptx_pptxgenjs.md updated" || echo "  [FAIL] pptx_pptxgenjs.md"

# Download xlsx.md
echo "Downloading xlsx.md..."
curl -sL "https://raw.githubusercontent.com/$REPO/$BRANCH/skills/xlsx/SKILL.md" -o "$SKILLS_DIR/xlsx.md" && echo "  [OK] xlsx.md updated" || echo "  [FAIL] xlsx.md"

echo "Update complete!"
