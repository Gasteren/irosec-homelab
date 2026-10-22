// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://wiki.irosec.com',
  integrations: [
    starlight({
      title: 'irosec',
      favicon: '/favicon.png',
      components: {
        Banner: './src/components/Banner.astro',
        EditLink: './src/components/EditLink.astro',
        SocialIcons: './src/components/SocialIcons.astro',
      },
      logo: {
        src: './src/assets/logo.png',
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
      // Sidebar is auto-generated from folder/file structure by default.
      // Uncomment and customize once content is migrated if you want manual
      // grouping instead of autogenerate:
      //
      // sidebar: [
      //   {
      //     label: 'Homelab',
      //     autogenerate: { directory: 'homelab' },
      //   },
      //   {
      //     label: 'WoW Addons',
      //     autogenerate: { directory: 'addons' },
      //   },
      // ],
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
          label: 'Addons',
          link: '/addons/',
        },
      ],
      head: [
        {
          tag: 'script',
          attrs: { src: '/lightbox.js', defer: true },
        },
      ],
      customCss: [
        './src/styles/custom.css',
        // Add a custom stylesheet for branding tweaks later:
        // './src/styles/custom.css',
      ],
      lastUpdated: true,
      pagination: true,
    }),
    sitemap(),
    mdx(),
  ],
});
