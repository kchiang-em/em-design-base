# UI-5 Client colour themes

Draft key: UI-5 · Clause prefix: `THM` · Version 1 (draft, 11 Nov 2026) · Owner: not yet named

## Purpose

Some clients want a product in their own brand colours. This policy says what a client theme may change and what stays the same in every product, so that a themed product is still safe, readable and recognisable.

## Clauses

**THM-1 One theme file.** *Must.* All of a client's colours live in one theme file per product. Raw colour values are allowed there and nowhere else (SCP-3); everywhere else, the product uses the tokens, which the theme overrides.

**THM-2 What a theme may change.** *May.* The brand palette (navy, blue, slate, greys), the brand scale (the lighter and darker shades for hover, tinted backgrounds and dark surfaces), text colours, surfaces and borders, and the tint of the keyboard focus ring and the shadows. The pressed colours only as THM-8 allows.

**THM-3 Status colours never change.** *Must.* A theme never changes red, orange or green (FND-3). If a user asks to change them, decline and explain that status colours are universal.

**THM-4 Only colours are themed.** *Must.* A theme never changes sizes, spacing, radii, the type scale, or the five control states and their structure.

**THM-5 The main colour and its shades change together.** *Must.* When the main brand colour changes, its lighter and darker shades change with it, derived from it by the standard derivation, not invented one by one. Otherwise hover and tinted states keep the old colours.

**THM-6 Contrast holds.** *Must.* A themed product meets ACC-6: white text on the new primary colour and its hover shade, headings on white, text in the pressed state, and dark text on the green navigation toggle all stay at 4.5:1 or better. A colour that fails is darkened or lightened, and the user is told the before and after.

**THM-7 Extra client colours.** *May.* A client colour with no EncoreMed role (a second brand colour, a highlight) is added to the theme as a new, client-named colour and used only through that name. It is never used for a status (FND-3), and text on it keeps 4.5:1.

**THM-8 The pressed state stays amber.** *Must.* The pressed state stays amber by default (ACC-3). If the client's brand is itself amber, orange or yellow, tell the user that pressed may be hard to tell apart, and change the pressed colours only if they ask, keeping pressed text at 4.5:1.

**THM-9 A primary close to a status colour.** *Must.* A primary colour whose hue is close to red, orange or green is allowed, but tell the user: because status colours cannot change, errors or warnings may look like the brand. Status messages keep their icon and text label (ACC-7).

**THM-10 Where theme colours come from.** *Must.*
- Use colour codes the user gives. Convert other notations (rgb, hsl) to hex. For a colour name ("burgundy") or a brand name, ask for the code; do not guess.
- When the user gives a logo instead, read its colours with a measuring tool from the logo file. Never use a colour estimated by eye from an image or screenshot.
- When it is unclear which colour plays which role, choose the most likely one and say so. For a logo, confirm the colours and their roles with the user before applying them, unless they said to go ahead.

**THM-11 The client logo is an asset.** *Must.* A logo is not a theme colour. Placing a client logo in the product is a separate task: keep its proportions and clear space, never recolour or stretch it (CMP-20), and say if its shape (for example a wide wordmark) does not fit the logo tile and needs a design decision.

**THM-12 Out of a theme's scope.** *Must.* A typeface change, dark mode, gradients, illustrations and photos are not part of a colour theme. Tell the user and treat each as a separate decision (SCP-5, FND-15).

**THM-13 Report the theme.** *Must.* Tell the user which colours were themed and to what values, which colour was treated as primary and secondary if they did not say, what was deliberately left unchanged (status colours, sizes, states), and any colour that was adjusted.
