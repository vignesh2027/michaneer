# Green Shift Hacks: rules as recorded

Source pages fetched on 6 November 2026:

* Overview: https://green-shift-hacks.devpost.com/
* Rules: https://green-shift-hacks.devpost.com/rules
* Schedule: https://green-shift-hacks.devpost.com/details/dates
* Gallery: https://green-shift-hacks.devpost.com/project-gallery ("The hackathon managers haven't published this gallery yet, but hang tight!")
* Updates: https://green-shift-hacks.devpost.com/updates (no announcements yet)

Quoted text is copied from those pages. Notes in plain paragraphs are ours.

## Key facts

| Item | Value |
| --- | --- |
| Host | HackathonForEveryone. Judges listed as "GreenShift, GreenShiftTeam". Manager contact ssisodia@scu.edu |
| Submission period | 19 October 2026, 12:00 AM UTC to 17 November 2026, 10:00 PM UTC |
| Deadline in India | **Wednesday 18 November 2026, 03:30 IST** (verified) |
| Winners announced | 21 November 2026, 10:00 PM UTC |
| Prize | Green Shift Grand Prize, **$125 cash, 1 winner** (verified). No other prizes |
| Eligibility | Students only, above the legal age of majority, companies excluded, all countries except standard exceptions. "Teams may have up to four members." Solo is allowed |
| Participants | 158 registered on 6 November 2026 |
| Themes | Beginner Friendly, Social Good |

## Important difference from AccessED, SafeSpace and LaunchPad

The brief assumed the same organiser and the same four criteria. That is not the case. AccessED, SafeSpace and LaunchPad are run by Hack4TodayOrg with four criteria scored 1 to 5 (see /Users/vignesh/olivaasi/RULES.md, /Users/vignesh/kedayam/RULES.md, /Users/vignesh/ainooru/RULES.md). Green Shift Hacks is run by HackathonForEveryone and publishes **one** criterion, with no stated scale. The rules page is also much shorter: it has no resources page, no explicit AI rule and no tie-break rule.

## Judging criteria (verbatim, overview page)

There is exactly one published criterion:

* **Environmental Impact.** "How clearly the project reduces waste, emissions, resource use, or environmental harm."

Rules page: "Projects will be evaluated using the published criteria. Organizer decisions are final."

No scale (1 to 5 or otherwise) and no weighting are published. Our internal scoring uses 1 to 5 for consistency with the sibling entries, and it is ours, not the organiser's.

## Theme text (verbatim, overview page)

> Climate solutions need more than good intentions—they need tools people can use. Green Shift Hacks is an online student hackathon for practical technology that makes sustainable choices easier, clearer, and more scalable.

> Build a prototype that helps people reduce waste, conserve energy or water, choose lower-impact options, repair and reuse materials, understand climate information, or support healthier local systems. Start with a real behavior or system, then show how your solution moves it forward.

> Think beyond awareness: make sustainability more actionable, measurable, and possible.

## Submission requirements (verbatim, overview page "Requirements")

> Build an original technology project with a clear sustainability goal and a working prototype. Your project may focus on energy, waste, water, food, transportation, materials, ecosystems, or climate resilience.

> Submit a complete Devpost project page with a project story, all team members, a demo video or walkthrough, and source code or clear build instructions.

> Explain the problem, the intended users, your approach, the expected environmental benefit, the tools you used, and any limitations. Use data and examples you have permission to share.

Our checklist from this text:

1. Devpost page with a project story and all team members (solo: the owner).
2. A demo video or walkthrough. Unlike the sibling events, this is required here, not optional.
3. Source code or clear build instructions.
4. The story must cover: problem, intended users, approach, expected environmental benefit, tools used, limitations.
5. Only data and examples we have permission to share. All data in this project is public and cited in `michaneer/sources.py` and the README.

## New-work rule (verbatim, rules page)

> Projects must be original work created during the event period. Pre-existing open-source tools and datasets may be used when clearly credited.

The event period is 19 October to 17 November 2026. Michaneer is a new repository started on 6 November 2026, and the git history is the evidence. Open-source libraries (FastAPI, Jinja2, Uvicorn, pytest) and public documents are credited in the README.

## AI-assistance credit rule

The Green Shift pages contain no sentence about AI assistance. The only related text is the credit rule above ("Pre-existing open-source tools and datasets may be used when clearly credited") and "Entries must follow Devpost community guidelines and must not include harmful, illegal, or deceptive content." For comparison, the sibling events say AI assistance may be used when disclosed and credited. The lead handles any credits line on Devpost. The app itself makes no AI or LLM calls.

## Entering the same project elsewhere

The Green Shift pages say nothing about entering the same project in another hackathon. The rules page says only "Submit a complete Devpost project page before the deadline." Michaneer is a new idea, distinct from the owner's other entries (Olivaasi, Kedayam, Ainooru, Haat, Mergoshi, Triagewell), and is not planned for any other event.

## Other constraints

* "Entries must follow Devpost community guidelines and must not include harmful, illegal, or deceptive content." The app must not tell anyone their water is safe to drink, and must not present a stayed court direction as law. Both are handled in the copy and covered by tests.
* No secrets or personal data in the repo, screenshots or video. The app stores bucket-test readings only, on the user's own machine.
* Judging links should stay reachable until winners are announced (21 November 2026).

## Competitive landscape

* The Green Shift gallery is unpublished, so no direct competitors are visible.
* Devpost project search for "michaneer" returns 0 results. A web search for RO reject water projects found hardware student projects (Smart India Hackathon 2019 organic filter by SRM students, a KCG College reject-boiling unit) and DIY reuse blog posts, but no software tool that measures a household's own recovery ratio and turns it into a reuse plan.
* GitHub search "RO reject water" returns 2 repositories: a bacteria growth study and a hydroponic planter simulation. Neither overlaps.
