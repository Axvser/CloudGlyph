# Context Setup

## Responsibility

Confirm all necessary context

## Flow

1. Derive CloudGlyph_Child_Git from MainSKILL_Path

2. Project_Root must be provided by the user

3. LanguageTargets_List must be provided by the user, and must be a subset of LanguageMap_List; if not, inform the user that LanguageMap_List needs to be edited to support the specified languages

4. Discover the project's tech stack, such as .NET, C/C++, Python, JavaScript, etc.

5. Optionally accept a SKILL path from the user; if provided, load the corresponding SKILL

6. Present a summary table to the user; proceed with the workflow after user confirmation
