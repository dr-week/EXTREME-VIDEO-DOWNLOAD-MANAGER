Use these skills:

* ytdown-core
* ytdown-visual-ui
* ytdown-source-intelligence
* ytdown-media-conversion

Do not begin until backend and worker source-media tests pass.

Implement the source-aware frontend milestone only.

Requirements:

1. Preserve the existing download form and API behaviour.
2. Inspect the source through the new backend inspection endpoint.
3. Debounce inspection by approximately 350 milliseconds.
4. Do not inspect empty or invalid input.
5. Cancel or ignore outdated inspection responses.
6. Display a platform badge.
7. Display recognized source name.
8. Display detected content type.
9. Display capability state:

   * Direct media
   * Recognized; checking support
   * Probe required
   * Generic website
10. Display authentication warning when returned.
11. Do not display Pinterest as guaranteed.
12. Display WebP conversion controls only when relevant.
13. Conversion targets:

* Automatic
* PNG
* JPEG
* GIF

14. Default conversion to automatic.
15. Explain automatic behavior:

* animation -> GIF
* transparency -> PNG
* opaque image -> JPEG

16. Display processing, conversion, success and failure states.
17. Display the final file format.
18. Preserve existing polling behaviour.
19. Do not create fake download percentages.
20. Respect prefers-reduced-motion.
21. Keep animations restrained.
22. Add accessible labels and aria-live status.
23. Verify desktop and mobile layouts.
24. Run frontend lint and production build.

Suggested UI flow:

URL entered
-> platform fades in
-> capability inspection begins
-> available options appear
-> user submits
-> task processing state
-> conversion state when relevant
-> completed result

Do not modify backend or worker logic in this milestone.

Use Windows PowerShell commands only.

Stop after frontend validation.

Do not begin infrastructure work.
Do not deploy.
Do not merge.
Do not push.

