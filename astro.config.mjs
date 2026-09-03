// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://wiki.irosec.com',
  integrations: [
    starlight({
      title: 'irosec',
      favicon: '/favicon.svg',
      description: 'Homelab, security portfolio, and project documentation.',
      social: {
        github: 'https://github.com/Gasteren',
      },
      editLink: {
        // Lets readers jump to the source markdown on GitHub. Point this at
        // wherever the site repo actually lives.
        baseUrl: 'https://github.com/Gasteren/irosec-homelab/edit/main/starlight-wiki/',
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
      ],
      customCss: [
        // Add a custom stylesheet for branding tweaks later:
        // './src/styles/custom.css',
      ],
      lastUpdated: true,
      pagination: true,
    }),
    sitemap(),
  ],
});
