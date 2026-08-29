# Setup

Everything below is a one-time setup. Once done, the README maintains itself.

## 1. File layout

Your profile repo must be named exactly `KumarArsh4720` (same as your username) and be **public**.

```
KumarArsh4720/
├── README.md
├── assets/
│   ├── hero.svg
│   └── stack.svg
└── .github/
    └── workflows/
        └── snake.yml
```

Push to the `main` branch. If your default branch is `master`, change `/main/` to `/master/`
in the two `raw.githubusercontent.com` URLs at the top of the README.

## 2. Replace the placeholders

Search the README for `REPLACE` — there are three, in the **elsewhere** section
(email, LinkedIn, X). Delete any badge you don't want.

## 3. Turn on the contribution snake

> Until you do this, the contribution grid near the bottom of the README will show a broken
> image — the file it points to doesn't exist yet. This step creates it.

Go to the **Actions** tab → *Snake contribution animation* → **Run workflow**.

It writes six variants to a branch called `output`. Pick whichever you like and put its
filename in the README's `<picture>` block:

| file | look |
| :--- | :--- |
| `autumn.svg` | amber → matches the hero banner *(current default)* |
| `ember.svg` | deeper, redder orange |
| `clay.svg` | terracotta |
| `sand.svg` | pale gold on warm black — the softest of the four |
| `github-snake.svg` | stock GitHub light *(current light-mode default)* |
| `autumn.gif` | animated, amber on warm black |

Preview any of them at:
`https://raw.githubusercontent.com/KumarArsh4720/KumarArsh4720/output/<filename>`

After the first run it regenerates automatically twice a day.

## 4. Make the stats cards reliable

The two cards in the **activity** section come from `github-readme-stats.vercel.app`, a free
shared instance. It's rate-limited across all its users, so it intermittently renders a
"Failed to retrieve contributions" box or a broken image — this is what you were seeing before,
and it is not something the README itself can fix.

**The permanent fix is deploying your own copy** (free, ~3 minutes):

1. Go to <https://github.com/anuraghazra/github-readme-stats> and click **Deploy to Vercel** (bottom of the README).
2. Sign in to Vercel with GitHub, accept the defaults, deploy.
3. Create a GitHub personal access token at <https://github.com/settings/tokens> with **no scopes ticked** (public data only — or tick `repo` if you want private repos counted).
4. In your new Vercel project → **Settings → Environment Variables**, add `PAT_1` set to that token. Redeploy.
5. In the README, replace both instances of `github-readme-stats.vercel.app` with your own
   Vercel domain, e.g. `arsh-stats.vercel.app`.

Your own instance has its own rate limit that only you consume, so the cards stop breaking.

## 5. Count private repos

The stats card already passes `count_private=true`, but that only works for repos the token can
see — so it needs the `repo` scope on the PAT from step 4.

Separately, for the contribution graph and snake to include private work:
**GitHub → Settings → Profile → Contributions**, tick *"Include private contributions on my profile"*.

## Why the animation lives in the SVGs, not the README

GitHub runs every README through an HTML sanitiser before rendering it. That sanitiser
**strips `<style>` blocks and `style="..."` attributes**, and it allows only a fixed whitelist
of tags. So CSS written in `README.md` — for falling leaves or anything else — is silently
deleted. There is no flag or workaround for this; it applies to every repo on the site.

What *does* survive is CSS **inside an SVG file** that the README embeds with `<img>`. The
browser loads that SVG as an image and runs its stylesheet normally, so `@keyframes`,
transitions and transforms all work. That is where the leaves, the lamp glow, the rotating
tagline and the chip entrance animations in `assets/` live.

Two limits worth knowing:

- An SVG loaded via `<img>` cannot run JavaScript, and cannot fetch external fonts or images.
  Both banners are therefore fully self-contained and use system font stacks.
- Both files honour `prefers-reduced-motion`, so all motion stops for readers who ask their
  OS to reduce it.

## Regenerating the banners

`gen_assets.py` builds both SVGs. Edit the values at the top of the file (colours, name, role)
or the `taglines` / `rows` lists, then:

```bash
python3 gen_assets.py
```

No dependencies — plain Python 3. The SVGs are self-contained: no external fonts, no network
calls, so they can never break the way the third-party services do.

## Why some things were removed

| removed | reason |
| :--- | :--- |
| `github-readme-activity-graph.vercel.app` | Returns **HTTP 402** — the deployment is over its Vercel quota and is effectively dead. |
| `github-readme-streak-stats.herokuapp.com` | Heroku ended free dynos in Nov 2022. The successor, `streak-stats.demolab.com`, is up but slow and frequently times out. |
| `capsule-render` header/footer waves | Still works, but the custom `hero.svg` replaces it with something that can't go down. |
| `readme-typing-svg` | Same reason — the hero banner's rotating tagline does this locally, with no third party in the path. |
| Pinned-repo cards | Same rate-limited service as the stats cards — replaced with a plain markdown table that always renders. |
