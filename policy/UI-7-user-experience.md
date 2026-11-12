# UI-7 User experience: tasks, navigation and flow

Draft key: UI-7 · Clause prefix: `UX` · Version 1 (draft, 12 Nov 2026) · Owner: Head of Product

## Purpose

UI-1 to UI-6 make a screen look and behave correctly. This policy makes the product work for the people using it: clinic staff who are busy and often interrupted, doctors who must not act on the wrong patient, and patients who use the portal once in a while. It covers how people find their way, how many steps a task takes, and what happens when something goes wrong.

## Standards this policy applies

| Standard | What it covers here |
|---|---|
| ISO 9241-11:2018 *Usability: definitions and concepts* | Usability is measured as effectiveness, efficiency and satisfaction for named users, tasks and settings (UX-2, UX-12). |
| ISO 9241-110:2020 *Interaction principles* | The seven principles every screen follows (UX-1). |
| ISO 9241-210:2019 *Human-centred design for interactive systems* | Design from real users, tasks and settings, and evaluate with users (UX-12). |
| ISO 9241-143:2012 *Forms* | Data entry (UX-7). |
| IEC 62366-1:2015+A1:2020 *Usability engineering for medical devices* | Clinical functions where a use error could harm a patient (UX-11, UX-12). Mandatory for any part of a product that is regulated as medical device software. |
| NISTIR 7804 (2012) and NISTIR 7804-1 (2015) *Usability of electronic health records* | How to test critical clinical tasks and find use errors (UX-12). |
| WHO Patient Safety Solutions (2007), *Patient identification* | At least two identifiers before acting for a patient (UX-4, UX-11). |
| WCAG 2.2 Level AA (ACC-11) | The success criteria named in the clauses below. |

No published standard sets a maximum number of clicks. The "three-click rule" is folklore and research does not support it. Step and time budgets are therefore set per task by each product (UX-2) and measured.

## Clauses

**UX-1 Interaction principles.** *Must.* Every screen and flow meets the seven interaction principles of ISO 9241-110:2020:
- **Suitable for the task:** it shows what the task needs, in the order the work happens, and nothing that gets in the way.
- **Self-descriptive:** users can tell where they are, what they can do and what just happened, without training or a manual.
- **As users expect:** the same thing looks and works the same way everywhere (WCAG 3.2.3, 3.2.4), and follows the clinic's own vocabulary and paper forms where they exist.
- **Learnable:** a new user can do the common tasks on their first day; experienced users get shortcuts (UX-6).
- **Controllable:** users decide the pace. They can pause, go back, cancel and pick up where they left off (UX-10).
- **Robust against use errors:** mistakes are prevented where possible and easy to correct where not (UX-8).
- **Engaging:** the product feels trustworthy and calm, and never rushes or nags.

**UX-2 Key tasks have step and time budgets.** *Must.*
- Each product keeps a **task register**: its key tasks (the most frequent ones, and every task where an error could harm a patient or lose money). For each task the register names the user role, where the task starts, the steps it takes and a target time. For example: register a walk-in, book an appointment, check a patient in, take payment, record an allergy.
- Targets come from the product plan where it sets them (for the clinic system: registration in under 90 seconds, checkout in under 2 minutes). Otherwise the product owner sets them.
- **Counting steps:** a step is one click, tap or key press that the user must make to move on, such as choosing, confirming or navigating. Typing a value into a field counts as one step for that field.
- *Should:* these default budgets apply unless the register sets others:
  - a key task can be **started from anywhere** in at most 2 steps (navigation, global search or the quick action menu);
  - a key task is **completed** on one screen, or in one short linear flow, without the user leaving it to look something up;
  - the **most frequent task** of a role is reachable in 1 step from that role's home screen.
- Estimate a new flow's time during design with the Keystroke-Level Model (Card, Moran and Newell), and confirm it with timed tests (UX-12).
- A change that adds a step or time to a key task is reported, with the reason (SCP-4).

**UX-3 Wayfinding.** *Must.*
- **Where am I:** every screen shows its page title (CMP-22), the active navigation item, and the context it belongs to (outlet, patient, visit). A page more than one level deep shows a breadcrumb (CMP-35).
- **How did I get here and how do I get back:** Back returns to the exact previous place, with its filters, sort, scroll position and selection kept. The browser's back button and the platform back gesture do the same. Every distinct screen and filtered view has its own address (URL or deep link), so it can be reloaded, bookmarked and shared without losing the state.
- **Two ways in:** every page can be reached in at least two ways, for example navigation and search (WCAG 2.4.5).
- **Same place, same thing:** navigation, search, notifications and the account menu are in the same place on every screen (WCAG 3.2.3).
- **Role home:** each role lands on a home screen built around its daily work (the front office sees today's queue, a doctor sees today's patients). The home screen is a workspace, not a menu of links.

**UX-4 Finding a patient and knowing it is the right one.** *Must* for products that handle patient records.
- One global search, in the same place on every screen (CMP-22), finds patients by any identifier staff have to hand: name, record number, IC or passport number, phone. It is reachable by keyboard shortcut, and results appear as the user types (ACC-12).
- Every result, and every screen or dialog that acts for one patient, shows **at least two identifiers** (for example full name and record number or date of birth), following the WHO patient identification guidance. Two patients with similar names are visibly told apart.
- Masking (CMP-31) may hide names in lists and on shared screens. Before any clinical or billing action, the identity needed to confirm the right patient is shown, or can be revealed in one step.

