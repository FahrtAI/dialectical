# Install and test Dialectical in ChatGPT

Dialectical 0.4.0 is a skills-only plugin. Its entry point is
`skills/dialectical/SKILL.md`, and its display name is **Dialectical**.
The package requires no server, OAuth, API key, developer mode, or app connection.

## Install or update the account plugin

Use an account installation for both desktop and iPhone. A ZIP on your Mac,
a Git push, or an installation from a local marketplace does not establish
availability on your phone.

1. Open ChatGPT on the web in the intended account/workspace.
2. Open **Plugins** and find the existing **Dialectical** plugin under
   **Personal / Created by me** (or the workspace where it was created).
3. Select **Edit Plugin**. Attach `dist/dialectical-0.4.0.zip` and send:

   > Replace Dialectical's package with this skills-only version 0.4.0.
   > Preserve its name and ownership. Remove the old MCP/app dependency.
   > Use the supplied skill and reference files, including the startup
   > instructions for “@Dialectical start a conversation.”

4. Review the proposed update and complete the save/update prompts. Confirm
   that the plugin lists the supplied skills and no required Apps/MCP connection.
5. Select the plus/install button if it is not installed, then start a new chat.
   An already open chat may still have the old version.

If there is no existing editable account plugin, select **Plugin Creator** from
the `@` menu, attach the ZIP, and ask it to create a private skills-only plugin
named Dialectical using the package exactly. Review and finish creation, then
install it. If editing or importing the existing plugin is unsupported for its
source, use the source-specific update flow shown by ChatGPT; do not create
duplicate plugins just to work around a missing control.

Plugin Creator and plugin use must be available to your account/workspace.
If these controls are absent, check the workspace and its permissions. A local
package cannot enable a feature the account lacks.

## Desktop acceptance test

1. Open a new ChatGPT desktop chat after installation.
2. Type `@`, search for **Dialectical**, and select the entry under **Plugins**.
   Select the actual mention; plain typed text alone does not prove invocation.
3. Send `@Dialectical start a conversation`.
4. Expect one short question asking which idea, question, or decision to explore.
   There must be no server connection, login, file initialization, or setup step.
5. Reply: “I think remote work slows mentoring because juniors cannot overhear
   seniors.” Expect clarification and qualified exploration, not automatic
   acceptance of the explanation.
6. Ask `HYPOTHESIZE`, then `CHALLENGE`, then `DISTILL`. Check that the operations
   differ, alternatives are meaningful, and speculation remains qualified.
7. Ask `@Dialectical help`. Expect the ASCII command card.
8. Ask `SAVE this finding` with no storage available. Expect a copyable record
   and an honest statement that it was not saved elsewhere.

## iPhone acceptance test

1. Open ChatGPT on the iPhone with the same account and workspace.
2. Start a new Chat or Work conversation.
3. Select **Dialectical** from the `@` menu and repeat the startup test.
4. Repeat HYPOTHESIZE, CHALLENGE, DISTILL, and the no-storage SAVE test.
5. Keep the Mac and any former localhost server off during this test.
6. In another new chat, paste a checkpoint and ask Dialectical to RESUME it.
   It should use that supplied context without claiming unseen chat access.

Official documentation supports account-available plugins in Chat and Work on
mobile. Local/desktop-only plugins are a different distribution path. If
Dialectical is missing on iPhone, check account/workspace, installation, and
whether only a local desktop copy was installed. Record the observed limitation
rather than claiming the mobile test passed.

## Public directory (optional)

Public submission is separate from private installation. Upload the ZIP through
[OpenAI Platform Plugins](https://platform.openai.com/plugins), complete the
metadata/skill scans and applicable review, and publish only after approval.
A skills-only package does not require MCP setup, server hosting, or MCP review
credentials. Publisher verification and directory policies still apply.
Do not confuse a submitted draft with an installed or published plugin.

## Sources and verification boundary

Checked against current official documentation during the 0.4.0 cleanup:

- [Build and edit plugins](https://learn.chatgpt.com/docs/build-plugins)
- [Install, invoke, and use plugins on supported surfaces](https://learn.chatgpt.com/docs/plugins)
- [Portable package structure](https://developers.openai.com/plugins/build/plugins)
- [Skill authoring](https://developers.openai.com/plugins/build/skills)
- [Upload, review, and skills-only metadata requirements](https://developers.openai.com/plugins/deploy/submission)

These are installation and test instructions. A local build is not evidence
that the account update or either device test has been completed.
