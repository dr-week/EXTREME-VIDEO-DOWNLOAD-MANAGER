name: ytdown-visual-ui
description: Iteratively improves the YTDOWN React interface, responsive layout, accessibility, visual polish and animations one screen or component at a time without breaking downloader functionality.

---

# YTDOWN Visual UI Skill

## Purpose

Improve the existing YTDOWN frontend through small, visually verifiable iterations.

Do not rebuild the entire frontend in one task.

Required cycle:

Inspect
-> Select one visual target
-> Implement
-> Run
-> Inspect result
-> Correct
-> Verify
-> Stop

## Required Reading

Before changing frontend files, read:

1. `.blackbox\PROJECT_STATE.md`
2. `.blackbox\WORKFLOW.md`
3. `.blackbox\skills\ytdown-core\SKILL.md`
4. `.blackbox\skills\ytdown-visual-ui\SKILL.md`
5. `.blackbox\templates\UI_TASK_TEMPLATE.md`
6. `frontend\package.json`
7. frontend source tree
8. current Git diff

## First UI Run

The first run must be an audit.

Do not modify files during the first audit.

Inspect:

* React version
* Vite version
* Tailwind version
* installed animation libraries
* installed icon libraries
* frontend source structure
* application entry file
* form state
* URL validation
* format and quality controls
* custom directory behaviour
* API base URL
* task creation request
* task polling request
* loading state
* completed state
* failure state
* reset behaviour
* mobile layout
* keyboard accessibility
* colour contrast
* console warnings
* available npm scripts

## UI Scope

UI work may modify only:

* `frontend\src\`
* frontend-specific CSS files
* frontend assets
* `frontend\package.json`
* frontend lock file
* frontend Tailwind configuration
* frontend Vite configuration when necessary
* `.blackbox\PROJECT_STATE.md` after validation passes

Do not modify:

* backend\
* worker\
* terraform\
* k8s\
* .github\
* main.py

## Design Objective

Create a modern, premium and trustworthy video downloader interface.

The interface should feel:

* focused
* fast
* clear
* technically capable
* responsive
* accessible
* visually restrained

## Suggested Page Structure

Use the existing application structure where possible.

A suitable layout may contain:

1. App shell
2. Navigation or compact brand header
3. Hero introduction
4. Downloader form
5. Format and quality controls
6. Task progress area
7. Success or failure result
8. Small privacy or local-processing note
9. Footer

Do not add sections merely to make the page longer.

## Component Strategy

Prefer clear reusable components such as:

* `AppShell`
* `BackgroundEffects`
* `Header`
* `Hero`
* `DownloadForm`
* `UrlInput`
* `FormatSelector`
* `QualitySelector`
* `DirectoryControl`
* `DownloadButton`
* `TaskStatusCard`
* `ProgressIndicator`
* `SuccessState`
* `ErrorState`
* `ConnectionStatus`

Do not split components when the component would contain only trivial markup.

## Visual Direction

Use:

* dark premium background
* restrained gradient accents
* clear typography hierarchy
* clean form controls
* rounded cards
* subtle borders
* visible focus states
* consistent spacing
* strong primary action
* simple supporting icons
* mobile-first responsive behaviour

Avoid:

* excessive neon
* unreadable transparency
* giant glowing blobs
* heavy 3D effects
* background videos
* constant movement
* fake progress
* excessive blur
* excessive shadows
* animation on every element
* unnecessary marketing sections

## Animation Strategy

Use an existing animation package when already installed.

If no animation library exists:

1. inspect React version
2. inspect package compatibility
3. explain why a dependency is needed
4. install only one lightweight animation dependency
5. update the lock file
6. run a production build

Preferred animations:

* initial hero entrance
* staggered form entrance
* button hover
* button tap feedback
* selector transition
* task-card entrance
* processing-state transition
* completed-state check animation
* one-time failure shake
* subtle background drift
* progress change transition

Do not:

* animate important text continuously
* animate every polling response
* use fast flashing
* block interaction during animation
* loop large elements
* create fake numerical progress
* hide errors behind animation

## Reduced Motion

Respect reduced-motion preferences.

When using CSS:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 0.01ms !important;
  }
}
```

When using an animation library, use its reduced-motion support where available.

## Functional Protection

Do not alter API fields for visual reasons.

Before changing the form, identify the exact:

* task creation route
* request method
* request payload
* required fields
* optional fields
* response task identifier
* status route
* polling interval
* polling limit
* success status values
* failure status values

Keep those contracts unchanged.

## Accessibility

Every UI milestone must preserve or improve:

* keyboard navigation
* form labels
* input descriptions
* validation messages
* visible focus
* sufficient contrast
* button disabled state
* loading announcement
* error announcement
* reduced motion
* semantic headings

Use `aria-live` for asynchronous task status when suitable.

Do not rely only on colour to communicate status.

## Responsive Requirements

Verify at minimum:

* approximately 375px width
* approximately 768px width
* approximately 1280px width
* approximately 1440px width

Do not allow:

* horizontal page scrolling
* controls outside cards
* clipped select content
* unreadable status messages
* buttons below touch-friendly height
* excessive empty space on mobile

## Performance

Avoid:

* giant animation dependencies
* unnecessary global state libraries
* unnecessary API calls
* large uncompressed media
* full-screen continuously animated blur
* repeated re-renders caused by animation
* animations tied to every polling tick

## Visual Verification

After implementation:

1. start the frontend using its actual package script
2. inspect the page in a browser
3. check browser console
4. test desktop layout
5. test mobile layout
6. test hover and keyboard focus
7. test reduced-motion behaviour where possible
8. test loading, success and failure states
9. correct visible problems
10. stop after the selected milestone

Use screenshot or browser inspection tools when available.

Do not claim visual verification if the page was not opened.

## Required Validation

First detect actual package scripts.

Run available commands such as:

```powershell
Set-Location "E:\CODES\001\YTDOWN\frontend"

npm install
npm run lint
npm run test
npm run build
```

Then:

```powershell
Set-Location "E:\CODES\001\YTDOWN"

git diff --check
git status
```

Do not run a missing npm script.

Mark it NOT RUN and explain that the script does not exist.

## Iteration Limit

One UI task should modify one main visual target.

Examples:

* application shell
* downloader form
* format selector
* task status card
* success and failure states
* mobile layout
* animation system

Do not change all of them in one run unless the existing frontend is extremely small and the user explicitly approves a complete redesign.

## Response Format

### Visual Target

Name one component or screen.

### Audit

Report current structure and problems.

### Implementation

Report exact files and decisions.

### Visual Verification

Report what was actually inspected.

### Validation

Use PASS, FAIL, BLOCKED or NOT RUN.

### Stop Point

Recommend only one next visual target.

