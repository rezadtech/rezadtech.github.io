# RDTECH — Reza Dayhool's weblog

A static, dependency-free site for GitHub Pages. Home offers two categories; each opens a themed page containing its own resume and journal area. English content follows the supplied resumes and CODEX_RESUME_MEMORY.md. No fabricated blog posts or metrics are included.

## Preview

From this directory run `python -m http.server 8000` and open http://localhost:8000. Or open index.html directly. The print button opens the browser print dialog, with a resume-focused print stylesheet.

## GitHub Pages

Upload the contents of this folder to a repository (root level, including .github and .nojekyll). For a personal site, use rezadtech.github.io as the repository name; a project repository also works because local links are relative. In repository Settings → Pages choose GitHub Actions, then push to main or run the Deploy GitHub Pages workflow. No repository has been created and nothing has been published by this task.

## Editing

- index.html: landing page.
- cybersecurity.html: cybersecurity resume and journal.
- photonics.html: optical research resume, publication, and journal.
- assets/style.css: responsive themes and print layout.
- assets/site.js: print action.

To add a blog post, create an HTML page and link it from the appropriate journal section. Write only your own approved content; the current journal sections honestly indicate that no articles have been published here yet.

## Content review before publishing

Review current employment and contact details. Fara Afrand dates were omitted because source resumes disagree. Research dates follow the supplied DOCX; cleanroom and simulation coursework follows the optics resume, without implying fabrication experience. Graduation dates and unconfirmed impact metrics were omitted. The public pages include your professional email and existing professional profile links, but omit your phone number. No resume-source files or private memory files are included.
