# SEO Fix Maps by Stack

## Next.js (App Router)

### Meta Title & Description
File: `src/app/layout.tsx` or `src/app/page.tsx`
```tsx
export const metadata: Metadata = {
  title: 'Your Page Title (50-60 chars)',
  description: 'Your meta description (120-160 chars)',
}
```

### Canonical URL
File: `src/app/layout.tsx`
```tsx
export const metadata: Metadata = {
  alternates: {
    canonical: 'https://yourdomain.com',
  },
}
```

### Open Graph / Social
File: `src/app/layout.tsx`
```tsx
export const metadata: Metadata = {
  openGraph: {
    title: 'Your Title',
    description: 'Your description',
    url: 'https://yourdomain.com',
    siteName: 'Your Site Name',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Your Title',
    description: 'Your description',
    images: ['/og-image.png'],
  },
}
```

### Robots.txt
File: `src/app/robots.ts` (create if missing)
```ts
import { MetadataRoute } from 'next'
export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: '*', allow: '/' },
    sitemap: 'https://yourdomain.com/sitemap.xml',
  }
}
```

### Sitemap
File: `src/app/sitemap.ts` (create if missing)
```ts
import { MetadataRoute } from 'next'
export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: 'https://yourdomain.com', lastModified: new Date(), changeFrequency: 'monthly', priority: 1 },
  ]
}
```

### Structured Data (Schema.org)
File: `src/app/layout.tsx` or relevant page
```tsx
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: 'Your Site',
  url: 'https://yourdomain.com',
}
// In component:
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
```

### Missing Alt Text
Find all `<Image>` and `<img>` without `alt` prop, add descriptive alt text.

---

## Next.js (Pages Router)

### Meta Title & Description
File: `pages/_app.tsx` or individual page files
```tsx
import Head from 'next/head'
<Head>
  <title>Your Title</title>
  <meta name="description" content="Your description" />
</Head>
```

### Robots.txt & Sitemap
Create `public/robots.txt` and `public/sitemap.xml` directly.

---

## Plain HTML

### Meta Title
```html
<title>Your Page Title (50-60 chars)</title>
```

### Meta Description
```html
<meta name="description" content="Your description (120-160 chars)">
```

### Canonical
```html
<link rel="canonical" href="https://yourdomain.com/page">
```

### Open Graph
```html
<meta property="og:title" content="Your Title">
<meta property="og:description" content="Your description">
<meta property="og:image" content="https://yourdomain.com/og-image.png">
<meta property="og:url" content="https://yourdomain.com">
<meta property="og:type" content="website">
```

### Twitter Card
```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Your Title">
<meta name="twitter:description" content="Your description">
<meta name="twitter:image" content="https://yourdomain.com/og-image.png">
```

### Structured Data
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Your Site",
  "url": "https://yourdomain.com"
}
</script>
```

### Robots.txt
Create `robots.txt` in project root:
```
User-agent: *
Allow: /
Sitemap: https://yourdomain.com/sitemap.xml
```

### Missing Alt Text
Find all `<img>` tags without `alt` attribute and add descriptive alt text.

---

## Nuxt 3

### Meta Title & Description
File: `nuxt.config.ts`
```ts
export default defineNuxtConfig({
  app: {
    head: {
      title: 'Your Title',
      meta: [{ name: 'description', content: 'Your description' }],
    },
  },
})
```
Or per-page using `useSeoMeta()`:
```ts
useSeoMeta({ title: 'Your Title', description: 'Your description' })
```

### Robots.txt & Sitemap
Use `@nuxtjs/robots` and `@nuxtjs/sitemap` modules.

---

## Vue SPA (Vite)

### Meta Tags
Use `vite-plugin-html` or edit `index.html` directly:
```html
<title>Your Title</title>
<meta name="description" content="Your description">
```
For dynamic meta, use `vue-meta` or `@vueuse/head`.

---

## Issue ID → Fix Map

| seomator issue id | Stack | Action |
|---|---|---|
| `meta-description` | all | Add description metadata |
| `title-missing` | all | Add title metadata |
| `title-length` | all | Shorten title to 50-60 chars |
| `canonical-missing` | all | Add canonical link |
| `og-title` | all | Add og:title |
| `og-description` | all | Add og:description |
| `og-image` | all | Add og:image (1200x630px) |
| `twitter-card` | all | Add twitter:card meta |
| `structured-data` | all | Add JSON-LD schema |
| `robots-txt` | all | Create robots.txt |
| `sitemap` | all | Create sitemap.xml |
| `image-alt` | all | Add alt attributes to images |
| `h1-missing` | all | Add single H1 to page |
| `h1-multiple` | all | Remove extra H1 tags |
| `https` | manual | Configure SSL on hosting |
| `gzip` | manual | Configure compression on server |
| `core-web-vitals` | manual | Performance optimization needed |
