import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Your Comprehensive Guide to Intelligent Robot Systems',
  favicon: 'img/favicon.ico',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  url: 'https://your-docusaurus-site.example.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'facebook', // Usually your GitHub org/user name.
  projectName: 'docusaurus', // Usually your repo name.

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: false,
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'ai-book',
        path: 'ai-book-docs',
        routeBasePath: 'ai-book',
        sidebarPath: require.resolve('./ai-book-docs/sidebar.ts'),
      },
    ],
    // Custom Webpack plugin to expose REACT_APP_FASTAPI_BASE_URL to client-side
    function (context, options) {
      return {
        name: 'webpack-env-plugin',
        configureWebpack(config, isServer, utils) {
          // Only apply on the client-side build
          if (!isServer) {
            config.plugins.push(
              new (require('webpack').DefinePlugin)({
                'process.env.REACT_APP_FASTAPI_BASE_URL': JSON.stringify(process.env.REACT_APP_FASTAPI_BASE_URL),
              }),
            );
          }
          return config;
        },
      };
    },
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
              logo: {
                alt: 'Physical AI Humanoid Robotics Logo',
                src: 'img/physical-ai-robotics-logo.png',
              },              items: [
                {
                  to: '/ai-book/intro',
                  label: 'Text Book',
                  position: 'left',
                  activeBaseRegex: `/ai-book/`,
                  docsPluginId: 'ai-book',
                },
                {
                  href: 'https://github.com/BBismaarshad',
                  label: 'GitHub',
                  position: 'right',
                },
              ],    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'AI Book',
              to: '/ai-book/intro',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Youtube',
              href: 'http://youtube.com/channel/UC0SxCVKA6U2oDSZ1ecK_TMA',
            },
            {
              label: 'Twitter',
              href: 'https://x.com/BismaArshad_Dev/',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/BBismaarshad',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;