**UX-5 Every summary leads to its items.** *Must.*
- A stat card, count, badge, filter chip count, banner, attention item or notification that refers to items opens **those exact items** in one step: the list shows the same number the summary showed, with the filter that produced it visible and removable. An item that refers to one object (an alert about one device, a notification about one invoice) opens that object.
- Back from there returns to the summary (UX-3).
- A number that leads nowhere does not look clickable, and a number that leads somewhere looks clickable and has an accessible name that says where it goes ("Show 9 patients in nursing triage").

**UX-6 Actions where the work is.** *Should.*
- The main action of a screen is visible without scrolling, in the same position on every screen of its kind (CMP-27). On phones it stays reachable at the bottom (FND-16).
- An action on one item sits on that item (its row or card). Less frequent actions go into the item's "More" menu.
- A **quick action** menu, reachable from every screen, starts the product's most frequent create tasks (register walk-in, book appointment, new invoice), so they never need navigation first.
- Frequent actions have keyboard shortcuts, listed in the product (for example in the account menu). Shortcuts never replace a visible control (ACC-8).
- An action the user cannot take is either hidden (when they never can) or shown disabled with the reason (when they cannot yet, for example "Add a payment method first").

**UX-7 Entering data.** *Must.* Data entry follows ISO 9241-143:
- Nothing already known is asked for again (WCAG 3.3.7). Forms are prefilled from the patient, visit and previous entries, and offer sensible defaults.
- Fields follow the order of the work (and of the paper form staff know, where one exists). Only the fields the task needs are shown; the rest stay optional or behind "More details".
- Faster input is offered where it exists: scanning an IC (MyKad) or a barcode, choosing from recent values, typing to search a long list.
- A long form saves a draft as the user goes, so an interruption or a timeout loses nothing (UX-10).
- Validation and error messages follow CMP-2.

**UX-8 Preventing and recovering from errors.** *Must.*
- Destructive actions ask first (CMP-21). For low-risk actions, prefer **undo** (a toast with "Undo" for a few seconds, CMP-17) over a confirmation, so confirmations keep their weight.
- Submissions with legal or financial effect (payments, refunds, issuing an invoice, sending an e-Invoice, clinical orders) can be reviewed before they are final, or reversed afterwards (WCAG 3.3.4). The review shows exactly what will happen ("Charge RM 120.00 to Visa ending 4421").
- An error never loses what the user entered. The message says what went wrong and how to continue (CNT-4).
- A session timeout warns at least 2 minutes before, lets the user extend it, and keeps unsaved work for when they sign in again (WCAG 2.2.1).

**UX-9 Feedback and response time.** *Should.*
- Every action shows a visible response within about 0.1 second (the pressed state, ACC-3, counts).
- An action that takes longer than about 1 second shows progress. One that takes longer than about 10 seconds shows how far it has got, and the user can keep working or cancel. These thresholds are the long-established limits of human response perception (Miller 1968; Card, Moran and Newell 1983).
- The result of an action is visible where the user is looking: the saved item updates in place, and a toast confirms only what is not otherwise visible (CMP-17).
- Data that changes while the screen is open says how fresh it is (CMP-29).

**UX-10 Interruptions and switching.** *Must.*
- Leaving a task and coming back finds it as it was: drafts, filters, selected tabs and scroll position are kept for the session (UX-3, UX-7).
- Working on two patients at once is either supported safely (each in its own clearly labelled tab or window, with the patient identity always visible, UX-4) or prevented, never half supported.
- Notifications never take focus or cover the work. Only a critical, time-bound event (for example a critical result or an emergency call) may interrupt, and it says what to do.

**UX-11 Clinical safety.** *Must* for functions that create, change or display clinical information.
- A screen about one patient keeps that patient's identity and critical alerts (allergies, alerts set by clinicians) visible at the top, without scrolling, on every tab and step.
- An alert interrupts only when it matters for the action being taken, and says why. Repeated or low-value alerts are reduced, because alert fatigue causes real alerts to be missed.
- Clinical values show their unit, and their time where it matters (CNT-2, CNT-3). An abnormal value is marked with an icon and words, not colour alone (ACC-7).
- Where any part of the product is regulated as medical device software, that part follows IEC 62366-1 in full: use specification, hazard-related use scenarios, and formative and summative evaluation.

**UX-12 Evidence with real users.** *Must* before a release that adds or changes a key task (UX-2).
- **During design:** walk through each changed key task against its budget: count the steps, estimate the time, and do one pass with the keyboard only. AI assistants do this walkthrough and report the counts (SCP-9).
- **With users:** test key tasks with people from each role that does them (ISO 9241-210), in a setting like theirs. Record task success, time, errors and close calls. *Should:* about five people per role per round of design testing. Use NISTIR 7804 for critical clinical tasks.
- **Satisfaction:** *Should:* measure with the System Usability Scale (Brooke 1996) after testing, and treat a score below 68 (the average across published studies, Sauro 2011) as a reason to improve before release.
- A task that misses its budget, or a use error that could harm a patient or lose money, is fixed before release, or accepted in writing by the product owner with the reason (SCP-13 applies to every use error found).

**UX-13 Patient-facing screens.** *Must* for the patient portal, kiosks, reminders and anything else a patient uses.
- Written for a lay reader: plain words, no internal codes or clinical shorthand, one task per screen.
- Available in the languages of the clinic's patients (CNT-5); for Malaysia, at least Malay and English.
- Built for phones first (FND-16), usable with large text (WCAG 1.4.4), and never dependent on a mouse.
- A patient can always see who to contact and how, in the same place on every screen (WCAG 3.2.6).
