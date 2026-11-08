import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Physical AI & Humanoid Robotics | The Open Curriculum for Embodied AI',
  tagline: 'Master low-latency ROS 2 middleware, physics-accurate Digital Twins, NVIDIA Isaac perception, and Vision-Language-Action (VLA) foundation models for autonomous bipedal humanoids.',
  favicon: 'img/favicon.svg',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
    faster: {
      rspackPersistentCache: false, // Disables Windows file-locking persistent cache crashes
    },
  },

  // Set the production url of your site here
  url: 'https://mudassirt.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  baseUrl: '/',

  // GitHub pages deployment config.
  organizationName: 'MudassirT',
  projectName: 'Physical-AI-Humanoid-Robotics',

  onBrokenLinks: 'throw',
  onBrokenAnchors: 'ignore',

  // Senior SEO Head Tags Injection
  headTags: [
    // Preconnect to Google Fonts
    {
      tagName: 'link',
      attributes: {
        rel: 'preconnect',
        href: 'https://fonts.googleapis.com',
      },
    },
    {
      tagName: 'link',
      attributes: {
        rel: 'preconnect',
        href: 'https://fonts.gstatic.com',
        crossorigin: 'anonymous',
      },
    },
    // Primary JSON-LD Structured Data: Course & WebSite Schema
    {
      tagName: 'script',
      attributes: {
        type: 'application/ld+json',
      },
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@graph': [
          {
            '@type': 'WebSite',
            '@id': 'https://your-docusaurus-site.example.com/#website',
            'url': 'https://your-docusaurus-site.example.com/',
            'name': 'Physical AI & Humanoid Robotics',
            'description': 'The definitive open-access engineering curriculum for Physical AI, humanoid robotics, ROS 2, Gazebo, Isaac Sim, and Vision-Language-Action foundation models.',
            'inLanguage': 'en-US',
            'potentialAction': {
              '@type': 'SearchAction',
              'target': 'https://your-docusaurus-site.example.com/?q={search_term_string}',
              'query-input': 'required name=search_term_string',
            },
          },
          {
            '@type': 'Course',
            '@id': 'https://your-docusaurus-site.example.com/#course',
            'name': 'Physical AI & Humanoid Robotics Curriculum',
            'description': 'A comprehensive 4-module, 26-chapter engineering pathway covering ROS 2 real-time middleware, physics simulation, NVIDIA Isaac perception, and Vision-Language-Action (VLA) models.',
            'provider': {
              '@type': 'Organization',
              'name': 'Physical AI & Humanoid Robotics Open Source Initiative',
              'url': 'https://github.com/MudassirT/GIAIC-Hackathon',
              'logo': 'https://your-docusaurus-site.example.com/img/physical-ai-robotics-logo.svg',
            },
            'educationalLevel': 'Advanced',
            'isAccessibleForFree': true,
            'hasCourseInstance': {
              '@type': 'CourseInstance',
              'courseMode': 'Online',
              'courseWorkload': 'PT20H',
            },
          },
        ],
      }),
    },
  ],

  markdown: {
    mermaid: true,
  },
  themes: ['@docusaurus/theme-mermaid'],

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
    // Custom Webpack/Rspack plugin to expose REACT_APP_FASTAPI_BASE_URL to client-side
    function (context, options) {
      return {
        name: 'webpack-env-plugin',
        configureWebpack(config, isServer, utils) {
          // Only apply on the client-side build
          if (!isServer) {
            // Detect rspack vs webpack bundler at runtime
            let BundlerDefinePlugin;
            try {
              BundlerDefinePlugin = require('@rspack/core').DefinePlugin;
            } catch {
              BundlerDefinePlugin = require('webpack').DefinePlugin;
            }
            return {
              plugins: [
                new BundlerDefinePlugin({
                  'process.env.REACT_APP_FASTAPI_BASE_URL': JSON.stringify(process.env.REACT_APP_FASTAPI_BASE_URL),
                }),
              ],
            };
          }
          return {};
        },
      };
    },
  ],

  themeConfig: {
    // Senior SEO Metadata Configuration
    metadata: [
      {
        name: 'description',
        content: 'The definitive open-access engineering curriculum for Physical AI, humanoid robotics, ROS 2 real-time middleware, Gazebo & Unity simulation, NVIDIA Isaac perception, and Vision-Language-Action (VLA) foundation models.',
      },
      {
        name: 'keywords',
        content: 'Physical AI, Humanoid Robotics, Embodied AI, ROS 2, ROS 2 Humble, DDS, CycloneDDS, Iceoryx, Digital Twins, Gazebo Harmonic, DART physics, Unity HDRP, NVIDIA Isaac Sim, cuVSLAM, Nav2, Vision-Language-Action, OpenVLA, π0, Octo, Robot Learning, Bipedal Locomotion, Reinforcement Learning, Sim-to-Real, RAG Agent, Qdrant Cloud',
      },
      {
        name: 'author',
        content: 'Mudassir Ahmed & Physical AI Robotics Engineering Team',
      },
      {
        name: 'robots',
        content: 'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1',
      },
      {
        name: 'googlebot',
        content: 'index, follow, max-snippet:-1, max-image-preview:large',
      },
      {
        property: 'og:site_name',
        content: 'Physical AI & Humanoid Robotics',
      },
      {
        property: 'og:type',
        content: 'website',
      },
      {
        property: 'og:title',
        content: 'Physical AI & Humanoid Robotics | The Open Curriculum for Embodied AI',
      },
      {
        property: 'og:description',
        content: 'Master low-latency ROS 2 middleware, physics-accurate Digital Twins, NVIDIA Isaac perception, and Vision-Language-Action foundation models for bipedal humanoids.',
      },
      {
        property: 'og:image',
        content: 'https://your-docusaurus-site.example.com/img/docusaurus-social-card.jpg',
      },
      {
        property: 'og:image:alt',
        content: 'Physical AI & Humanoid Robotics Curriculum Cover',
      },
      {
        name: 'twitter:card',
        content: 'summary_large_image',
      },
      {
        name: 'twitter:site',
        content: '@Mudassir__Ahmed',
      },
      {
        name: 'twitter:creator',
        content: '@Mudassir__Ahmed',
      },
      {
        name: 'twitter:title',
        content: 'Physical AI & Humanoid Robotics | The Open Curriculum for Embodied AI',
      },
      {
        name: 'twitter:description',
        content: 'The definitive engineering curriculum to architect, simulate, and deploy autonomous bipedal humanoids — from ROS 2 middleware to Vision-Language-Action foundation models.',
      },
      {
        name: 'twitter:image',
        content: 'https://your-docusaurus-site.example.com/img/docusaurus-social-card.jpg',
      },
      {
        name: 'theme-color',
        content: '#07090e',
      },
      {
        name: 'apple-mobile-web-app-capable',
        content: 'yes',
      },
      {
        name: 'apple-mobile-web-app-status-bar-style',
        content: 'black-translucent',
      },
    ],
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    mermaid: {
      theme: {light: 'neutral', dark: 'dark'},
    },
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI Humanoid Robotics Logo',
        src: 'img/physical-ai-robotics-logo.svg',
        srcDark: 'img/physical-ai-robotics-logo.svg',
        width: 34,
        height: 34,
      },
      items: [
        {
          to: '/ai-book/intro',
          label: 'Curriculum',
          position: 'left',
          activeBaseRegex: `/ai-book/`,
          docsPluginId: 'ai-book',
        },
        {
          type: 'dropdown',
          label: 'Modules',
          position: 'left',
          items: [
            {
              label: 'Module 1: The Robotic Nervous System (ROS 2)',
              to: '/ai-book/module1-ros2/1-1-introduction',
            },
            {
              label: 'Module 2: The Digital Twin (Gazebo & Unity)',
              to: '/ai-book/module2-digital-twin/2-1-introduction-to-digital-twins',
            },
            {
              label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
              to: '/ai-book/module3-ai-robot-brain/3-1-introduction-to-isaac-platform',
            },
            {
              label: 'Module 4: Vision-Language-Action (VLA)',
              to: '/ai-book/module4-vla/4-1-introduction-to-vla-systems',
            },
            {
              label: 'Module 5: Humanoid Kinematics & Dynamics',
              to: '/ai-book/module5-kinematics-dynamics/5-1-introduction-to-robot-kinematics',
            },
          ],
        },
        {
          to: '/#ai-assistant',
          label: 'AI Assistant',
          position: 'left',
        },
        {
          href: 'https://github.com/MudassirT/GIAIC-Hackathon',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Curriculum Modules',
          items: [
            {
              label: 'Introduction & Foundations',
              to: '/ai-book/intro',
            },
            {
              label: 'Module 1: ROS 2 Nervous System',
              to: '/ai-book/module1-ros2/1-1-introduction',
            },
            {
              label: 'Module 2: Digital Twin (Gazebo/Unity)',
              to: '/ai-book/module2-digital-twin/2-1-introduction-to-digital-twins',
            },
            {
              label: 'Module 3: AI-Robot Brain (Isaac)',
              to: '/ai-book/module3-ai-robot-brain/3-1-introduction-to-isaac-platform',
            },
            {
              label: 'Module 4: VLA Systems',
              to: '/ai-book/module4-vla/4-1-introduction-to-vla-systems',
            },
            {
              label: 'Module 5: Kinematics & Dynamics',
              to: '/ai-book/module5-kinematics-dynamics/5-1-introduction-to-robot-kinematics',
            },
          ],
        },
        {
          title: 'Community & Media',
          items: [
            {
              label: 'YouTube Channel',
              href: 'https://www.youtube.com/@MudassirAhmedMuhammadTariq',
            },
            {
              label: 'X (Twitter)',
              href: 'https://x.com/Mudassir__Ahmed',
            },
            {
              label: 'GIAIC Hackathon',
              href: 'https://github.com/MudassirT/GIAIC-Hackathon',
            },
          ],
        },
        {
          title: 'Open Source Ecosystem',
          items: [
            {
              label: 'GitHub Repository',
              href: 'https://github.com/MudassirT/GIAIC-Hackathon',
            },
            {
              label: 'ROS 2 Humble / Iron',
              href: 'https://docs.ros.org/en/humble/',
            },
            {
              label: 'NVIDIA Isaac Sim',
              href: 'https://developer.nvidia.com/isaac-sim',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics • Spec-Driven Development. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;