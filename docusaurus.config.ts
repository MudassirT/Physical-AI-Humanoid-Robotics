import fs from 'fs';
import path from 'path';
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

function getModuleRoute(dirName: string, firstChapter: string, categorySlug: string): string {
  const chapterPath = path.join(__dirname, 'ai-book-docs', dirName, `${firstChapter}.mdx`);
  if (fs.existsSync(chapterPath)) {
    return `/ai-book/${dirName}/${firstChapter}`;
  }
  const dirPath = path.join(__dirname, 'ai-book-docs', dirName);
  if (fs.existsSync(dirPath) && fs.readdirSync(dirPath).some((f) => f.endsWith('.md') || f.endsWith('.mdx'))) {
    return `/ai-book/${categorySlug}`;
  }
  return '/ai-book/intro';
}

const config: Config = {
  title: 'Physical AI & Humanoid Robotics | The Open Curriculum for Embodied AI',
  tagline: 'Master low-latency ROS 2 middleware, physics-accurate Digital Twins, NVIDIA Isaac perception, and Vision-Language-Action (VLA) foundation models for autonomous bipedal humanoids.',
  favicon: 'img/favicon.svg',

  stylesheets: [
    {
      href: 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css',
      type: 'text/css',
      integrity: 'sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+',
      crossorigin: 'anonymous',
    },
  ],

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
        remarkPlugins: [remarkMath],
        rehypePlugins: [rehypeKatex],
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
        width: 36,
        height: 36,
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
          label: 'Modules (1–12)',
          position: 'left',
          items: [
            {
              label: 'Module 1: The Robotic Nervous System (ROS 2)',
              to: getModuleRoute('module1-ros2', '1-1-introduction', 'category/module-1-robotic-nervous-system'),
            },
            {
              label: 'Module 2: The Digital Twin (Gazebo & Unity)',
              to: getModuleRoute('module2-digital-twin', '2-1-introduction-to-digital-twins', 'category/module-2-digital-twin'),
            },
            {
              label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac)',
              to: getModuleRoute('module3-ai-robot-brain', '3-1-introduction-to-isaac-platform', 'category/module-3-ai-robot-brain'),
            },
            {
              label: 'Module 4: Vision-Language-Action (VLA) Systems',
              to: getModuleRoute('module4-vla', '4-1-introduction-to-vla-systems', 'category/module-4-vla'),
            },
            {
              label: 'Module 5: Humanoid Kinematics & Dynamics',
              to: getModuleRoute('module5-kinematics-dynamics', '5-1-introduction-to-robot-kinematics', 'category/module-5-kinematics-dynamics'),
            },
            {
              label: 'Module 6: Bipedal Locomotion & Whole-Body Control',
              to: getModuleRoute('module6-bipedal-locomotion', '6-1-introduction-to-bipedal-locomotion', 'category/module-6-bipedal-locomotion'),
            },
            {
              label: 'Module 7: Dexterous Manipulation & Hand Design',
              to: getModuleRoute('module7-dexterous-manipulation', '7-1-introduction-to-dexterous-manipulation', 'category/module-7-dexterous-manipulation'),
            },
            {
              label: 'Module 8: Robot Learning & Reinforcement Learning',
              to: getModuleRoute('module8-robot-learning', '8-1-foundations-of-reinforcement-learning', 'category/module-8-robot-learning'),
            },
            {
              label: 'Module 9: Sim-to-Real Transfer & Domain Randomization',
              to: getModuleRoute('module9-sim-to-real', '9-1-the-reality-gap', 'category/module-9-sim-to-real'),
            },
            {
              label: 'Module 10: Hardware Architecture & Embedded Systems',
              to: getModuleRoute('module10-hardware-architecture', '10-1-humanoid-mechanical-design', 'category/module-10-hardware-architecture'),
            },
            {
              label: 'Module 11: Safety, Ethics & Deployment',
              to: getModuleRoute('module11-safety-ethics', '11-1-robot-safety-standards', 'category/module-11-safety-ethics'),
            },
            {
              label: 'Module 12: Capstone Projects & Research Frontiers',
              to: getModuleRoute('module12-capstone-frontiers', '12-1-capstone-project-guide', 'category/module-12-capstone-frontiers'),
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
          title: 'Curriculum (Modules 1–6)',
          items: [
            {
              label: 'Introduction & Foundations',
              to: '/ai-book/intro',
            },
            {
              label: 'Module 1: ROS 2 Nervous System',
              to: getModuleRoute('module1-ros2', '1-1-introduction', 'category/module-1-robotic-nervous-system'),
            },
            {
              label: 'Module 2: Digital Twin (Gazebo/Unity)',
              to: getModuleRoute('module2-digital-twin', '2-1-introduction-to-digital-twins', 'category/module-2-digital-twin'),
            },
            {
              label: 'Module 3: AI-Robot Brain (Isaac)',
              to: getModuleRoute('module3-ai-robot-brain', '3-1-introduction-to-isaac-platform', 'category/module-3-ai-robot-brain'),
            },
            {
              label: 'Module 4: VLA Systems',
              to: getModuleRoute('module4-vla', '4-1-introduction-to-vla-systems', 'category/module-4-vla'),
            },
            {
              label: 'Module 5: Kinematics & Dynamics',
              to: getModuleRoute('module5-kinematics-dynamics', '5-1-introduction-to-robot-kinematics', 'category/module-5-kinematics-dynamics'),
            },
            {
              label: 'Module 6: Bipedal Locomotion',
              to: getModuleRoute('module6-bipedal-locomotion', '6-1-introduction-to-bipedal-locomotion', 'category/module-6-bipedal-locomotion'),
            },
          ],
        },
        {
          title: 'Curriculum (Modules 7–12)',
          items: [
            {
              label: 'Module 7: Dexterous Manipulation',
              to: getModuleRoute('module7-dexterous-manipulation', '7-1-introduction-to-dexterous-manipulation', 'category/module-7-dexterous-manipulation'),
            },
            {
              label: 'Module 8: Robot Learning & RL',
              to: getModuleRoute('module8-robot-learning', '8-1-foundations-of-reinforcement-learning', 'category/module-8-robot-learning'),
            },
            {
              label: 'Module 9: Sim-to-Real Transfer',
              to: getModuleRoute('module9-sim-to-real', '9-1-the-reality-gap', 'category/module-9-sim-to-real'),
            },
            {
              label: 'Module 10: Hardware & Embedded',
              to: getModuleRoute('module10-hardware-architecture', '10-1-humanoid-mechanical-design', 'category/module-10-hardware-architecture'),
            },
            {
              label: 'Module 11: Safety, Ethics & Deployment',
              to: getModuleRoute('module11-safety-ethics', '11-1-robot-safety-standards', 'category/module-11-safety-ethics'),
            },
            {
              label: 'Module 12: Capstones & Frontiers',
              to: getModuleRoute('module12-capstone-frontiers', '12-1-capstone-project-guide', 'category/module-12-capstone-frontiers'),
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