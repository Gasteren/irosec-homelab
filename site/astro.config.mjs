// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://wiki.irosec.com',
  // Under `astro dev`, serve /api/*.json (the live data nginx provides in
  // production, see nginx.conf.template) straight from GitHub.
  vite: {
    server: {
      proxy: {
        '/api': {
          target: 'https://raw.githubusercontent.com',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api\//, '/Gasteren/irosec-homelab/main/data/'),
        },
      },
    },
  },
  integrations: [
    starlight({
      title: 'irosec',
      favicon: '/favicon.png',
      components: {
        EditLink: './src/components/EditLink.astro',
        Footer: './src/components/Footer.astro',
        PageTitle: './src/components/PageTitle.astro',
        SocialIcons: './src/components/SocialIcons.astro',
      },
      logo: {
        // logo-light.png is the same artwork with dark text, for the light theme.
        dark: './src/assets/logo.png',
        light: './src/assets/logo-light.png',
        replacesTitle: true,
      },
      description: 'Homelab, security portfolio, and project documentation.',
      social: {
        github: 'https://github.com/Gasteren',
        linkedin: 'https://linkedin.com/in/vgasteren',
      },
      editLink: {
        // Lets readers jump to the source markdown on GitHub. Section pages are
        // mapped back to their folders at the repo root by the EditLink override.
        baseUrl: 'https://github.com/Gasteren/irosec-homelab/edit/main/site/',
      },
      sidebar: [
        {
          label: 'Infrastructure',
          autogenerate: { directory: 'infrastructure' },
        },
        {
          label: 'Security Stack',
          autogenerate: { directory: 'security-stack' },
        },
        {
          label: 'Projects',
          autogenerate: { directory: 'projects' },
        },
        {
          label: 'Lessons Learned',
          autogenerate: { directory: 'lessons-learned' },
        },
        {
          label: 'World of Warcraft',
          items: [{ label: 'Addons', link: '/addons/' }],
        },
      ],
      head: [
        {
          tag: 'script',
          attrs: { src: '/lightbox.js', defer: true },
        },
      ],
      customCss: ['./src/styles/custom.css'],
      expressiveCode: {
        styleOverrides: { borderRadius: '0.75rem' },
      },
      lastUpdated: true,
      pagination: true,
    }),
    sitemap(),
    mdx(),
  ],
});
