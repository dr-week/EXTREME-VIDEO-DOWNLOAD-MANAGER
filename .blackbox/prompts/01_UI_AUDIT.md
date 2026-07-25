Use the ytdown-core and ytdown-visual-ui skills.

Repository:

E:\CODES\001\YTDOWN

Read:

* .blackbox\PROJECT_STATE.md
* .blackbox\WORKFLOW.md
* .blackbox\skills\ytdown-core\SKILL.md
* .blackbox\skills\ytdown-visual-ui\SKILL.md
* .blackbox\templates\UI_TASK_TEMPLATE.md

Perform UI-1 audit only.

Do not modify files.
Do not install packages.
Do not create components.
Do not begin infrastructure work.

Inspect:

1. Git status and current branch
2. frontend\package.json
3. frontend package lock file
4. frontend\src complete structure
5. application entry file
6. current App component
7. all current frontend components
8. global CSS
9. Tailwind configuration
10. Vite configuration
11. environment variable usage
12. backend API base URL
13. URL submission flow
14. format field
15. quality field
16. custom directory field
17. task creation request
18. task ID response
19. status polling route
20. polling interval and retry limit
21. processing state
22. completed state
23. failure state
24. reset or retry behaviour
25. installed animation libraries
26. installed icon libraries
27. available npm scripts
28. mobile layout problems
29. accessibility problems
30. likely browser console problems

Return:

### Repository State

* current branch
* changed files
* untracked files

### Frontend Stack

* React version
* Vite version
* Tailwind version
* other relevant packages

### Current File Structure

List important frontend files and their roles.

### Functional Contract

Report exact:

* API base URL
* task creation method
* task creation route
* request body
* task ID field
* status route
* polling interval
* retry limit
* processing values
* completed values
* failure values

### Current UI Problems

List specific problems found in actual code.

### Proposed Component Structure

Propose the smallest suitable component structure.

### Animation Strategy

State:

* whether an animation library already exists
* whether CSS is sufficient
* whether a new package is justified
* reduced-motion approach

### Exact Files To Modify

List exact paths only.

### Validation Commands

Give Windows PowerShell commands only.

Stop after the audit.

