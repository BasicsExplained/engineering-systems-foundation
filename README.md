# Engineering Systems Foundation — Private Course Source

This private repository contains the complete master source for the **Engineering Systems Foundation: Signal-to-Cloud** one-month internship course.

The students should not browse this repository. They should receive only the published documentation website.

## Public documentation site behavior

The GitHub Actions workflow builds a public documentation site from the files in this private repository. The build includes:

- always-available course rules, roadmap, templates, and basic glossary
- only checkpoint folders whose number is less than or equal to `unlocked_until` in `release-config.json`

Future checkpoint materials remain in this private repository and are not published to the website until the unlock number is increased.

## Release a checkpoint

Edit `release-config.json`:

```json
{
  "unlocked_until": 2
}
```

Commit and push. The workflow will rebuild the public docs site with Checkpoint 02 included.

## Suggested student URL

After GitHub Pages is enabled with **Source: GitHub Actions**, the site should be available at:

```text
https://basicsexplained.github.io/engineering-systems-foundation/
```

## Important

Do not change Pages to publish from repository root, because this private repo contains all master content. Use the included GitHub Actions workflow.
