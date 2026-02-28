import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

os.makedirs("output", exist_ok=True)
file_path = "output/ECOIN_Core_Proposal_L2.pdf"

doc = SimpleDocTemplate(file_path)
styles = getSampleStyleSheet()
story = []

content = [
    ("ECOIN: A Cognitive Operating System for Post-Nation Civilization", True),
    ("Not a currency. Not a nation. A cognitive operating system.", False),
    ("ECOIN is designed to support human coordination in a post-nation world.", False),
    ("It restores natural human cooperation without coercion.", False),
    ("Problem Statement", True),
    ("Existing nation-state systems rely on borders, force, and scarcity.", False),
    ("These systems are outdated for a highly connected world.", False),
    ("Core Concept", True),
    ("ECOIN is a Cognitive Operating System (COS).", False),
    ("It manages observation, translation, resonance, and circulation.", False),
    ("Architecture", True),
    ("Layer 1: Cognitive Layer", False),
    ("Layer 2: Translation Layer", False),
    ("Layer 3: Circulation Layer", False),
    ("Layer 4: Interface Layer", False),
    ("Human-AI Co-Cognition", True),
    ("AI assists translation; humans retain responsibility.", False),
    ("Conclusion", True),
    ("ECOIN is not a revolution, but a remembering device.", False),
]

for text, is_title in content:
    style = styles["Title"] if is_title else styles["BodyText"]
    story.append(Paragraph(text, style))
    story.append(Spacer(1, 12))

doc.build(story)

file_path
